insert into Service(ServiceId, Name, Owner, Criticality, SlaTarget, SloTarget, Status)
values
  ('ServicePayments', 'Payments', 'Operations', 'Critical', '99.9%', 'p95 < 500ms', 'Warning'),
  ('ServiceReporting', 'Reporting', 'Operations', 'Medium', '99.0%', 'p95 < 1000ms', 'OK')
on conflict do nothing;

insert into Application(ApplicationId, ServiceId, Name, Environment, HealthStatus, EndToEndPerformanceStatus)
values
  ('ApplicationPaymentsApi', 'ServicePayments', 'Payments API', 'Production', 'Warning', 'Warning'),
  ('ApplicationReportingApi', 'ServiceReporting', 'Reporting API', 'Production', 'OK', 'OK')
on conflict do nothing;

insert into MonitoredResource(ResourceId, ResourceType, Name, Platform, CapacityUnit, TotalCapacity, Status)
values
  ('ResourcePaymentsCpu', 'Server', 'payments-cpu', 'Linux', 'Percent', 100, 'Warning'),
  ('ResourcePaymentsStorage', 'Storage', 'payments-storage', 'Linux', 'Percent', 100, 'Critical'),
  ('ResourceReportingCpu', 'Server', 'reporting-cpu', 'Linux', 'Percent', 100, 'OK')
on conflict do nothing;

insert into ServiceResourceMap(MapId, ServiceId, ApplicationId, ResourceId, Role, ImpactWeight)
values
  ('MapPaymentsCpu', 'ServicePayments', 'ApplicationPaymentsApi', 'ResourcePaymentsCpu', 'Primary', 90),
  ('MapPaymentsStorage', 'ServicePayments', 'ApplicationPaymentsApi', 'ResourcePaymentsStorage', 'Primary', 100),
  ('MapReportingCpu', 'ServiceReporting', 'ApplicationReportingApi', 'ResourceReportingCpu', 'Primary', 80)
on conflict do nothing;

insert into AlertThreshold(ThresholdId, ScopeType, ScopeId, MetricName, WarningValue, CriticalValue, Comparison, Enabled)
values
  ('ThresholdCpu', 'ResourceType', 'Server', 'CPU', 75, 90, 'GreaterOrEqual', true),
  ('ThresholdStorage', 'ResourceType', 'Storage', 'Storage', 80, 95, 'GreaterOrEqual', true)
on conflict do nothing;
