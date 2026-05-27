"""Application-layer failure types for use-case orchestration boundaries."""


class ApplicationError(ValueError):
    """Base class for application command and orchestration failures."""


class InvalidCommandError(ApplicationError):
    """Raised when an application command has invalid technical shape."""


class SessionNotFoundError(ApplicationError):
    """Raised when a requested session does not exist in application state."""


class PipelineEditError(ApplicationError):
    """Raised when pipeline edit orchestration fails at application boundary."""


class ExecutionRequestError(ApplicationError):
    """Raised when execution orchestration cannot satisfy an execution request."""


class ExternalDependencyError(ApplicationError):
    """Raised when a dependency port fails with a known technical failure."""
