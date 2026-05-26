"""Bootstrap layer for runtime wiring and lifecycle ownership.

Bootstrap may assemble dependencies across layers, validate configuration, and
own startup or shutdown concerns. It must not become a home for business rules.
"""
