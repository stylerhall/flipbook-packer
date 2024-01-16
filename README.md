Flipbook Packer
===

Python tool for VFX artists to aid in different methods of texture flipbook atlasing.

Current methods are your default full RGB(A) flipbook tiled for VFX playback. There are currently 3 flavors of packing; _Atlas_, _Super_, and _Stagger_.

Super Packing and Stagger Packing both allow you to pack a minimum of 192 frames across the RGB channels or 256 frames across the RGBA channels. The way the images are packed into the channels are what makes them different.

---

# Command Line Usage

Under the `bin` folder there are 3 `bat` files that will help you create the desired flipbook layout via the command line.

## Atlas Layout

After the `atlas_pack.bat` filename, the first int arg is the rows, then the columns, and finally the path to the images you want to pack.

    atlas_pack.bat 6 6 "c:\path\to\images"

## Stagger Packed Layout

After the `stagger_pack.bat` filename, the only required argument is the path to the images you want to pack. Note, that in order to pack this type of atlas you must have either `192` or `256` images.

    stagger_pack.bat "c:\path\to\images"

The final atlas is laid out as such:

- SourceImage 1-4   = TextureAtlas.001.RGBA
- SourceImage 5-8   = TextureAtlas.002.RGBA
- SourceImage 9-12  = TextureAtlas.003.RGBA
- SourceImage 13-16 = TextureAtlas.004.RGBA

## Super Packed Layout

After the `super_pack.bat` filename, the only required argument is the path to the images you want to pack. Note, that in order to pack this type of atlas you must have either `192` or `256` images.

    super_pack .bat "c:\path\to\images"

The final atlas is laid out as such:

- Source Image 1-64    = TextureAtlas.R
- Source Image 65-128  = TextureAtlas.G
- Source Image 129-192 = TextureAtlas.B
- Source Image 193-256 = TextureAtlas.A

---

# Examples

Under the examples module you will find a few examples of how to call the flipbook packing methods from within your own python scripts.