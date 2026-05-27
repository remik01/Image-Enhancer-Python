"""Local image-processing adapters for application-owned execution ports."""

from .exceptions import (
    ImageProcessingAdapterError,
    ImageProcessingFailureError,
    ImageReadError,
    ImageWriteError,
    OperationMappingError,
    UnsupportedImageReferenceError,
)
from .pillow_processor import PillowImageProcessor

__all__ = [
    "ImageProcessingAdapterError",
    "ImageProcessingFailureError",
    "ImageReadError",
    "ImageWriteError",
    "OperationMappingError",
    "PillowImageProcessor",
    "UnsupportedImageReferenceError",
]
