"""Explicit mappings from domain pipeline steps to Pillow operations."""

from __future__ import annotations

from collections.abc import Callable

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from image_workbench.domain import PipelineStep

from .exceptions import OperationMappingError

PillowOperation = Callable[[Image.Image], Image.Image]


def map_step_to_pillow_operation(step: PipelineStep) -> PillowOperation:
    """Return a Pillow transformation for one validated pipeline step."""
    operation_id = step.operation_id.value

    if operation_id == "blur":
        radius = _required_parameter(step, "radius")
        return lambda image: image.filter(ImageFilter.GaussianBlur(radius=radius))
    if operation_id == "brightness":
        delta = _required_parameter(step, "delta")
        return lambda image: ImageEnhance.Brightness(image).enhance(1.0 + delta)
    if operation_id == "contrast":
        factor = _required_parameter(step, "factor")
        return lambda image: ImageEnhance.Contrast(image).enhance(factor)
    if operation_id == "saturation":
        factor = _required_parameter(step, "factor")
        return lambda image: ImageEnhance.Color(image).enhance(factor)
    if operation_id == "sepia":
        intensity = _required_parameter(step, "intensity")
        return lambda image: _apply_sepia(image, intensity=intensity)
    if operation_id == "sharpen":
        amount = _required_parameter(step, "amount")
        return lambda image: ImageEnhance.Sharpness(image).enhance(1.0 + amount)

    raise OperationMappingError(
        f"Unsupported image-processing operation '{operation_id}' for step '{step.step_id.value}'."
    )


def _required_parameter(step: PipelineStep, name: str) -> float:
    try:
        return step.parameters[name]
    except KeyError as exc:
        raise OperationMappingError(
            f"Missing adapter parameter '{name}' for operation "
            f"'{step.operation_id.value}' in step '{step.step_id.value}'."
        ) from exc


def _apply_sepia(image: Image.Image, *, intensity: float) -> Image.Image:
    if intensity == 0.0:
        return image.copy()

    rgb_image = image.convert("RGB")
    grayscale = ImageOps.grayscale(rgb_image)
    sepia_image = ImageOps.colorize(grayscale, black="#2c1608", white="#f8e0a8")
    if intensity == 1.0:
        return sepia_image
    return Image.blend(rgb_image, sepia_image, intensity)
