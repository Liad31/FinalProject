# Import required packages
import cv2
import pytesseract
import sys
from moviepy.editor import *


# def text_from_video(path, videoID):
# 	def extract_middle_frame():
# 		# loading video gfg
# 		clip = VideoFileClip("../../Downloads/6752101886431595782.mp4")
#
#
# 		# getting duration of the video
# 		duration = clip.duration
#
# 		# saving a frame at 1 second
# 		clip.save_frame("frame.png", int(duration/2))
#
# 		# showing clip
# 		clip.ipython_display(width = 360)
#
# 	# Read image from which text needs to be extracted
# 	extract_middle_frame()
#
# 	img = cv2.imread('frame.png')
#
# 	# Preprocessing the image starts
#
# 	# Convert the image to gray scale
# 	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# 	# Performing OTSU threshold
# 	ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
#
# 	# Specify structure shape and kernel size.
# 	# Kernel size increases or decreases the area
# 	# of the rectangle to be detected.
# 	# A smaller value like (10, 10) will detect
# 	# each word instead of a sentence.
# 	rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
#
# 	# Applying dilation on the threshold image
# 	dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
#
# 	# Finding contours
# 	contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
# 													cv2.CHAIN_APPROX_NONE)
#
# 	# Creating a copy of image
# 	im2 = img.copy()
#
# 	# A text file is created and flushed
# 	file = open("recognized.txt", "w+")
# 	file.write("")
# 	file.close()
#
# 	# Looping through the identified contours
# 	# Then rectangular part is cropped and passed on
# 	# to pytesseract for extracting text from it
# 	# Extracted text is then written into the text file
# 	for cnt in contours:
# 		x, y, w, h = cv2.boundingRect(cnt)
#
# 		# Drawing a rectangle on copied image
# 		rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
# 		# Cropping the text block for giving input to OCR
# 		cropped = im2[y:y + h, x:x + w]
#
# 		# Open the file in append mode
# 		file = open("recognized.txt", "a")
#
# 		# Apply OCR on the cropped image
# 		text = pytesseract.image_to_string(cropped, lang='ara')
#
# 		# Appending the text into file
# 		file.write(text)
# 		file.write("\n")
#
# 		# Close the file
# 		file.close
#
# 	with open('recognized.txt', 'w+') as file:
# 		for line in file:
# 			if not line.isspace():
# 				file.write(line)
# 	with open('recognized.txt', 'r') as file:
# 		text = file.read()
#
# 	return text


# text_from_video(1,1)

from ArabicOcr import arabicocr

def text_from_video(path):
	def extract_middle_frame(path):
		# loading video gfg
		clip = VideoFileClip(path)


		# getting duration of the video
		duration = clip.duration

		# saving a frame at 1 second
		clip.save_frame("frame.png", int(duration/2))

		# showing clip
		clip.ipython_display(width = 360)

	extract_middle_frame(path)
	image_path="frame.png"
	out_image='out.jpg'
	results=arabicocr.arabic_ocr(image_path,out_image)
	words=[]
	for i in range(len(results)):
			word=results[i][1]
			words.append(word)
	return ' '.join(words)




