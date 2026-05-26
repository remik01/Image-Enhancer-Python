# Lightweight Observability Templates

Use these snippets when a generated phase introduces lightweight runtime observability without Prometheus, Grafana, tracing, alerting, Docker Compose, or cloud monitoring.

## Boundary Rules

Keep observability at runtime and adapter boundaries:

* Bootstrap or runtime modules may register lifecycle, startup, readiness, and configuration-safe metrics.
* API adapters may rely on framework-provided request metrics and may add bounded outcome metrics when useful.
* CLI adapters may emit bounded diagnostics and structured exit/status summaries.
* Domain types must not import observability, metrics, web framework, or logging APIs.
* Application services should expose semantic results that adapters can translate into diagnostics.

## Local Metrics Or Health Template

When a project already has a framework, use its existing health or metrics extension point. Otherwise, prefer a small project-owned boundary abstraction rather than adding a metrics dependency casually.

Example lightweight protocol:

```python
from typing import Protocol


class RuntimeCounter(Protocol):
    """Records bounded runtime events without coupling core logic to a metrics backend."""

    def increment(self, name: str, tags: dict[str, str] | None = None) -> None:
        """Record one event with low-cardinality tags."""
```

Keep metric names project-prefixed and tags stable:

* Good: `example.runtime.startups`, `example.import.completed`
* Avoid: request ids, usernames, file paths containing secrets, tokens, connection strings, or free-form exception messages.

## Test Template

```python
class RecordingCounter:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, str]]] = []

    def increment(self, name: str, tags: dict[str, str] | None = None) -> None:
        self.events.append((name, tags or {}))


def test_runtime_counter_records_startup() -> None:
    counter = RecordingCounter()
    counter.increment("example.runtime.startups", {"outcome": "success"})

    assert counter.events == [
        ("example.runtime.startups", {"outcome": "success"}),
    ]
```

Adapt names and boundaries to the repository. Tests should assert the project-owned behavior, not a vendor-specific implementation unless that dependency is already accepted.

## Acceptance Criteria Template

* Runtime or adapter boundary owns observability behavior; domain and application models do not import metrics, web framework, or logging APIs.
* Metric names are project-prefixed and low-cardinality.
* Tags avoid request ids, usernames, tokens, secrets, raw paths, connection strings, and free-form messages.
* Tests assert metric, health-check, or diagnostic behavior through the selected boundary.
* README or operations documentation states that metrics are local lightweight observability and that Prometheus/Grafana are not part of the current baseline.
* No Prometheus client, Grafana dashboard, scrape configuration, alerting rule, Docker Compose topology, or cloud monitoring dependency is introduced without explicit acceptance.
* Decision log records the local observability convention; ADR discussion is required only if exporters, dashboards, tracing, alerting, or production observability ownership are introduced.
