from __future__ import annotations

from typing import Any, ReadOnly, Required, Sequence, TypedDict

from .const import DOMAIN_ERROR_MESSAGE, DOMAIN_VALIDATION_ERROR_MESSAGE


class FieldDetail(TypedDict):
    fields: Required[ReadOnly[str | Sequence[str]]]
    message: Required[ReadOnly[str]]


class DomainError(Exception):
    """Базовая ошибка домена."""

    message: str = DOMAIN_ERROR_MESSAGE
    details: dict[str, Any] | None = None

    def __init__(
        self,
        message: str | None = DOMAIN_ERROR_MESSAGE,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message if message else self.message
        self.details = details if details else self.details
        super().__init__(self.message, self.details)


class DomainValidationError(DomainError):
    """Ошибки валидации."""

    def __init__(self, errors: Sequence[FieldDetail]) -> None:
        if not errors:
            raise ValueError("errors cannot be empty sequence")

        super().__init__(
            DOMAIN_VALIDATION_ERROR_MESSAGE,
            {"errors": list(errors)},
        )
