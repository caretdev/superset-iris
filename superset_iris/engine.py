import logging

from typing import (
    Any,
    Dict,
    ContextManager,
    TYPE_CHECKING,
)

import pandas as pd
from flask_babel import gettext as __
from marshmallow import Schema, fields
from marshmallow.validate import Range
from superset.db_engine_specs.base import BaseEngineSpec, BasicParametersType, BasicParametersMixin
from superset.sql_parse import Table
from sqlalchemy.engine.base import Engine

if TYPE_CHECKING:
    from superset.models.core import Database


logger = logging.getLogger(__name__)

class IRISParametersSchema(Schema):
    username = fields.String(allow_none=True, description=__('Username'))
    password = fields.String(allow_none=True, description=__('Password'))
    host = fields.String(required=True, description=__('Hostname or IP address'))
    port = fields.Integer(allow_none=True, description=__('Database port'), validate=Range(min=0, max=65535))
    database = fields.String(allow_none=True, description=__('Database name'))


class IRISEngineSpec(BaseEngineSpec, BasicParametersMixin):
    """
    See :py:class:`superset.db_engine_specs.base.BaseEngineSpec`
    """

    engine = 'iris'
    engine_name = 'InterSystems IRIS'

    allow_limit_clause = False

    max_column_name_length = 50

    sqlalchemy_uri_placeholder = 'iris://_SYSTEM:SYS@iris:1972/USER'
    parameters_schema = IRISParametersSchema()

    _time_grain_expressions = {
        None: "{col}",
        "P1D": "CAST({col} AS Date)",
        "P1W": "DATEADD(DAY, 1 - ((DATEPART(WEEKDAY, {col}) + 5) # 7), {col})",
        "P1M": "DATEADD(MONTH, DATEDIFF(MONTH, 1, {col}), 1)",
        "P3M": "DATEADD(QUARTER, DATEDIFF(MONTH, 1, {col}) \ 3, 1)",
        "P1Y": "DATEADD(YEAR, DATEDIFF(YEAR, 1, {col}) \ 3, 1)",
    }
