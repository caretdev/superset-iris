# InterSystems IRIS support for Apache Superset

<img
  src="https://github.com/apache/superset/raw/master/superset-frontend/src/assets/branding/superset-logo-horiz-apache.png"
  alt="Superset"
  width="500"
/>

[Apache Superset](https://superset.apache.org/) is a modern data exploration and data visualization platform. Superset can replace or augment proprietary business intelligence tools for many teams. Superset integrates well with a variety of data sources.

## How to test with IRIS

* Clone this repository

```shell
git clone https://github.com/caretdev/superset-iris.git superset-iris
cd superset-iris
```

* Start Superset with Docker-Compose
```shell
docker-compose pull
docker-compose up -d
```

* During the start it imports example data to IRIS Database, it will take a while, to wait until it's done, run this command
```shell
docker-compose logs -f superset-init
```

> In addition there is `docker-compose-simple.yml` file, which contains only superset and IRIS, it loads examples too, but with no way to see the progress, but through Superset UI
> ```
> docker-compose -f docker-compose-simple.yml up -d --build 
> ```

When the command above will finish work, go to http://localhost:8088/dashboard/list/. Dashboards available without authorization. To access SQL Lab use admin/admin as login and password.

![Apache Superset](https://raw.githubusercontent.com/caretdev/superset-iris/main/imgs/superset.png)

With SQL Lab access to powerful SQL editor

![Apache Superset](https://raw.githubusercontent.com/caretdev/superset-iris/main/imgs/sqllab.png)

It is possible to upload CSV files to IRIS. Go to Settings, [Database Connections](http://localhost:8088/databaseview/list/). Edit action on database.

![Databases list](https://raw.githubusercontent.com/caretdev/superset-iris/main/imgs/databases.png)

In the modal dialog, go to Advanced, Security and check `Allow file uploads to database` and Finish

![Edit database](https://raw.githubusercontent.com/caretdev/superset-iris/main/imgs/edit-database.png)

And now [import CSV](http://localhost:8088/csvtodatabaseview/form) is available

![Import CSV](https://raw.githubusercontent.com/caretdev/superset-iris/main/imgs/import-csv.png)