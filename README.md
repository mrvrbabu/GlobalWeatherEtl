# GlobalWeatherEtl

# https://www.youtube.com/watch?v=Y_vQyMljDsE&ab_channel=KrishNaik

# How to run 

rbabu@k8s-master:~/GlobalWeatherEtl/airflow$ docker-compose up -d 
airflow_redis_1 is up-to-date
airflow_postgres_1 is up-to-date
Starting airflow_airflow-init_1 ... done
airflow_airflow-triggerer_1 is up-to-date
airflow_airflow-webserver_1 is up-to-date
airflow_airflow-worker_1 is up-to-date
airflow_airflow-scheduler_1 is up-to-date
rbabu@k8s-master:~/GlobalWeatherEtl/airflow$ docker ps 
CONTAINER ID   IMAGE                   COMMAND                  CREATED        STATUS                  PORTS                                                 NAMES
ae68fc6bfe8a   apache/airflow:2.10.5   "/usr/bin/dumb-init …"   29 hours ago   Up 29 hours (healthy)   0.0.0.0:5555->5555/tcp, :::5555->5555/tcp, 8080/tcp   airflow_flower_1
9227ff571a18   apache/airflow:2.10.5   "/usr/bin/dumb-init …"   29 hours ago   Up 29 hours (healthy)   8080/tcp                                              airflow_airflow-triggerer_1
ee2081ae3a04   apache/airflow:2.10.5   "/usr/bin/dumb-init …"   29 hours ago   Up 29 hours (healthy)   8080/tcp                                              airflow_airflow-worker_1
02939a5f3620   apache/airflow:2.10.5   "/usr/bin/dumb-init …"   29 hours ago   Up 29 hours (healthy)   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp             airflow_airflow-webserver_1
12c91ef7bd85   apache/airflow:2.10.5   "/usr/bin/dumb-init …"   29 hours ago   Up 29 hours (healthy)   8080/tcp                                              airflow_airflow-scheduler_1
d7ad1d412cc1   postgres:15.1           "docker-entrypoint.s…"   29 hours ago   Up 29 hours (healthy)   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp             airflow_postgres_1
faba4dcb31fd   redis:7.2-bookworm      "docker-entrypoint.s…"   29 hours ago   Up 29 hours (healthy)   6379/tcp                                              airflow_redis_1
rbabu@k8s-master:~/GlobalWeatherEtl/airflow$ date
Sun Feb 23 05:31:16 PM UTC 2025
rbabu@k8s-master:~/GlobalWeatherEtl/airflow$ 