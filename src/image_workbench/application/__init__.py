"""Application layer for use cases, commands, results, and owned ports.

Application code may depend on domain concepts and application-owned contracts.
It must not import adapter implementations or external framework DTOs.
"""

from .commands import (
    AddPipelineStepCommand,
    CreateSessionCommand,
    LoadImageReferenceCommand,
    MovePipelineStepCommand,
    RedoPipelineEditCommand,
    RemovePipelineStepCommand,
    ReplacePipelineStepCommand,
    RequestExecutionCommand,
    UndoPipelineEditCommand,
    ValidatePipelineProposalCommand,
)
from .exceptions import (
    ApplicationError,
    ExecutionRequestError,
    ExternalDependencyError,
    InvalidCommandError,
    PipelineEditError,
    SessionNotFoundError,
)
from .ports import (
    AIInterpretationPort,
    DiagnosticsPort,
    ExportWriterPort,
    ImageProcessingPort,
    ImageSourceAccessPort,
    MetadataAccessPort,
    PluginDiscoveryPort,
    ProjectStoragePort,
    QueueExecutionPort,
)
from .results import (
    DiagnosticsEvent,
    ExecutionArtifact,
    ExecutionResult,
    ImageMetadata,
    ImageReference,
    PipelineSuggestion,
    PipelineValidationResult,
    SessionSnapshot,
)
from .services import ExecutionService, PipelineService, SessionService

__all__ = [
    "AIInterpretationPort",
    "AddPipelineStepCommand",
    "ApplicationError",
    "CreateSessionCommand",
    "DiagnosticsEvent",
    "DiagnosticsPort",
    "ExecutionArtifact",
    "ExecutionRequestError",
    "ExecutionResult",
    "ExecutionService",
    "ExportWriterPort",
    "ExternalDependencyError",
    "ImageMetadata",
    "ImageProcessingPort",
    "ImageReference",
    "ImageSourceAccessPort",
    "InvalidCommandError",
    "LoadImageReferenceCommand",
    "MetadataAccessPort",
    "MovePipelineStepCommand",
    "PipelineEditError",
    "PipelineService",
    "PipelineSuggestion",
    "PipelineValidationResult",
    "PluginDiscoveryPort",
    "ProjectStoragePort",
    "QueueExecutionPort",
    "RedoPipelineEditCommand",
    "RemovePipelineStepCommand",
    "ReplacePipelineStepCommand",
    "RequestExecutionCommand",
    "SessionNotFoundError",
    "SessionService",
    "SessionSnapshot",
    "UndoPipelineEditCommand",
    "ValidatePipelineProposalCommand",
]
