from setuptools import setup

setup(
    install_requires=[
        "sqlalchemy-iris~=0.7.0",
    ],
    entry_points={
        'superset.db_engine_specs': ['iris=superset_iris.engine:IRISEngineSpec']
    },
)
