# FROM apache/superset

# RUN --mount=type=tmpfs,dst=/tmp/superset-iris \
#     --mount=type=bind,src=.,dst=/tmp/dist/superset-iris \
#     cp -fR /tmp/dist/superset-iris/* /tmp/superset-iris/ && \
#     pip install -e /tmp/superset-iris

# ENV SUPERSET_PORT=52773

FROM intersystemsdc/iris-community:preview

ENV IRISUSERNAME=superset
ENV IRISPASSWORD=superset
ENV IRISNAMESPACE=superset