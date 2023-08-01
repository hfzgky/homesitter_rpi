
import time
from subprocess import call
import picamera
import json
import pyrebase
from firebase import firebase
import datetime

config={
    "apiKey": "AIzaSyBaWvcfynct_sX6ayJNtwhKd8GYmU3yEq4", # webkey
    "authDomain": "homesitter-54d69.firebaseapp.com", # projectID
    "databaseURL": "https://homesitter-54d69-default-rtdb.firebaseio.com",
    "storageBucket": "homesitter-54d69.appspot.com" # storageURL
}

firebase=pyrebase.initialize_app(config)

uploadfile="/home/pi/Desktop/homesitter/" # camera

storage=firebase.storage()

db=firebase.database()

count = 0

while True :
    count += 1
    updatefile="%d" % (count)
    now = datetime.datetime.now()
    filename = now.strftime('%Y%m%d%H%M%S')
    uploadfile="/home/pi/Desktop/homesitter/"+filename+".mp4"

    with picamera.PiCamera() as camera: # make a video file
        camera.rotation = 180
        camera.resolution = (360, 240) # video size
        camera.start_recording(output=filename+".h264") # now time is used to file name
        camera.wait_recording(60) # video file time length
        camera.stop_recording() # stop film

        command = "MP4Box -add " + filename+".h264" + " " + filename+".mp4"
        call([command], shell=True)
        print("\r\nRasp_Pi => Video Converted! \r")



    storage.child("cctv/video/"+filename+".mp4").put(uploadfile)
    storage.child("cctv/samevideo/"+str(count) +".mp4").put(uploadfile)
    print(filename+".mp4 done file upload!")
    fileUrl=storage.child("cctv/video/"+filename+".mp4").get_url(1) # 0: storage url, 1: download url
    updateUrl=storage.child("cctv/samevideo/"+str(count)+".mp4").get_url(1) # 0: storage url, 1: download url
    db.child("cctv/videoLink/real/"+filename).set(fileUrl)
    db.child("cctv/videoLink/Update/"+updatefile).set(updateUrl)

    print(filename+".mp4 done url push!")
    print(updateUrl+".mp4 done updateUrl push!")

