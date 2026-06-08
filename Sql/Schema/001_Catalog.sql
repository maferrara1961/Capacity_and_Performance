create table if not exists Service (
  ServiceId text primary key,
  Name text not null unique,
  Owner text not null,
  Criticality text not null check (Criticality in ('Low', 'Medium', 'High', 'Critical')),
  SlaTarget text,
  SloTarget text,
  Status text not null default 'Unknown'
);

create table if not exists Application (
  ApplicationId text primary key,
  ServiceId text not null references Service(ServiceId),
  Name text not null,
  Environment text not null,
  HealthStatus text not null default 'Unknown',
  EndToEndPerformanceStatus text not null default 'Unknown'
);

create table if not exists MonitoredResource (
  ResourceId text primary key,
  ResourceType text not null,
  Name text not null,
  Platform text not null,
  CapacityUnit text not null,
  TotalCapacity numeric,
  Status text not null default 'Unknown'
);

create table if not exists ServiceResourceMap (
  MapId text primary key,
  ServiceId text not null references Service(ServiceId),
  ApplicationId text references Application(ApplicationId),
  ResourceId text not null references MonitoredResource(ResourceId),
  Role text not null,
  ImpactWeight integer not null check (ImpactWeight between 1 and 100)
);

create table if not exists AlertThreshold (
  ThresholdId text primary key,
  ScopeType text not null,
  ScopeId text,
  MetricName text not null,
  WarningValue numeric not null,
  CriticalValue numeric not null,
  Comparison text not null,
  Enabled boolean not null default true
);

create table if not exists Baseline (
  BaselineId text primary key,
  ResourceId text not null references MonitoredResource(ResourceId),
  MetricName text not null,
  PeriodStart timestamp not null,
  PeriodEnd timestamp not null,
  AverageValue numeric not null,
  P95Value numeric not null,
  PeakValue numeric not null
);
