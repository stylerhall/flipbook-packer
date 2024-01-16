__all__: list[str] = [
    "save_format",
    "image_formats"
]

# image format to look for on disk from the seqPath variable.
# image format to save out as. if tif format, you need 2 f"s (ex, "tiff").
save_format: str = "tif"


# supported input image types
image_formats: list[str] = ["tif", "png", "jpg", "jpeg", "tiff", "tga"]
