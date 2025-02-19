import numpy as np
import cv2
from keras.preprocessing import image
import timeit
import os
import fnmatch
import csv




# open the file in the write mode
f = open('ABC.csv', 'w', encoding='UTF8', newline='')

# create the csv writer
writer = csv.writer(f)

#-----------------------------
#opencv initialization

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#cap = cv2.VideoCapture(0)
#-----------------------------
#face expression recognizer initialization
from keras.models import model_from_json
model = model_from_json(open("facial_expression_model_structure.json", "r").read())
model.load_weights('facial_expression_model_weights.h5') #load weights

#-----------------------------

emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')


total_time = 0.0
content_path = "Test-Copy"
with os.scandir(content_path) as listOfEntries:
		for entry in listOfEntries:
			if fnmatch.fnmatch(entry.name, '*.db') == False:
				fileName = entry.name
				#print(fileName)
				filename_tuple = os.path.splitext(fileName)
				contentfileName = filename_tuple[0]
				#print("we are using this content:", contentfileName)
				content_image_path = content_path+"/"+entry.name
				img = cv2.imread(content_image_path)
				gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				faces = face_cascade.detectMultiScale(gray, 1.3, 5)
				for (x,y,w,h) in faces:
					cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) #draw rectangle to main image
					detected_face = img[int(y):int(y+h), int(x):int(x+w)] #crop detected face
					detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
					detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48
		
					img_pixels = image.img_to_array(detected_face)
					img_pixels = np.expand_dims(img_pixels, axis = 0)
		
					img_pixels /= 255 #pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]
					start = timeit.default_timer()
					predictions = model.predict(img_pixels) #store probabilities of 7 expressions
					stop = timeit.default_timer()
					time = stop - start
					total_time = total_time + time
					#find max indexed array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral
					max_index = np.argmax(predictions[0])
		
					emotion = emotions[max_index]
					print(emotion)
					print('Time: ', stop - start)
					row = contentfileName, emotion, time
					writer.writerow(row)
print("Total time in sec:", total_time)
if total_time > 60:
	total_time = total_time/60
Frow = ("Total time is: ",total_time)
writer.writerow(Frow)
print("Total time is: ",total_time)

f.close()










	
