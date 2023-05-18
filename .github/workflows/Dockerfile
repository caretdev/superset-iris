FROM intersystemsdc/iris-community

USER root

RUN apt update && apt install -y python3-venv

USER irisowner

RUN python3 -m venv ~/superset && \
    . ~/superset/bin/activate && \
    pip install superset-iris apache-superset sqlparse=='0.4.3' && \
    mkdir ~/superset/pythonpath && \
    echo '. ~/superset/bin/activate' >> ~/.bashrc

ENV FLASK_APP="superset.app:create_app()" \
    FLASK_ENV=production \
    SUPERSET_ENV=production \
    IRISUSERNAME=superset \
    IRISPASSWORD=superset \
    IRISNAMESPACE=superset \
    DATABASE_DIALECT=iris \
    DATABASE_USER=superset \
    DATABASE_PASSWORD=superset \
    DATABASE_DB=superset \
    DATABASE_HOST=localhost \
    DATABASE_PORT=1972

ENV PYTHONPATH=/home/irisowner/superset/pythonpath

COPY --chown=irisowner:irisowner *.sh /docker-entrypoint-initdb.d/

COPY --chown=irisowner:irisowner superset_config.py /home/irisowner/superset/pythonpath/

WORKDIR /home/irisowner/superset
