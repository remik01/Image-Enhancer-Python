"""Failure types for local image-processing adapter boundaries."""

from __future__ import annotations


class ImageProcessingAdapterError(OSError):
    """Base failure raised when local image-processing cannot satisfy the port."""


class UnsupportedImageReferenceError(ImageProcessingAdapterError):
    """Raised when an image reference uses a URI shape the adapter cannot resolve."""


class ImageReadError(ImageProcessingAdapterError):
    """Raised when source image content cannot be read or decoded safely."""


class ImageWriteError(ImageProcessingAdapterError):
    """Raised when processed output cannot be written to the adapter output path."""


class OperationMappingError(ImageProcessingAdapterError):
    """Raised when a validated pipeline step cannot be mapped to adapter behavior."""


class ImageProcessingFailureError(ImageProcessingAdapterError):
    """Raised when the image library fails while applying a supported operation."""
