# Flipbook Packer
Python tool for VFX artists to aide in different methods of texture atlas'ing and channel packing.

Current methods are your default full RGB(A) flipbook tiled for VFX playback. There are curently 2 other methods outlined in the script. Super Packing and Stagger Packing.

Super Packing and Stagger Packing both allow you to pack a minimum of 192 frames across the RGB channels or 256 frames across the RGBA channels. The way the images are packed into the channels are what makes them different.

Super Packing:
This method is easier to unpack in the shader although compression will suffer because the pixels among the RGBA channels will be very different.
Source Image 1-64    = TextureAtlas.R
Source Image 65-128  = TextureAtlas.G
Source Image 129-192 = TextureAtlas.B
Source Image 193-256 = TextureAtlas.A

Stagger Packing:
This method is a tad more expensive to unpack in the shader but will offer cleaner compression. Since the RGBA channels are the next 4 frames in your sequence, the pixels are closer matched which will help compression.
SourceImage 1-4   = TextureAtlas.001.RGBA
SourceImage 5-8   = TextureAtlas.002.RGBA
SourceImage 9-12  = TextureAtlas.003.RGBA
SourceImage 13-16 = TextureAtlas.004.RGBA
Etc, ...
