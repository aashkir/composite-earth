import pygame
import io
import os
import sys
from urllib.request import urlopen
import json

def main():
	path = os.path.dirname(sys.argv[0])
	if len(sys.argv) > 1:
		if sys.argv[1] == 'rename':
			print("Renaming files...")
			renameEarths(path)
			sys.exit()


	timeStampsUrl = urlopen("http://rammb-slider.cira.colostate.edu/data/json/goes-16/full_disk/geocolor/latest_times.json")
	# provides the last 100 satellite-times of earth (24 hours), in 15 min intervals in UTC time (delayed by 30 min.) 8:30 EST to grab another day	
	latestTimeStamps = json.loads(timeStampsUrl.read())
	totalTimeStampEntries = len(latestTimeStamps['timestamps_int'])
	totalImages = totalTimeStampEntries + getImageCount(path)

	surface = pygame.display.set_mode((1356, 1356))

	for i in range(totalTimeStampEntries - 1, -1, -1):
		assembleImage(str(latestTimeStamps['timestamps_int'][i]), surface, totalImages, i)
		print(int(((totalTimeStampEntries - i)/totalTimeStampEntries) * 100), "% Completed")

def assembleImage(timestamp, finalImage, totalImages, i):
	dim = 1356
	dateOnly = timestamp[:8]

	imgStr = urlopen("http://rammb-slider.cira.colostate.edu/data/imagery/" + dateOnly + "/goes-16---full_disk/geocolor/" + timestamp + "/01/000_000.png").read()
	imgFile = io.BytesIO(imgStr)
	topLeft = pygame.image.load(imgFile)

	imgStr = urlopen("http://rammb-slider.cira.colostate.edu/data/imagery/" + dateOnly + "/goes-16---full_disk/geocolor/" + timestamp + "/01/000_001.png").read()
	imgFile = io.BytesIO(imgStr)
	topRight = pygame.image.load(imgFile)

	imgStr = urlopen("http://rammb-slider.cira.colostate.edu/data/imagery/" + dateOnly + "/goes-16---full_disk/geocolor/" + timestamp + "/01/001_000.png").read()
	imgFile = io.BytesIO(imgStr)
	bottomLeft = pygame.image.load(imgFile)

	imgStr = urlopen("http://rammb-slider.cira.colostate.edu/data/imagery/" + dateOnly + "/goes-16---full_disk/geocolor/" + timestamp + "/01/001_001.png").read()
	imgFile = io.BytesIO(imgStr)
	bottomRight = pygame.image.load(imgFile)
	# Used to create the Earth
	finalImage.blit(topLeft, (0, 0))
	finalImage.blit(topRight, (678, 0))
	finalImage.blit(bottomLeft, (0, 678))
	finalImage.blit(bottomRight, (678, 678))
	pygame.image.save(finalImage, 'Earth_' + '{:04d}'.format(totalImages - i) + ".jpg")

def renameEarths(path):
	files = os.listdir(path)
	i = 1
	for file in files:
		if file.endswith(".jpg"):
			os.rename(os.path.join(path, file), os.path.join(path, 'Earth_' + '{:04d}'.format(i) + '.jpg'))
			i = i + 1

def getImageCount(path):
	files = os.listdir(path)
	i = 0
	for file in files:
		if file.endswith(".jpg"):
			i = i + 1
	return i

pygame.init()
main()
