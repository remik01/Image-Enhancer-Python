"""Domain layer API for framework-free pipeline modeling and invariants.

This package exposes immutable value objects, operation definitions, ordered
pipeline behavior, and undo/redo state transitions. It intentionally does not
depend on adapters, UI, HTTP, persistence, plugin implementation modules, or
image-processing libraries.
"""

from .exceptions import (
    DomainValidationError,
    DuplicatePipelineStepIdError,
    InvalidImageDimensionsError,
    InvalidImageIdentifierError,
    InvalidOperationIdentifierError,
    InvalidOperationParametersError,
    InvalidParameterNameError,
    InvalidParameterValueError,
    InvalidPipelineStepIdentifierError,
    PipelineHistoryStateError,
    PipelineOrderingError,
    PipelineStepNotFoundError,
    UnsupportedOperationError,
)
from .history import PipelineHistory
from .models import (
    EnhancementOperationId,
    ImageDimensions,
    ImageId,
    OperationParameters,
    PipelineStepId,
)
from .operations import (
    OperationDefinition,
    OperationParameterDefinition,
    resolve_operation_definition,
    supported_operations,
    validate_operation_parameters,
)
from .pipeline import EnhancementPipeline, PipelineStep

__all__ = [
    "DomainValidationError",
    "DuplicatePipelineStepIdError",
    "EnhancementOperationId",
    "EnhancementPipeline",
    "ImageDimensions",
    "ImageId",
    "InvalidImageDimensionsError",
    "InvalidImageIdentifierError",
    "InvalidOperationIdentifierError",
    "InvalidOperationParametersError",
    "InvalidParameterNameError",
    "InvalidParameterValueError",
    "InvalidPipelineStepIdentifierError",
    "OperationDefinition",
    "OperationParameterDefinition",
    "OperationParameters",
    "PipelineHistory",
    "PipelineHistoryStateError",
    "PipelineOrderingError",
    "PipelineStep",
    "PipelineStepId",
    "PipelineStepNotFoundError",
    "UnsupportedOperationError",
    "resolve_operation_definition",
    "supported_operations",
    "validate_operation_parameters",
]
