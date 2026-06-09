select 'create database grafana'
where not exists (
  select 1 from pg_database where datname = 'grafana'
)\gexec
