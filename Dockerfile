FROM apache/superset

RUN --mount=type=tmpfs,dst=/tmp/superset-iris \
    --mount=type=bind,src=.,dst=/tmp/dist/superset-iris \
    cp -fR /tmp/dist/superset-iris/* /tmp/superset-iris/ && \
    pip install -e /tmp/superset-iris
