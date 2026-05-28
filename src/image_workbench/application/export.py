"""Application models and service for deterministic batch export planning."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal, Protocol

from image_workbench.domain import ImageId

from .batch import BatchImage
from .exceptions import InvalidCommandError

ExportFormat = Literal["jpeg", "png"]
ConflictPolicy = Literal["fail", "overwrite", "rename"]

_SAFE_FILENAME_PATTERN = re.compile(r"[^A-Za-z0-9_.-]+")
_SUPPORTED_FORMATS: frozenset[str] = frozenset({"jpeg", "png"})
_SUPPORTED_CONFLICT_POLICIES: frozenset[str] = frozenset({"fail", "overwrite", "rename"})
_KNOWN_IMAGE_EXTENSIONS: frozenset[str] = frozenset({"jpg", "jpeg", "png"})


def _require_text(value: str, *, label: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise InvalidCommandError(f"{label} must be a non-empty string.")
    return normalized


@dataclass(frozen=True)
class ExportPreset:
    """Caller-selected export behavior that makes naming and metadata policy explicit."""

    destination: str
    output_format: ExportFormat = "png"
    filename_template: str = "{index:03d}-{image_id}"
    conflict_policy: ConflictPolicy = "fail"
    strip_metadata: bool = True

    def __post_init__(self) -> None:
        output_format = self.output_format.lower()
        if output_format not in _SUPPORTED_FORMATS:
            raise InvalidCommandError(
                f"Export format must be one of {sorted(_SUPPORTED_FORMATS)!r}."
            )
        conflict_policy = self.conflict_policy.lower()
        if conflict_policy not in _SUPPORTED_CONFLICT_POLICIES:
            raise InvalidCommandError(
                f"Export conflict policy must be one of {sorted(_SUPPORTED_CONFLICT_POLICIES)!r}."
            )
        object.__setattr__(
            self,
            "destination",
            _require_text(self.destination, label="Export destination"),
        )
        object.__setattr__(
            self,
            "filename_template",
            _require_text(self.filename_template, label="Filename template"),
        )
        object.__setattr__(self, "output_format", output_format)
        object.__setattr__(self, "conflict_policy", conflict_policy)


@dataclass(frozen=True)
class PlannedExport:
    """One export request expressed in internal app terms, not filesystem DTOs."""

    image: BatchImage
    output_name: str
    output_format: ExportFormat
    strip_metadata: bool
    sequence_number: int


@dataclass(frozen=True)
class BatchExportCommand:
    """Request deterministic export planning and writing for a batch of images."""

    images: tuple[BatchImage, ...]
    preset: ExportPreset

    def __post_init__(self) -> None:
        images = tuple(self.images)
        if not images:
            raise InvalidCommandError("Batch export requires at least one image.")
        object.__setattr__(self, "images", images)


@dataclass(frozen=True)
class BatchExportResult:
    """Completed export locations in deterministic batch order."""

    exported_uris: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "exported_uris", tuple(self.exported_uris))


class BatchExportWriterPort(Protocol):
    """Write planned exports to an external destination selected by the caller."""

    def write_exports(
        self,
        planned_exports: tuple[PlannedExport, ...],
        *,
        preset: ExportPreset,
    ) -> BatchExportResult: ...


class BatchExportService:
    """Plan deterministic output names and delegate concrete writes to an adapter."""

    def __init__(self, *, export_writer_port: BatchExportWriterPort) -> None:
        self._export_writer_port = export_writer_port

    def export_batch(self, command: BatchExportCommand) -> BatchExportResult:
        planned_exports = plan_exports(command)
        return self._export_writer_port.write_exports(planned_exports, preset=command.preset)


def plan_exports(command: BatchExportCommand) -> tuple[PlannedExport, ...]:
    """Build deterministic export names before crossing the filesystem boundary."""
    name_counts: dict[str, int] = {}
    planned_exports: list[PlannedExport] = []
    for index, image in enumerate(command.images, start=1):
        base_name = _render_output_name(
            template=command.preset.filename_template,
            index=index,
            image_id=image.image_reference.image_id,
            source_name=image.source_name,
        )
        name = _with_extension(base_name, command.preset.output_format)
        occurrence = name_counts.get(name, 0)
        name_counts[name] = occurrence + 1
        if occurrence:
            if command.preset.conflict_policy != "rename":
                raise InvalidCommandError(
                    f"Duplicate output name '{name}' requires conflict policy 'rename'."
                )
            name = _add_suffix(name, occurrence + 1)
        planned_exports.append(
            PlannedExport(
                image=image,
                output_name=name,
                output_format=command.preset.output_format,
                strip_metadata=command.preset.strip_metadata,
                sequence_number=index,
            )
        )
    return tuple(planned_exports)


def _render_output_name(
    *,
    template: str,
    index: int,
    image_id: ImageId,
    source_name: str,
) -> str:
    stem = source_name.rsplit(".", maxsplit=1)[0]
    try:
        rendered = template.format(
            index=index,
            image_id=_safe_filename(image_id.value),
            stem=_safe_filename(stem),
        )
    except (IndexError, KeyError, ValueError) as exc:
        raise InvalidCommandError(f"Filename template is invalid: {template!r}.") from exc
    return _safe_filename(rendered)


def _with_extension(base_name: str, output_format: ExportFormat) -> str:
    extension = "jpg" if output_format == "jpeg" else "png"
    stem = base_name
    if "." in base_name:
        candidate_stem, candidate_extension = base_name.rsplit(".", maxsplit=1)
        if candidate_extension.casefold() in _KNOWN_IMAGE_EXTENSIONS:
            stem = candidate_stem
    return f"{stem}.{extension}"


def _add_suffix(name: str, occurrence: int) -> str:
    stem, extension = name.rsplit(".", maxsplit=1)
    return f"{stem}-{occurrence:03d}.{extension}"


def _safe_filename(value: str) -> str:
    safe_value = _SAFE_FILENAME_PATTERN.sub("-", value.strip()).strip(".-")
    return safe_value or "image"
