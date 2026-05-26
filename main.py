"""Development entry point for the scaffolded package.

The real product entry points are owned by later UI, API, CLI, or bootstrap
phases. This module only verifies that the package scaffold imports.
"""

from image_workbench import __version__


def main() -> int:
    """Return success after proving the scaffolded package is importable."""
    print(f"image-workbench {__version__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
