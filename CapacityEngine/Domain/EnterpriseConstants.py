from enum import Enum


class TechnologyDomainName(str, Enum):
    INFRASTRUCTURE = "Infrastructure"
    OPERATING_SYSTEM = "OperatingSystem"
    DATABASE = "Database"
    MIDDLEWARE = "Middleware"
    CONTAINER_PLATFORM = "ContainerPlatform"
    MESSAGING_PLATFORM = "MessagingPlatform"
    MONITORING_PLATFORM = "MonitoringPlatform"
    ENTERPRISE_APPLICATION = "EnterpriseApplication"
    BUSINESS_SERVICE = "BusinessService"


class EnterpriseStatus(str, Enum):
    ACTIVE = "Active"
    DEPRECATED = "Deprecated"
    DISABLED = "Disabled"
    UNKNOWN = "Unknown"


class EvidenceState(str, Enum):
    AVAILABLE = "Available"
    MISSING = "Missing"
    UNKNOWN = "Unknown"
    INCOMPLETE = "Incomplete"
    UNVERIFIED = "Unverified"


class ScoreType(str, Enum):
    CAPACITY = "Capacity"
    PERFORMANCE = "Performance"
    AVAILABILITY = "Availability"
    LIFECYCLE = "Lifecycle"
    COMPLIANCE = "Compliance"
    MONITORING_CONFIDENCE = "MonitoringConfidence"
    TECHNOLOGY_HEALTH = "TechnologyHealth"


class ScoreClassification(str, Enum):
    EXCELLENT = "Excellent"
    HEALTHY = "Healthy"
    ATTENTION_REQUIRED = "AttentionRequired"
    AT_RISK = "AtRisk"
    CRITICAL = "Critical"
    UNKNOWN = "Unknown"


class EnterpriseRiskSeverity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class RiskCategory(str, Enum):
    CAPACITY = "Capacity"
    PERFORMANCE = "Performance"
    AVAILABILITY = "Availability"
    LIFECYCLE = "Lifecycle"
    COMPLIANCE = "Compliance"
    MONITORING = "Monitoring"


class ScopeType(str, Enum):
    ENTERPRISE = "Enterprise"
    DOMAIN = "Domain"
    BUSINESS_SERVICE = "BusinessService"
    TECHNOLOGY_COMPONENT = "TechnologyComponent"


class FreshnessStatus(str, Enum):
    FRESH = "Fresh"
    STALE = "Stale"
    EXPIRED = "Expired"
    UNKNOWN = "Unknown"


class ForecastConfidence(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
