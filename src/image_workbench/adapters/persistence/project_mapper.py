"""Explicit mapping between v1 project-file DTOs and application models."""

from __future__ import annotations

from pathlib import Path

from image_workbench.application import SessionSnapshot
from image_workbench.domain import (
    DomainValidationError,
    EnhancementOperationId,
    EnhancementPipeline,
    ImageDimensions,
    ImageId,
    OperationParameters,
    PipelineStep,
    PipelineStepId,
)

from .schema import (
    DIMENSIONS_FIELDS,
    IMAGE_FIELDS,
    PIPELINE_FIELDS,
    PROJECT_FIELDS,
    SCHEMA_VERSION,
    STEP_FIELDS,
    ProjectFileValidationError,
    require_array,
    require_exact_fields,
    require_int,
    require_nullable_string,
    require_number,
    require_object,
    require_string,
    validate_project_document,
)


def snapshot_to_project_document(snapshot: SessionSnapshot) -> dict[str, object]:
    """Map an application session snapshot into the v1 external project contract."""
    image_id = snapshot.image_id.value
    return {
        "schema_version": SCHEMA_VERSION,
        "project": {
            "session_id": snapshot.session_id,
            "active_image_id": image_id,
        },
        "images": [
            {
                "image_id": image_id,
                "source_uri": snapshot.source_uri,
                "dimensions": {
                    "width": snapshot.image_dimensions.width,
                    "height": snapshot.image_dimensions.height,
                },
            }
        ],
        "pipelines": [
            {
                "image_id": image_id,
                "steps": [
                    {
                        "step_id": step.step_id.value,
                        "operation_id": step.operation_id.value,
                        "parameters": {
                            key: step.parameters[key] for key in sorted(step.parameters)
                        },
                    }
                    for step in snapshot.pipeline
                ],
            }
        ],
        "settings": {},
    }


def project_document_to_snapshot(document: object, *, source: Path) -> SessionSnapshot:
    """Validate and map a v1 project document into an application session snapshot."""
    root = validate_project_document(document, source=source)
    project = _read_project(root["project"], source=source)
    images = _read_images(root["images"], source=source)
    pipelines = _read_pipelines(root["pipelines"], source=source)

    active_image_id = project["active_image_id"]
    image = _require_single_image(images, active_image_id=active_image_id, source=source)
    pipeline = _require_single_pipeline(
        pipelines,
        active_image_id=active_image_id,
        source=source,
    )
    dimensions = image["dimensions"]
    if not isinstance(dimensions, ImageDimensions):
        raise ProjectFileValidationError(
            f"Project file '{source}' image dimensions mapping failed for image "
            f"'{active_image_id}'."
        )
    return SessionSnapshot(
        session_id=project["session_id"],
        image_id=ImageId(active_image_id),
        image_dimensions=dimensions,
        pipeline=pipeline,
        can_undo=False,
        can_redo=False,
        source_uri=_require_nullable_string_value(image["source_uri"], source=source),
    )


def _read_project(value: object, *, source: Path) -> dict[str, str]:
    project = require_object(value, field_path="$.project", source=source)
    require_exact_fields(
        project,
        expected_fields=PROJECT_FIELDS,
        field_path="$.project",
        source=source,
    )
    return {
        "session_id": require_string(
            project["session_id"],
            field_path="$.project.session_id",
            source=source,
        ),
        "active_image_id": require_string(
            project["active_image_id"],
            field_path="$.project.active_image_id",
            source=source,
        ),
    }


def _read_images(value: object, *, source: Path) -> list[dict[str, object]]:
    image_values = require_array(value, field_path="$.images", source=source)
    images: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for index, image_value in enumerate(image_values):
        field_path = f"$.images[{index}]"
        image = require_object(image_value, field_path=field_path, source=source)
        require_exact_fields(
            image, expected_fields=IMAGE_FIELDS, field_path=field_path, source=source
        )
        image_id = require_string(
            image["image_id"], field_path=f"{field_path}.image_id", source=source
        )
        if image_id in seen_ids:
            raise ProjectFileValidationError(
                f"Project file '{source}' contains duplicate image_id '{image_id}'."
            )
        seen_ids.add(image_id)
        source_uri = require_nullable_string(
            image["source_uri"], field_path=f"{field_path}.source_uri", source=source
        )
        dimensions = _read_dimensions(
            image["dimensions"], field_path=f"{field_path}.dimensions", source=source
        )
        images.append({"image_id": image_id, "source_uri": source_uri, "dimensions": dimensions})
    if len(images) != 1:
        raise ProjectFileValidationError(
            f"Project file '{source}' v1 requires exactly one image entry."
        )
    return images


