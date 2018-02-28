from imutils import paths
import argparse
import sys
import cv2
import os

def dhash(image, hashSize=8):

	resized = cv2.resize(image, (hashSize + 1, hashSize))
	diff = resized[:, 1:] > resized[:, :-1]

	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True,
	help="dataset of images to search through ")
ap.add_argument("-c", "--check", required=True,
	help="set of images we are searching for ")
args = vars(ap.parse_args())
 
print("Computing hashes for \"source\" images...")
sourcePath = list(paths.list_images(args["source"]))
checkPath = list(paths.list_images(args["check"]))
 
if sys.platform != "win32":
	sourcePath = [p.replace("\\", "") for p in sourcePath]
	checkPath = [p.replace("\\", "") for p in checkPath]

BASE_PATHS = set([p.split(os.path.sep)[-2] for p in checkPath])
image_source = {}

for p in sourcePath:
	image = cv2.imread(p)
 
	if image is None:
		continue
 
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	imageHash = dhash(image)
 
	l = image_source.get(imageHash, [])
	l.append(p)
	image_source[imageHash] = l

print("Computing hashes for \"check\" images...")

for p in checkPath:
	image = cv2.imread(p)

	if image is None:
		continue
 
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	imageHash = dhash(image)
 
	matchedPaths = image_source.get(imageHash, [])
 
	for matchedPath in matchedPaths:
		b = p.split(os.path.sep)[-2]

		if b in BASE_PATHS:
			BASE_PATHS.remove(b)

print("Check the following images...")

for b in BASE_PATHS:
	print("{}".format(b))
