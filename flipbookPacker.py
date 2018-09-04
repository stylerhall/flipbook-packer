'''
08/2018
Flipbook Packer

Written by Seth Hall
seth@pixill.com
https://www.pixill.com

Set the execution variables.
Uncomment the def you want to use then execute the script.

Stagger Packing and Super Packing both expect a total image
sequence on disk of 64 frames. This will give you a final
image of 8x8 rows and columns.

Super Packing if using 192 or 256 total frames:
	* Alpha channel is packed if you are using 256
	Frame[1-64].R
	Frame[65-128].G
	Frame[129-192].B
	Frame[193-256].A

Stagger Packing if using 192 or 256 frames:
	* Alpha channel is packed if you are using 256
	Frame[1-4] = Image001.RGBA
	Frame[5-8] = Image002.RGBA
	Frame[9-12] = Image003.RGBA
	Frame[13-16] = Image004.RGBA
'''

import PIL
from PIL import Image
import math
import os

#
# execution variables start

seqPath = 'C:/img/' 	# path to your image sequence on disk.
imgFormat = 'tif'		# image format to look for on disk from the seqPath variable.
pilFormat = 'tiff'		# image format to save out as. if tif format, you need 2 f's (ex, 'tiff').
compress = 'tiff_lzw'	# tif compression if using tif format.
atlasRow = 6 			# total texture atlas columns. only used for atlasLayout().
atlasCol = 6			# total texture atlas rows. only used for atlasLayout().

if pilFormat == 'tiff':
	saveFormat = 'tif'
else:
	saveFormat = pilFormat

# execution variables end
#

def compareDimension(image, imPath, width, height):
	img = Image.open(imPath + image)
	w, h = img.size

	if w == width and h == height:
		return True
	elif w != width or h != height:
		return False

def getImages(images, imPath, width, height):
	catch = []
	for file in images:
		if file.endswith(imgFormat):
			check = compareDimension(file, imPath, width, height)

			if check == True:
				catch.append(file)

	return catch

def atlasLayout(row, col, imPath):
	images = os.listdir(imPath)

	if len(images) < 1:
		print('No images in folder to Atlas Layout')
	else:
		name = images[0].split('.')
		exportPath = imPath + '_texture/'
		atlasTex = exportPath + 'atlas_' + name[0] + '.' + saveFormat

		if os.path.exists(exportPath) == False:
			os.makedirs(exportPath)

		# load the first image then determine the width and height
		img = Image.open(imPath + images[0], 'r')
		w, h = img.size
		hasAlpha = img.mode == 'RGBX'
		dimensions = [w * row, h * col]

		if hasAlpha == True:
			newImg = Image.new('RGBX', dimensions)
		elif hasAlpha == False:
			newImg = Image.new('RGB', dimensions)

		# lets loop through the images to make sure we're only getting the format we want
		# and to check and ensure the images are all the same width and height
		imagesToProcess = getImages(images, imPath, w, h)

		for i in range(len(imagesToProcess)):
			currCol = i % row
			currRow = math.floor(i / row)
			leftPixel = currCol * w
			topPixel = currRow * h

			currentImg = Image.open(imPath + imagesToProcess[i])

			if hasAlpha == True:
				newImg.paste(currentImg, (leftPixel, topPixel))

				r, g, b, a = currentImg.split()
				
				newAlphaImg = Image.merge('RGBX', (r, g, b, a))
			elif hasAlpha == False:
				newImg.paste(currentImg, (leftPixel, topPixel))

		if pilFormat == 'tiff':
			newImg.save(atlasTex, pilFormat, compression=compress)
		else:
			newImg.save(atlasTex, pilFormat)

		print(atlasTex)

