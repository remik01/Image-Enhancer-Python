from image_workbench import __version__


def test_package_imports_from_src_layout() -> None:
    assert __version__ == "0.1.0"
