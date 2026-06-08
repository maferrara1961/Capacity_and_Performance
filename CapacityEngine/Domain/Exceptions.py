class ValidationError(ValueError):
    """Raised when user-controlled or imported data fails validation."""


class CapacityCalculationError(RuntimeError):
    """Raised when a capacity calculation cannot complete deterministically."""
