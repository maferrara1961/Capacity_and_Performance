select 'missing_service_owner' as CheckName, count(*) as Violations
from Service
where Owner is null or Owner = '';

select 'invalid_mapping_weight' as CheckName, count(*) as Violations
from ServiceResourceMap
where ImpactWeight < 1 or ImpactWeight > 100;