def staggerPack(imPath):
	images = os.listdir(imPath)

	if len(images) < 1:
		print('No images in folder to Stagger Pack')
	else:
		name = images[0].split('.')
		exportPath = imPath + '_texture/'
		atlasTex = imPath + '_texture/staggerPack_' + name[0] + '.' + saveFormat

		img = Image.open(imPath + images[0])
		w, h = img.size

		imagesToProcess = getImages(images, imPath, w, h)

		if len(imagesToProcess) != 192 and len(imagesToProcess) != 256:
			print('Super Packing requires sequences of 192 for RGB or 256 for RGBA packing.')
		else:
			if os.path.exists(exportPath) == False:
				os.makedirs(exportPath)

			channelsToPack = 3
			channels = 'RGB'

			if len(imagesToProcess) == 256:
				channels = 'RGBX'
				channelsToPack = 4

			atlasFrames = int(len(imagesToProcess) / channelsToPack)
			square = int(math.sqrt(atlasFrames))

			dimensions = [w * square, h * square]

			newImg = Image.new(channels, dimensions)
			tempAlphaImg = Image.new(channels, dimensions)

			if channelsToPack == 4:
				r, g, b, a = newImg.split()
			elif channelsToPack == 3:
				r, g, b = newImg.split()

			if channelsToPack == 4:
				newAlphaImg = Image.new(channels, dimensions)

			# loop through all of our images, re: 192 or 256
			for i in range(len(imagesToProcess)):
				row = math.floor(i / (square * channelsToPack))

				if i % channelsToPack == 0:
					column = int((i / channelsToPack) % square)

					leftPixel = column * w
					topPixel = row * h

					for x in range(channelsToPack):
						if x % channelsToPack == 0:
							redImg = Image.open(imPath + imagesToProcess[i], mode='r')
							newImg.paste(redImg, (leftPixel, topPixel))

							if channelsToPack == 4:
								rr, rg, rb, ra = newImg.split()
							elif channelsToPack == 3:
								rr, rg, rb = newImg.split()

						if x % channelsToPack == 1:
							blueImg = Image.open(imPath + imagesToProcess[i+1], mode='r')
							newImg.paste(blueImg, (leftPixel, topPixel))

							if channelsToPack == 4:
								gr, gg, gb, ga = newImg.split()
							elif channelsToPack == 3:
								gr, gg, gb = newImg.split()

						if x % channelsToPack == 2:
							greenImg = Image.open(imPath + imagesToProcess[i+2], mode='r')
							newImg.paste(greenImg, (leftPixel, topPixel))

							if channelsToPack == 4:
								br, bg, bb, ba = newImg.split()
							elif channelsToPack == 3:
								br, bg, bb = newImg.split()

						if x % channelsToPack == 3:
							alphaImg = Image.open(imPath + imagesToProcess[i+3], mode='r')
							tempAlphaImg.paste(alphaImg, (leftPixel, topPixel))

							ar, ag, ab, aa = tempAlphaImg.split()

					if channelsToPack == 4:
						newImg = Image.merge(channels, (rr, gg, bb, ar))
					elif channelsToPack == 3:
						newImg = Image.merge(channels, (rr, gg, bb))

			if pilFormat == 'tiff':
				newImg.save(atlasTex, pilFormat, compression=compress)
			else:
				newImg.save(atlasTex, pilFormat)

			print(atlasTex)

def superPack(imPath):
	images = os.listdir(imPath)

	if len(images) < 1:
		print('No images in folder to Super Pack')
	else:
		name = images[0].split('.')
		exportPath = imPath + '_texture/'
		atlasTex = imPath + '_texture/superPack_' + name[0] + '.' + saveFormat

		img = Image.open(imPath + images[0])
		w, h = img.size

		imagesToProcess = getImages(images, imPath, w, h)

		if len(imagesToProcess) != 192 and len(imagesToProcess) != 256:
			print('Super Packing requires sequences of 192 for RGB or 256 for RGBA packing.')
		else:
			if os.path.exists(exportPath) == False:
				os.makedirs(exportPath)

			channelsToPack = 3
			channels = 'RGB'

			if len(imagesToProcess) == 256:
				channels = 'RGBX'
				channelsToPack = 4

			atlasFrames = int(len(imagesToProcess) / channelsToPack)
			square = int(math.sqrt(atlasFrames))

			dimensions = [w * square, h * square]

			if channelsToPack == 4:
				newImg = Image.new(channels, dimensions)
				r, g, b, a = newImg.split()
			elif channelsToPack == 3:
				newImg = Image.new(channels, dimensions)
				r, g, b = newImg.split()

			if channelsToPack == 4:
				tempAlphaImg = Image.new(channels, dimensions)

			# loop through all of our images, re: 192 or 256
			imgCount = int(0)
			for i in range(channelsToPack):
				for x in range(atlasFrames):
					col = x % square
					row = math.floor(x / square)

					leftPixel = col * w
					topPixel = row * h

					if i % channelsToPack == 0:
						redImg = Image.open(imPath + imagesToProcess[imgCount], mode='r')
						newImg.paste(redImg, (leftPixel, topPixel))

						if channelsToPack == 4:
							rr, rg, rb, ra = newImg.split()
						elif channelsToPack == 3:
							rr, rg, rb = newImg.split()

					elif i % channelsToPack == 1:
						blueImg = Image.open(imPath + imagesToProcess[imgCount], mode='r')
						newImg.paste(blueImg, (leftPixel, topPixel))

						if channelsToPack == 4:
							gr, gg, gb, ga = newImg.split()
						elif channelsToPack == 3:
							gr, gg, gb = newImg.split()

					elif i % channelsToPack == 2:
						greenImg = Image.open(imPath + imagesToProcess[imgCount], mode='r')
						newImg.paste(greenImg, (leftPixel, topPixel))

						if channelsToPack == 4:
							br, bg, bb, ba = newImg.split()
						elif channelsToPack == 3:
							br, bg, bb = newImg.split()

					if channelsToPack == 4:
						if i % channelsToPack == 3:
							alphaImg = Image.open(imPath + imagesToProcess[imgCount], mode='r')
							tempAlphaImg.paste(alphaImg, (leftPixel, topPixel))

							ar, ag, ab, aa = tempAlphaImg.split()

					imgCount = imgCount + 1

			if channelsToPack == 4:
				newImg = Image.merge('RGBX', (rr, gg, bb, ar))
			elif channelsToPack == 3:
				newImg = Image.merge('RGB', (rr, gg, bb))
			
			if pilFormat == 'tiff':
				newImg.save(atlasTex, pilFormat, compression=compress)
			else:
				newImg.save(atlasTex, pilFormat)

			print(atlasTex)

#
# Uncomment out the packing function you wish to use

atlasLayout(atlasRow, atlasCol, seqPath)

#staggerPack(seqPath)

#superPack(seqPath)
