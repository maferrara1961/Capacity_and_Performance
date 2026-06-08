from enum import Enum


class RiskLevel(str, Enum):
    OK = "OK"
    WARNING = "Warning"
    CRITICAL = "Critical"
    UNKNOWN = "Unknown"


class ResourceType(str, Enum):
    SERVER = "Server"
    DATABASE = "Database"
    STORAGE = "Storage"
    NETWORK = "Network"
    DEPENDENCY = "Dependency"
    APPLICATION_COMPONENT = "ApplicationComponent"


class MetricName(str, Enum):
    CPU = "CPU"
    RAM = "RAM"
    STORAGE = "Storage"
    IOPS = "IOPS"
    NETWORK = "Network"
    LATENCY = "Latency"
    THROUGHPUT = "Throughput"
    ERRORS = "Errors"
    SATURATION = "Saturation"


class Comparison(str, Enum):
    GREATER_THAN = "GreaterThan"
    GREATER_OR_EQUAL = "GreaterOrEqual"
    LESS_THAN = "LessThan"
    LESS_OR_EQUAL = "LessOrEqual"


class Confidence(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
