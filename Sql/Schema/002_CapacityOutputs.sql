create table if not exists CapacityRun (
  CapacityRunId text primary key,
  StartedAt timestamp not null,
  FinishedAt timestamp,
  Status text not null,
  ProcessedResourceCount integer not null default 0,
  FailedResourceCount integer not null default 0,
  ErrorMessage text
);

create table if not exists CapacityKpi (
  CapacityKpiId text primary key,
  ResourceId text not null,
  MetricName text not null,
  CalculatedAt timestamp not null,
  WindowStart timestamp not null,
  WindowEnd timestamp not null,
  AverageUtilization numeric not null,
  PeakUtilization numeric not null,
  P95Utilization numeric not null,
  MonthlyGrowthRate numeric not null,
  HeadroomAvailable numeric not null,
  BaselineDelta numeric not null default 0
);

create table if not exists ForecastResult (
  ForecastResultId text primary key,
  ResourceId text not null,
  MetricName text not null,
  CalculatedAt timestamp not null,
  Forecast30Days numeric not null,
  Forecast60Days numeric not null,
  Forecast90Days numeric not null,
  DaysToSaturation integer,
  Confidence text not null
);

create table if not exists RiskAssessment (
  RiskAssessmentId text primary key,
  ScopeType text not null,
  ScopeId text not null,
  OverallRisk text not null,
  Reason text not null,
  CalculatedAt timestamp not null
);

create table if not exists Recommendation (
  RecommendationId text primary key,
  RiskAssessmentId text not null references RiskAssessment(RiskAssessmentId),
  ScopeType text not null,
  ScopeId text not null,
  Priority text not null,
  Action text not null,
  Reason text not null,
  Status text not null default 'Open'
);
