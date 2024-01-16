from pathlib import Path
from typing import Union

from PIL import Image

from fbpack import consts

__all__: list[str] = [
    "get_filename_stem",
    "compare_image_size",
    "get_images"
]


def get_filename_stem(filename: Union[str, Path]) -> str:
    """
    Get the filename stem from the given filename.

    Args:
        filename (Union[str, Path]): The filename to get the stem from.

    Returns:
        (str) The filename stem.
    """
    filename: Path = Path(filename) if isinstance(filename, str) else filename
    return filename.stem.split(".")[0]


def compare_image_size(filename: Union[str, Path], resolution: tuple[int, int]) -> bool:
    """
    Compare the size of an image to the given width and height.

    Args:
        filename (Union[str, Path]): The path to the image file.
        resolution (tuple[int, int]): The width and height to compare against.

    Returns:
        (bool) True if the image size matches the given width and height.
    """
    filename: Path = Path(filename) if isinstance(filename, str) else filename
    width, height = resolution

    with Image.open(filename, "r") as file:
        w, h = file.size
        return w == width and h == height


def get_images(path: Union[str, Path]) -> list[Path]:
    """
    Get a list of all image files in the given path.

    Args:
        path (Union[str, Path]): The path to the image files.

    Returns:
        (list[Path]) A list of all image files in the given path.
    """
    path: Path = Path(path) if isinstance(path, str) else path

    # use a set to prevent duplicates
    files: set[Path] = set()
    [files.update(path.glob(f"*.{image_type}")) for image_type in consts.image_formats]

    # convert the set and sort it
    output: list[Path] = list(files)
    output.sort()

    return output
