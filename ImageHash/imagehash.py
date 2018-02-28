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
 
print("Computing hashes for \"source\"...")
haystackPaths = list(paths.list_images(args["source"]))
needlePaths = list(paths.list_images(args["check"]))
 
if sys.platform != "win32":
	haystackPaths = [p.replace("\\", "") for p in haystackPaths]
	needlePaths = [p.replace("\\", "") for p in needlePaths]

BASE_PATHS = set([p.split(os.path.sep)[-2] for p in needlePaths])
haystack = {}

for p in haystackPaths:
	image = cv2.imread(p)
 
	if image is None:
		continue
 
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	imageHash = dhash(image)
 
	l = haystack.get(imageHash, [])
	l.append(p)
	haystack[imageHash] = l

print("Computing hashes for \"check\" images...")

for p in needlePaths:
	image = cv2.imread(p)

	if image is None:
		continue
 
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	imageHash = dhash(image)
 
	matchedPaths = haystack.get(imageHash, [])
 
	for matchedPath in matchedPaths:
		b = p.split(os.path.sep)[-2]

		if b in BASE_PATHS:
			BASE_PATHS.remove(b)

print("Check the following directories...")

for b in BASE_PATHS:
	print("{}".format(b))
