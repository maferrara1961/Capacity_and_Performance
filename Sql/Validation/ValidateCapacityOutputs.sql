select 'invalid_p95_peak' as CheckName, count(*) as Violations
from CapacityKpi
where P95Utilization > PeakUtilization;

select 'missing_critical_reason' as CheckName, count(*) as Violations
from RiskAssessment
where OverallRisk in ('Warning', 'Critical') and (Reason is null or Reason = '');
