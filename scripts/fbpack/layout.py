"""Flipbook Packer Layout
This module contains the functions used to create the various texture atlas layouts.
"""
import math
import logging
from pathlib import Path
from enum import StrEnum
from typing import Optional, Union

from PIL import Image

from fbpack import consts, utils

__all__: list[str] = [
    "traditional_atlas",
    "stagger_packed_atlas",
    "super_packed_atlas"
]


_logger: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PackLayout(StrEnum):
    ATLAS: str = "atlas"
    STAGGER: str = "staggerpack"
    SUPER: str = "superpack"


def traditional_atlas(rows: int, columns: int, source_path: Union[str, Path]) -> Optional[Path]:
    """
    Create a traditional texture atlas from a folder of images.

    Args:
        rows (int): The number of rows in the atlas.
        columns (int): The number of columns in the atlas.
        source_path (Union[str, Path]): The path to the source images.

    Returns:
        (None | Path) The absolute path to the atlas if created. None if no images found.
    """
    images: list[Path] = utils.get_images(source_path)

    if len(images) < 1:
        _logger.error(f"no images in folder to {PackLayout.ATLAS.value} layout")
        raise ValueError(f"no images in folder to {PackLayout.ATLAS.value} layout")

    # set the export path and create if it doesn't exist
    export_path: Path = images[0].parent.joinpath("fbpack")
    export_path.mkdir(exist_ok=True)

    # set the output file and remove if it exists
    output_file: Path = export_path.joinpath(f"{PackLayout.ATLAS.value}_{utils.get_filename_stem(images[0])}.{consts.save_format}")
    output_file.unlink(missing_ok=True)

    # load the first image then determine the width and height
    width: int
    height: int
    with Image.open(images[0], "r") as first_image:
        width, height = first_image.size
        channel_mode: str = first_image.mode
        resolution: tuple[int, int] = (width * columns, height * rows)

    # prime the image we"ll be pasting the frames into
    # if the first image has an alpha channel, we need to use RGBX
    # otherwise, we fall back to RGB
    new_image: Image = Image.new(channel_mode, resolution)

    # iterate over all the images and paste each frame into the correct row and column
    for i, image in enumerate(images):
        # get frame position
        row: int = math.floor(i / rows)
        column: int = i % columns
        frame_top: int = row * height
        frame_left: int = column * width

        with Image.open(image, "r") as current_image:
            # paste the current image into the row/column cell
            new_image.paste(current_image, (frame_left, frame_top))

            if channel_mode == "RGBX":
                # merge in the alpha channel if the image has one
                new_image = Image.merge(channel_mode, list(current_image.split()))

            if consts.save_format == "tif":
                new_image.save(output_file, "tiff", compression="tiff_lzw")
                continue

        # save the image with the pasted frame
        new_image.save(output_file, consts.save_format)

    _logger.info(f"atlas created: {output_file}")
    return output_file


def stagger_packed_atlas(source_path: Union[str, Path]) -> Path:
    """
    Create a stagger packed texture atlas from a folder of images. This layout is used for 192 or 256 frame sequences.
    Using this texture atlas layout requires a custom material which can unpack the texture over time.

    The layout is as follows:
        -   Red channel frames: 01, 05, 09, 13, 17, 21, 25, 29, 33, 37, etc.
        - Green channel frames: 02, 06, 10, 14, 18, 22, 26, 30, 34, 38, etc.
        -  Blue channel frames: 03, 07, 11, 15, 19, 23, 27, 31, 35, 39, etc.
        - Alpha channel frames: 04, 08, 12, 16, 20, 24, 28, 32, 36, 40, etc.

    Args:
        source_path (Union[str, Path]): The path to the source images.

    Returns:
        (str) The absolute path to the atlas.
    """
    images: list[Path] = utils.get_images(source_path)

    # if we're not working with 192 or 256 frames, early out
    if len(images) not in [192, 256]:
        _logger.error("super packing requires either 192 for RGB or 256 frames for RGBA packing.")
        raise ValueError("super packing requires either 192 for RGB or 256 frames for RGBA packing.")

    # set the export path and create if it doesn't exist
    export_path: Path = images[0].parent.joinpath("fbpack")
    export_path.mkdir(exist_ok=True)

    # set the output file and remove if it exists
    output_file: Path = export_path.joinpath(f"{PackLayout.STAGGER.value}_{utils.get_filename_stem(images[0])}.{consts.save_format}")
    output_file.unlink(missing_ok=True)

    # declare the new image width and height
    width: int
    height: int
    with Image.open(images[0], "r") as first_image:
        width, height = first_image.size

    channel_mode: str = "RGB" if len(images) < 256 else "RGBX"
    channel_count: int = len(channel_mode)

    total_frames: int = int(len(images) / channel_count)
    square_frame: int = int(math.sqrt(total_frames))

    resolution: tuple[int, int] = (width * square_frame, height * square_frame)

    # prime the image we"ll be pasting the frames into
    # if the first image has an alpha channel, we need to use RGBX
    # otherwise, we fall back to RGB
    packed_image: Image = Image.new(channel_mode, resolution)

    # if we have an alpha channel we need to create a separate image
    # to store the frame in. we'll then merge the red channel of this
    # image into the alpha channel of our packed image
    alpha_frame: Optional[Image] = None if channel_count < 4 else Image.new(channel_mode, resolution)

    # loop through all of our images, re: 192 or 256
    # we only want to process every 4th image, so we use the channel count
    # to determine if we should process the image or not
    for i in range(len(images)):
        if i % channel_count != 0:
            continue

        # get the frame position in the atlas
        row: int = math.floor(i / (square_frame * channel_count))
        column: int = int((i / channel_count) % square_frame)
        frame_coords: tuple[int, int] = (column * width, row * height)

        # instantiates a new list object where we'll store the image channel bands
        # we use this to channel pack each frame into the correct channel
        final_frame: list[Image] = []

        # each channel of the image contains 3 to 4 frames depending on frame count.
        # we will load each image paste it into the correct channel
        for x in range(channel_count):
            # load the current frame
            with Image.open(images[i+x], "r") as current_frame:
                packed_image.paste(current_frame, frame_coords)

                packed_image: Image = alpha_frame if x > 2 else packed_image
                packed_image.paste(current_frame, frame_coords)

                image_channels: tuple[Image, ...] = packed_image.split()

            # determine which channel we're working with
            # 0 = red, 1 = green, 2 = blue, 3 = alpha
            channel: int = x % channel_count

            # generate the image channel bands
            if channel < 1:
                # red channel
                final_frame.append(image_channels[0])

            elif channel == 1:
                # green channel
                final_frame.append(image_channels[1])

            elif channel == 2:
                # blue channel
                final_frame.append(image_channels[2])

            else:
                # alpha channel
                # NOTE, we need to use index 0 of the channel split here
                # we're creating a new custom alpha image explicitly for
                # this, therefore we need the red channel of this image,
                # not the alpha channel.
                final_frame.append(image_channels[0])

        # merge the final frame channel bands into our packed image
        packed_image = Image.merge(channel_mode, final_frame)
        packed_image.save(output_file, "tiff", compression="tiff_lzw")

    _logger.info(f"{len(images)} frame stagger packed atlas created: {output_file}")
    return output_file


