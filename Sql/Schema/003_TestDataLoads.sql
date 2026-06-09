create table if not exists TestLoad (
  LoadId text primary key,
  ScenarioProfile text not null,
  RequestedVolume text not null,
  CreatedAt timestamp not null,
  FinishedAt timestamp,
  Status text not null,
  GeneratedServiceCount integer not null default 0,
  GeneratedResourceCount integer not null default 0,
  GeneratedMetricSampleCount integer not null default 0,
  GeneratedKpiCount integer not null default 0,
  GeneratedForecastCount integer not null default 0,
  GeneratedRiskCount integer not null default 0,
  GeneratedRecommendationCount integer not null default 0,
  ErrorMessage text,
  IsTestData boolean not null default true
);

create table if not exists TestDataRecordMap (
  RecordMapId text primary key,
  LoadId text not null references TestLoad(LoadId),
  RecordType text not null,
  RecordId text not null,
  IsTestData boolean not null default true
);
