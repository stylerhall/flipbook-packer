from pathlib import Path

import fbpack.paths
import fbpack.layout

__all__: list[str] = [
    "example_atlas_layout"
]


def example_atlas_layout() -> Path:
    """
    Example of using the traditional_atlas layout function.

    Returns:
        (Path) The absolute path to the atlas.
    """
    return fbpack.layout.traditional_atlas(rows=6, columns=6, source_path=fbpack.paths.resources_dir.joinpath("Numbers36"))


if __name__ == "__main__":
    example_atlas_layout()
