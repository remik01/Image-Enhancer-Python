"""Filesystem export writer for deterministic batch export workflows."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, PngImagePlugin, UnidentifiedImageError

from image_workbench.application.export import BatchExportResult, ExportPreset, PlannedExport


class ExportWriterError(OSError):
    """Base failure for local filesystem export writes."""


class ExportConflictError(ExportWriterError):
    """Raised when export output conflicts with existing files or batch names."""


class FilesystemExportWriter:
    """Write planned exports to a normalized local destination directory."""

    def write_exports(
        self,
        planned_exports: tuple[PlannedExport, ...],
        *,
        preset: ExportPreset,
    ) -> BatchExportResult:
        destination = _normalize_destination(preset.destination)
        exported_uris: list[str] = []
        reserved_paths: set[Path] = set()
        for planned_export in planned_exports:
            output_path = _resolve_output_path(
                destination=destination,
                output_name=planned_export.output_name,
                conflict_policy=preset.conflict_policy,
                reserved_paths=reserved_paths,
            )
            _write_image(planned_export, output_path)
            reserved_paths.add(output_path)
            exported_uris.append(str(output_path))
        return BatchExportResult(exported_uris=tuple(exported_uris))


def _normalize_destination(raw_destination: str) -> Path:
    try:
        destination = Path(raw_destination).expanduser().resolve(strict=False)
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise ExportWriterError(
            f"Export destination is not writable: '{raw_destination}'."
        ) from exc
    if not destination.is_dir():
        raise ExportWriterError(f"Export destination is not a directory: '{destination}'.")
    return destination


def _resolve_output_path(
    *,
    destination: Path,
    output_name: str,
    conflict_policy: str,
    reserved_paths: set[Path],
) -> Path:
    candidate = (destination / output_name).resolve(strict=False)
    if destination not in (candidate, *candidate.parents):
        raise ExportWriterError(f"Export output escapes destination: '{output_name}'.")
    if candidate in reserved_paths and conflict_policy != "rename":
        raise ExportConflictError(f"Duplicate export output path: '{candidate}'.")
    if conflict_policy == "overwrite" or not candidate.exists():
        return candidate
    if conflict_policy == "fail":
        raise ExportConflictError(f"Export output already exists: '{candidate}'.")
    return _next_available_path(candidate, reserved_paths=reserved_paths)


def _next_available_path(candidate: Path, *, reserved_paths: set[Path]) -> Path:
    for index in range(2, 10_000):
        renamed = candidate.with_name(f"{candidate.stem}-{index:03d}{candidate.suffix}")
        if renamed not in reserved_paths and not renamed.exists():
            return renamed
    raise ExportConflictError(f"No available deterministic export name for '{candidate}'.")


def _write_image(planned_export: PlannedExport, output_path: Path) -> None:
    source_path = Path(planned_export.image.image_reference.source_uri)
    try:
        with Image.open(source_path) as image:
            converted = _convert_for_format(image, planned_export.output_format)
            save_kwargs = _metadata_save_kwargs(image, planned_export=planned_export)
            converted.save(
                output_path,
                format="JPEG" if planned_export.output_format == "jpeg" else "PNG",
                **save_kwargs,
            )
    except FileNotFoundError as exc:
        raise ExportWriterError(f"Export source was not found: '{source_path}'.") from exc
    except PermissionError as exc:
        raise ExportWriterError(f"Export source is not readable: '{source_path}'.") from exc
    except UnidentifiedImageError as exc:
        raise ExportWriterError(
            f"Export source is not a supported image: '{source_path}'."
        ) from exc
    except OSError as exc:
        raise ExportWriterError(f"Export write failed for '{output_path}'.") from exc


def _convert_for_format(image: Image.Image, output_format: str) -> Image.Image:
    if output_format == "jpeg" and image.mode not in {"L", "RGB"}:
        return image.convert("RGB")
    if output_format == "png":
        return image.copy()
    return image.copy()


def _metadata_save_kwargs(
    image: Image.Image,
    *,
    planned_export: PlannedExport,
) -> dict[str, object]:
    if planned_export.strip_metadata:
        return {}
    if planned_export.output_format == "png":
        png_info = PngImagePlugin.PngInfo()
        for key, value in image.info.items():
            if isinstance(key, str) and isinstance(value, str):
                png_info.add_text(key, value)
        return {"pnginfo": png_info}
    return {str(key): value for key, value in image.info.items() if isinstance(key, str)}
