"""Custom exception hierarchy for the student registry."""


class StudentRegistryError(Exception):
    """Base exception for the whole domain."""


class ValidationError(StudentRegistryError):
    """Raised when domain validation fails."""


class NotFoundError(StudentRegistryError):
    """Raised when an entity cannot be found."""


class DuplicateError(StudentRegistryError):
    """Raised when an entity already exists."""