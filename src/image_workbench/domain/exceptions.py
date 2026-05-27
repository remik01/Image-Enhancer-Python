"""Domain-specific exceptions for pipeline invariant enforcement."""


class DomainValidationError(ValueError):
    """Base class for invalid domain state or command attempts."""


class InvalidImageIdentifierError(DomainValidationError):
    """Raised when an image identifier is missing or malformed."""


class InvalidImageDimensionsError(DomainValidationError):
    """Raised when image dimensions are not strictly positive integers."""


class InvalidOperationIdentifierError(DomainValidationError):
    """Raised when an operation identifier is missing or malformed."""


class InvalidPipelineStepIdentifierError(DomainValidationError):
    """Raised when a pipeline step identifier is missing or malformed."""


class InvalidParameterNameError(DomainValidationError):
    """Raised when a parameter name is missing or malformed."""


class InvalidParameterValueError(DomainValidationError):
    """Raised when a parameter value cannot be represented as a numeric value."""


class UnsupportedOperationError(DomainValidationError):
    """Raised when a pipeline references an unknown operation identifier."""


class InvalidOperationParametersError(DomainValidationError):
    """Raised when operation parameters are missing, unexpected, or out of range."""


class DuplicatePipelineStepIdError(DomainValidationError):
    """Raised when a pipeline definition contains duplicate step identifiers."""


class PipelineOrderingError(DomainValidationError):
    """Raised when an edit uses an invalid insertion or move index."""


class PipelineStepNotFoundError(DomainValidationError):
    """Raised when a requested step identifier is not present in the pipeline."""


class PipelineHistoryStateError(DomainValidationError):
    """Raised when undo/redo is requested without available history state."""
