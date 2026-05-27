"""Pillow-backed implementation of the application image-processing port."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

from PIL import Image, UnidentifiedImageError

from image_workbench.application import ExecutionArtifact, ImageReference
from image_workbench.domain import EnhancementPipeline, ImageId

from .exceptions import (
    ImageProcessingFailureError,
    ImageReadError,
    ImageWriteError,
    OperationMappingError,
    UnsupportedImageReferenceError,
)
from .mappers import map_step_to_pillow_operation

_SAFE_FILENAME_PATTERN = re.compile(r"[^A-Za-z0-9_.-]+")


class PillowImageProcessor:
    """Execute validated enhancement pipelines with Pillow behind the app port."""

    def __init__(self, *, output_directory: Path | str) -> None:
        self._output_directory = Path(output_directory)

    def execute_pipeline(
        self,
        image_reference: ImageReference,
        pipeline: EnhancementPipeline,
        *,
        session_id: str,
    ) -> ExecutionArtifact:
        source_path = _resolve_local_image_path(image_reference)
        output_path = self._build_output_path(
            image_reference=image_reference,
            pipeline=pipeline,
            session_id=session_id,
        )

        image = _open_rgb_image(source_path, image_reference=image_reference)
        try:
            for step in pipeline:
                operation = map_step_to_pillow_operation(step)
                image = operation(image)
        except OperationMappingError:
            raise
        except OSError as exc:
            raise ImageProcessingFailureError(
                f"Image processing failed for image '{image_reference.image_id.value}'."
            ) from exc

        _save_png(image, output_path, image_reference=image_reference)
        return ExecutionArtifact(
            session_id=session_id,
            output_image_id=ImageId(output_path.stem),
            applied_steps=tuple(step.step_id for step in pipeline),
            exported_uri=str(output_path),
        )

    def _build_output_path(
        self,
        *,
        image_reference: ImageReference,
        pipeline: EnhancementPipeline,
        session_id: str,
    ) -> Path:
        signature = hashlib.sha256()
        signature.update(session_id.encode("utf-8"))
        signature.update(b"\0")
        signature.update(image_reference.image_id.value.encode("utf-8"))
        for step in pipeline:
            signature.update(b"\0")
            signature.update(step.step_id.value.encode("utf-8"))
            signature.update(b":")
            signature.update(step.operation_id.value.encode("utf-8"))
            for key, value in step.parameters.items():
                signature.update(f":{key}={value:.12g}".encode())
        safe_session_id = _safe_filename(session_id)
        safe_image_id = _safe_filename(image_reference.image_id.value)
        digest = signature.hexdigest()[:16]
        return self._output_directory / f"{safe_session_id}-{safe_image_id}-{digest}.png"


def _resolve_local_image_path(image_reference: ImageReference) -> Path:
    source_uri = image_reference.source_uri.strip()
    parsed = urlparse(source_uri)
    if parsed.scheme == "file":
        path_text = unquote(parsed.path)
        if parsed.netloc:
            path_text = f"//{parsed.netloc}{path_text}"
        if path_text.startswith("/") and len(path_text) >= 3 and path_text[2] == ":":
            path_text = path_text[1:]
        return Path(path_text)
    if "://" in source_uri:
        raise UnsupportedImageReferenceError(
            f"Unsupported image reference scheme '{parsed.scheme}' for image "
            f"'{image_reference.image_id.value}'."
        )
    return Path(source_uri)


def _open_rgb_image(source_path: Path, *, image_reference: ImageReference) -> Image.Image:
    try:
        with Image.open(source_path) as loaded_image:
            return loaded_image.convert("RGB")
    except FileNotFoundError as exc:
        raise ImageReadError(
            f"Source image '{image_reference.image_id.value}' was not found at '{source_path}'."
        ) from exc
    except PermissionError as exc:
        raise ImageReadError(
            f"Source image '{image_reference.image_id.value}' is not readable at '{source_path}'."
        ) from exc
    except UnidentifiedImageError as exc:
        raise ImageReadError(
            f"Source image '{image_reference.image_id.value}' uses an unsupported format."
        ) from exc
    except OSError as exc:
        raise ImageReadError(
            f"Source image '{image_reference.image_id.value}' could not be read from "
            f"'{source_path}'."
        ) from exc


def _save_png(image: Image.Image, output_path: Path, *, image_reference: ImageReference) -> None:
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, format="PNG")
    except OSError as exc:
        raise ImageWriteError(
            f"Processed image '{image_reference.image_id.value}' could not be written to "
            f"'{output_path}'."
        ) from exc


def _safe_filename(value: str) -> str:
    safe_value = _SAFE_FILENAME_PATTERN.sub("-", value.strip()).strip(".-")
    return safe_value or "image"
