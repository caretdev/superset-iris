FROM apache/superset:4.0.1

RUN --mount=type=bind,src=.,dst=/tmp/dist/superset-iris \
    mkdir -p ~/superset-iris/ && \
    cp -fR /tmp/dist/superset-iris/* ~/superset-iris/; \
    pip install -e ~/superset-iris

COPY docker-entrypoint.sh /app/

COPY superset_config.py /app/pythonpath/superset_config.py

CMD [ "/app/docker-entrypoint.sh" ]