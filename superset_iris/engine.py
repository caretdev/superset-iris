import logging
import re

from typing import (
    Any,
    Dict,
    List,
    TYPE_CHECKING,
    Pattern,
    Tuple,
    Optional,
)

import pandas as pd
from flask_babel import gettext as __
from marshmallow import Schema, fields
from marshmallow.validate import Range
from superset.db_engine_specs.base import (
    BaseEngineSpec,
    BasicParametersType,
    BasicParametersMixin,
    BasicPropertiesType,
)
from superset.constants import USER_AGENT
from superset.errors import ErrorLevel, SupersetErrorType, SupersetError
from superset.sql_parse import Table
from superset.databases.utils import make_url_safe
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
from superset.utils.core import GenericDataType
from typing_extensions import TypedDict

from sqlalchemy_iris import BIT

if TYPE_CHECKING:
    from superset.models.core import Database


logger = logging.getLogger(__name__)

# Regular expressions to catch custom errors
CONNECTION_ACCESS_DENIED_REGEX = re.compile("Access Denied")

TABLE_DOES_NOT_EXIST_REGEX = re.compile("Table '(?P<table_name>.+?)' not found")

COLUMN_DOES_NOT_EXIST_REGEX = re.compile(
    "Field '(?P<column_name>.+?)' not found in the applicable tables\^(?P<location>.+?)"
)


class IRISParametersSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    host = fields.Str(required=True)
    port = fields.Integer(required=True)
    database = fields.Str(required=True)


class IRISParametersType(TypedDict):
    username: str
    password: str
    host: str
    port: int
    database: str


class IRISPropertiesType(TypedDict):
    parameters: IRISParametersType


class IRISEngineSpec(BaseEngineSpec, BasicParametersMixin):
    """
    See :py:class:`superset.db_engine_specs.base.BaseEngineSpec`
    """

    engine = "iris"
    engine_name = "InterSystems IRIS"

    parameters_schema = IRISParametersSchema()
    default_driver = "iris"

    allow_limit_clause = False

    max_column_name_length = 50

    sqlalchemy_uri_placeholder = "iris://{username}:{password}@{host}:{port}/{database}"
    parameters_schema = IRISParametersSchema()

    column_type_mappings = (
        (
            re.compile(r"^bit", re.IGNORECASE),
            BIT(),
            GenericDataType.NUMERIC,
        ),
        (
            re.compile(r"^bool(ean)?", re.IGNORECASE),
            BIT(),
            GenericDataType.NUMERIC,
        ),
    )

    @staticmethod
    def get_extra_params(database: "Database") -> Dict[str, Any]:
        """
        Add a user agent to be used in the connection.
        """
        extra: Dict[str, Any] = BaseEngineSpec.get_extra_params(database)
        engine_params: Dict[str, Any] = extra.setdefault("engine_params", {})
        connect_args: Dict[str, Any] = engine_params.setdefault("connect_args", {})

        connect_args.setdefault("application_name", USER_AGENT)

        return extra

    def build_sqlalchemy_uri(
        cls,
        parameters: IRISParametersType,
        encrypted_extra: Optional[  # pylint: disable=unused-argument
            Dict[str, Any]
        ] = None,
    ) -> str:
        url = str(
            URL(
                "iris",
                username=parameters.get("username"),
                password=parameters.get("password"),
                host=parameters.get("host"),
                port=parameters.get("port"),
                database=parameters.get("database"),
            )
        )
        return url

    @classmethod
    def get_parameters_from_uri(
        cls,
        uri: str,
        encrypted_extra: Optional[  # pylint: disable=unused-argument
            Dict[str, str]
        ] = None,
    ) -> Any:
        url = make_url_safe(uri)
        return {
            "username": url.username,
            "password": url.password,
            "host": url.host,
            "port": url.port,
            "database": url.database,
        }

    @classmethod
    def validate_parameters(cls, properties: IRISPropertiesType) -> List[SupersetError]:
        errors: List[SupersetError] = []
        required = {
            "username",
            "password",
            "host",
            "port",
            "database",
        }
        parameters = properties.get("parameters", {})
        present = {key for key in parameters if parameters.get(key, ())}
        missing = sorted(required - present)

        if missing:
            errors.append(
                SupersetError(
                    message=f'One or more parameters are missing: {", ".join(missing)}',
                    error_type=SupersetErrorType.CONNECTION_MISSING_PARAMETERS_ERROR,
                    level=ErrorLevel.WARNING,
                    extra={"missing": missing},
                ),
            )
        return errors

    _time_grain_expressions = {
        None: "{col}",
        "PT1S": "CAST(TO_CHAR(CAST({col} AS TIMESTAMP), 'YYYY-MM-DD HH24:MM:SS') AS DATETIME)",
        "PT1M": "CAST(TO_CHAR(CAST({col} AS TIMESTAMP), 'YYYY-MM-DD HH24:MM:00') AS DATETIME)",
        "PT1H": "CAST(TO_CHAR(CAST({col} AS TIMESTAMP), 'YYYY-MM-DD HH24:00:00') AS DATETIME)",
        "P1D": "CAST(CAST({col} AS TIMESTAMP) AS Date)",
        "P1W": "CAST(DATEADD(DAY, 1 - MOD((DATEPART(WEEKDAY, {col}) + 5), 7), {col}) AS DATE)",
        "P1M": "CAST(DATEADD(MONTH, DATEDIFF(MONTH, 1, {col}), 1) AS DATE)",
        "P3M": "CAST(DATEADD(QUARTER, DATEDIFF(MONTH, 1, {col}) \ 3, 1) AS DATE)",
        "P1Y": "CAST(DATEADD(YEAR, DATEDIFF(YEAR, 1, {col}), 1) AS DATE)",
    }

    custom_errors: Dict[Pattern[str], Tuple[str, SupersetErrorType, Dict[str, Any]]] = {
        CONNECTION_ACCESS_DENIED_REGEX: (
            __("Either the username, password or namespace is incorrect."),
            SupersetErrorType.CONNECTION_ACCESS_DENIED_ERROR,
            {"invalid": ["username", "password", "database"]},
        ),
        COLUMN_DOES_NOT_EXIST_REGEX: (
            __(
                'We can\'t seem to resolve the column "%(column_name)s"',
            ),
            SupersetErrorType.COLUMN_DOES_NOT_EXIST_ERROR,
            {},
        ),
        TABLE_DOES_NOT_EXIST_REGEX: (
            __(
                'The table "%(table_name)s" does not exist. '
                "A valid table must be used to run this query.",
            ),
            SupersetErrorType.TABLE_DOES_NOT_EXIST_ERROR,
            {},
        ),
    }