def _require_nullable_string_value(value: object, *, source: Path) -> str | None:
    if value is None or isinstance(value, str):
        return value
    raise ProjectFileValidationError(
        f"Project file '{source}' source_uri mapping failed after validation."
    )


def _read_dimensions(value: object, *, field_path: str, source: Path) -> ImageDimensions:
    dimensions = require_object(value, field_path=field_path, source=source)
    require_exact_fields(
        dimensions,
        expected_fields=DIMENSIONS_FIELDS,
        field_path=field_path,
        source=source,
    )
    try:
        return ImageDimensions(
            width=require_int(dimensions["width"], field_path=f"{field_path}.width", source=source),
            height=require_int(
                dimensions["height"], field_path=f"{field_path}.height", source=source
            ),
        )
    except DomainValidationError as exc:
        raise ProjectFileValidationError(
            f"Project file '{source}' field '{field_path}' has invalid dimensions: {exc}"
        ) from exc


def _read_pipelines(value: object, *, source: Path) -> list[dict[str, object]]:
    pipeline_values = require_array(value, field_path="$.pipelines", source=source)
    pipelines: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for index, pipeline_value in enumerate(pipeline_values):
        field_path = f"$.pipelines[{index}]"
        pipeline = require_object(pipeline_value, field_path=field_path, source=source)
        require_exact_fields(
            pipeline,
            expected_fields=PIPELINE_FIELDS,
            field_path=field_path,
            source=source,
        )
        image_id = require_string(
            pipeline["image_id"], field_path=f"{field_path}.image_id", source=source
        )
        if image_id in seen_ids:
            raise ProjectFileValidationError(
                f"Project file '{source}' contains duplicate pipeline image_id '{image_id}'."
            )
        seen_ids.add(image_id)
        steps = _read_steps(pipeline["steps"], field_path=f"{field_path}.steps", source=source)
        pipelines.append({"image_id": image_id, "pipeline": EnhancementPipeline(steps)})
    if len(pipelines) != 1:
        raise ProjectFileValidationError(
            f"Project file '{source}' v1 requires exactly one pipeline entry."
        )
    return pipelines


def _read_steps(value: object, *, field_path: str, source: Path) -> list[PipelineStep]:
    step_values = require_array(value, field_path=field_path, source=source)
    steps: list[PipelineStep] = []
    seen_ids: set[str] = set()
    for index, step_value in enumerate(step_values):
        step_path = f"{field_path}[{index}]"
        step = require_object(step_value, field_path=step_path, source=source)
        require_exact_fields(step, expected_fields=STEP_FIELDS, field_path=step_path, source=source)
        step_id = require_string(step["step_id"], field_path=f"{step_path}.step_id", source=source)
        if step_id in seen_ids:
            raise ProjectFileValidationError(
                f"Project file '{source}' contains duplicate step_id '{step_id}'."
            )
        seen_ids.add(step_id)
        operation_id = require_string(
            step["operation_id"],
            field_path=f"{step_path}.operation_id",
            source=source,
        )
        parameters = _read_parameters(
            step["parameters"],
            field_path=f"{step_path}.parameters",
            source=source,
        )
        try:
            steps.append(
                PipelineStep(
                    step_id=PipelineStepId(step_id),
                    operation_id=EnhancementOperationId(operation_id),
                    parameters=OperationParameters(parameters),
                )
            )
        except DomainValidationError as exc:
            raise ProjectFileValidationError(
                f"Project file '{source}' field '{step_path}' has invalid pipeline step: {exc}"
            ) from exc
    return steps


def _read_parameters(value: object, *, field_path: str, source: Path) -> dict[str, float]:
    parameters = require_object(value, field_path=field_path, source=source)
    result: dict[str, float] = {}
    for key in sorted(parameters):
        result[key] = require_number(
            parameters[key], field_path=f"{field_path}.{key}", source=source
        )
    return result


def _require_single_image(
    images: list[dict[str, object]],
    *,
    active_image_id: str,
    source: Path,
) -> dict[str, object]:
    image = images[0]
    if image["image_id"] != active_image_id:
        raise ProjectFileValidationError(
            f"Project file '{source}' active_image_id '{active_image_id}' has no matching image."
        )
    return image


def _require_single_pipeline(
    pipelines: list[dict[str, object]],
    *,
    active_image_id: str,
    source: Path,
) -> EnhancementPipeline:
    pipeline = pipelines[0]
    if pipeline["image_id"] != active_image_id:
        raise ProjectFileValidationError(
            f"Project file '{source}' active_image_id '{active_image_id}' has no matching pipeline."
        )
    value = pipeline["pipeline"]
    if not isinstance(value, EnhancementPipeline):
        raise ProjectFileValidationError(
            f"Project file '{source}' pipeline mapping failed for image '{active_image_id}'."
        )
    return value
