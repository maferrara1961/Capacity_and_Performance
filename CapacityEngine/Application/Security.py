from dataclasses import dataclass

from CapacityEngine.Domain.Exceptions import ValidationError


@dataclass(frozen=True)
class AuthenticatedContext:
    UserId: str
    Roles: tuple[str, ...]


def RequireAuthenticated(Context: AuthenticatedContext | None) -> AuthenticatedContext:
    if Context is None or not Context.UserId:
        raise PermissionError("Authentication is required")
    return Context


def RequireRole(Context: AuthenticatedContext | None, AllowedRoles: set[str]) -> None:
    Context = RequireAuthenticated(Context)
    if not set(Context.Roles).intersection(AllowedRoles):
        raise PermissionError("Authorization failed")


def ValidateCredentialInput(UserName: str, Password: str) -> None:
    if not UserName.strip() or not Password:
        raise ValidationError("Credentials are required")