def super_packed_atlas(source_path: Union[str, Path]) -> Path:
    """
    Create a super packed texture atlas from a folder of images.

    The layout is as follows:
        -   Red channel frames: 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, etc.
        - Green channel frames: 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, etc.
        -  Blue channel frames: 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, etc.
        - Alpha channel frames: 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, etc.

    Args:
        source_path (Union[str, Path]): The path to the source images.

    Returns:
        (str) The absolute path to the atlas.
    """
    images: list[Path] = utils.get_images(source_path)

    # if we're not working with 192 or 256 frames, early out
    if len(images) not in [192, 256]:
        _logger.error("super packing requires either 192 for RGB or 256 frames for RGBA packing.")
        raise ValueError("super packing requires either 192 for RGB or 256 frames for RGBA packing.")

    # set the export path and create if it doesn't exist
    export_path: Path = images[0].parent.joinpath("fbpack")
    export_path.mkdir(exist_ok=True)

    # set the output file and remove if it exists
    output_file: Path = export_path.joinpath(f"{PackLayout.SUPER.value}_{utils.get_filename_stem(images[0])}.{consts.save_format}")
    output_file.unlink(missing_ok=True)

    # declare the new image width and height
    width: int
    height: int
    with Image.open(images[0], "r") as first_image:
        width, height = first_image.size

        if len(images) < 256:
            channel_mode: str = 'RGB'
        else:
            channel_mode: str = "RGBX"

        channel_count: int = len(channel_mode)

        total_frames: int = int(len(images) / channel_count)
        square_frame: int = int(math.sqrt(total_frames))
        resolution: tuple[int, int] = (width * square_frame, height * square_frame)

    # prime the image we"ll be pasting the frames into
    # if the first image has an alpha channel, we need to use RGBX
    # otherwise, we fall back to RGB
    packed_image: Image = Image.new(channel_mode, resolution)

    red: Optional[Image] = None
    green: Optional[Image] = None
    blue: Optional[Image] = None
    alpha: Optional[Image] = None

    # we increment this at the end of the total_frames loop
    # this helps us track which frame number we're on
    frame_num: int = 0

    for i in range(channel_count):
        # loop over each channel

        for x in range(total_frames):
            # loop over each frame for said channel
            row: int = math.floor(x / square_frame)
            column: int = x % square_frame
            coords: tuple[int, int] = (column * width, row * height)

            with Image.open(source_path.joinpath(images[frame_num]), mode='r') as current_frame:
                packed_image.paste(current_frame, coords)
                image_channels: tuple[Image, ...] = packed_image.split()

            # determine which channel we're working with
            # 0 = red, 1 = green, 2 = blue, 3 = alpha
            channel: int = i % channel_count

            if channel < 1:
                red: Image = image_channels[0]

            elif channel == 1:
                green: Image = image_channels[1]

            elif channel == 2:
                blue: Image = image_channels[2]

            else:
                alpha: Image = image_channels[0]

            frame_num += 1

    if channel_count > 3:
        packed_image = Image.merge(channel_mode, (red, green, blue, alpha))
    else:
        packed_image = Image.merge(channel_mode, (red, green, blue))

    packed_image.save(output_file, "tiff", compression="tiff_lzw")

    _logger.info(f"{len(images)} frame super packed atlas created: {output_file}")
    return output_file
