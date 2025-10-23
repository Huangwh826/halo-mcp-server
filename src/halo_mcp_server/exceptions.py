"""Custom exceptions for Halo MCP Server."""


class HaloMCPError(Exception):
    """Base exception for Halo MCP Server."""

    def __init__(self, message: str, details: dict = None):
        """
        Initialize exception.

        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class AuthenticationError(HaloMCPError):
    """Authentication failed."""

    pass


class AuthorizationError(HaloMCPError):
    """Authorization/permission denied."""

    pass


class ResourceNotFoundError(HaloMCPError):
    """Resource not found."""

    def __init__(self, resource_type: str, name: str):
        """
        Initialize resource not found error.

        Args:
            resource_type: Type of resource
            name: Name of resource
        """
        super().__init__(f"{resource_type} '{name}' not found")
        self.resource_type = resource_type
        self.name = name


class ValidationError(HaloMCPError):
    """Data validation error."""

    pass


class NetworkError(HaloMCPError):
    """Network/HTTP error."""

    def __init__(self, message: str, status_code: int = None, details: dict = None):
        """
        Initialize network error.

        Args:
            message: Error message
            status_code: HTTP status code
            details: Additional error details
        """
        super().__init__(message, details)
        self.status_code = status_code


class ConfigurationError(HaloMCPError):
    """Configuration error."""

    pass


class OperationError(HaloMCPError):
    """Operation failed."""

    pass
