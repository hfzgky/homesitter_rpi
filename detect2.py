import cv2
import numpy as np
import mtcnn
from pyrebase import pyrebase

from architecture import *
from train_v2 import normalize,l2_normalizer
from scipy.spatial.distance import cosine
from tensorflow.keras.models import load_model
import pickle
from pyfcm import FCMNotification
import FCMManager as fcm
#
from firebase_admin import db

# ref = db.reference().child('cctv').child('videoLink').child('real')
# print(ref.get())
#print(ref.get() + '.mp4')
#
# APIKEY = "AAAA4a0r8r0:APA91bFOt0Xz4fkWgYeQumUeIU5GXTQZR3doAnAO0ObMdzgZZKT5402WiNPL3hCgnrLCaOdR-YzWJ0RygG-kBKtoX6LWlysiMDNmb4ELdWG7iLwoOMbC8vsjnftAHg7GAVvYssHiu-8z"
# # 애뮬 TOKEN = "fo0jBhQ9QaWasZHIvQNE4j:APA91bG7kn1ZTD2fZ0OO_s_VLDEGcZHh9gDYGEEZOhAABMd3f7SmXdleX2Y_RkzUEqxyjkfSLHveUqthaCQJctRErvCqLnzsgMi11Td_JADEZOSW9FmTMjor-1wxiJ_My-wlYO-h1R5M"
# tokens = ["c3QDY8soTkiV6x9hV65K8b:APA91bFs1ArB0kzZ_EVopFV2Uod6eG9Jh-Q9h1Hpa_20GTJoKYoGOlenMzojNskelAfa9J0XLmsyJr3HHrc81nscco_QF6H4y_iWYKYFZv8QhwKa6oEKBIbQ-ZJkgmTTGcUxeZZvm6hJ",
#           "fo0jBhQ9QaWasZHIvQNE4j:APA91bG7kn1ZTD2fZ0OO_s_VLDEGcZHh9gDYGEEZOhAABMd3f7SmXdleX2Y_RkzUEqxyjkfSLHveUqthaCQJctRErvCqLnzsgMi11Td_JADEZOSW9FmTMjor-1wxiJ_My-wlYO-h1R5M"]
config={
    "apiKey": "AIzaSyBaWvcfynct_sX6ayJNtwhKd8GYmU3yEq4",
    "authDomain": "homesitter-54d69.firebaseapp.com",
    "databaseURL": "https://homesitter-54d69-default-rtdb.firebaseio.com",
    "projectId": "homesitter-54d69",
    "storageBucket": "homesitter-54d69.appspot.com",
    "messagingSenderId": "969272980157",
    "appId": "1:969272980157:web:492ba7c27a658c9c8b3dd4",
    "measurementId": "G-L3L4HXJ5BY"
}

#  파이어베이스 콘솔에서 얻어온 서버키를 넣어줌
# push_service = FCMNotification(APIKEY)


firebase = pyrebase.initialize_app(config)
db = firebase.database()

users = db.child("cctv").child("videoLink").child("Update").order_by_key().limit_to_last(1).get().val()
# users = db.child("cctv").child("videoLink").child("real").order_by_child("real").limit_to_last(1).get()
print(users[next(reversed(users))])
# for user in users.each():
#     print(user.key())


