from pathlib import Path

import fbpack.paths
import fbpack.layout

__all__: list[str] = [
    "example_staggerpack_192",
    "example_staggerpack_256"
]


def example_staggerpack_192() -> Path:
    """
    Example of using the 192 frame stagger pack layout.

    Returns:
        (Path) The absolute path to the atlas.
    """
    return fbpack.layout.stagger_packed_atlas(fbpack.paths.resources_dir.joinpath("Numbers192"))


def example_staggerpack_256() -> Path:
    """
    Example of using the 256 frame stagger pack layout.

    Returns:
        (Path) The absolute path to the atlas.
    """
    return fbpack.layout.stagger_packed_atlas(fbpack.paths.resources_dir.joinpath("Numbers256"))


if __name__ == "__main__":
    # example_staggerpack_192()
    example_staggerpack_256()
