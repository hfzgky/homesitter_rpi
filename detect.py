import cv2 
import numpy as np
import mtcnn
from architecture import *
from train_v2 import normalize,l2_normalizer
from scipy.spatial.distance import cosine
from tensorflow.keras.models import load_model
import pickle
from pyfcm import FCMNotification
import FCMManager as fcm

# 파베에 저장되어있는 1분컷 영상 가져오기 위한 변수
count = 1

# 최종적으로  unknown인지 아닌지 판별하기위한 변수
global unknown_cnt
unknown_cnt = 0
global known_cnt
known_cnt = 0



APIKEY = "AAAA4a0r8r0:APA91bFOt0Xz4fkWgYeQumUeIU5GXTQZR3doAnAO0ObMdzgZZKT5402WiNPL3hCgnrLCaOdR-YzWJ0RygG-kBKtoX6LWlysiMDNmb4ELdWG7iLwoOMbC8vsjnftAHg7GAVvYssHiu-8z"
# 애뮬 TOKEN = "fo0jBhQ9QaWasZHIvQNE4j:APA91bG7kn1ZTD2fZ0OO_s_VLDEGcZHh9gDYGEEZOhAABMd3f7SmXdleX2Y_RkzUEqxyjkfSLHveUqthaCQJctRErvCqLnzsgMi11Td_JADEZOSW9FmTMjor-1wxiJ_My-wlYO-h1R5M"
tokens = ["c3QDY8soTkiV6x9hV65K8b:APA91bFs1ArB0kzZ_EVopFV2Uod6eG9Jh-Q9h1Hpa_20GTJoKYoGOlenMzojNskelAfa9J0XLmsyJr3HHrc81nscco_QF6H4y_iWYKYFZv8QhwKa6oEKBIbQ-ZJkgmTTGcUxeZZvm6hJ",
          "fo0jBhQ9QaWasZHIvQNE4j:APA91bG7kn1ZTD2fZ0OO_s_VLDEGcZHh9gDYGEEZOhAABMd3f7SmXdleX2Y_RkzUEqxyjkfSLHveUqthaCQJctRErvCqLnzsgMi11Td_JADEZOSW9FmTMjor-1wxiJ_My-wlYO-h1R5M"]

#  파이어베이스 콘솔에서 얻어온 서버키를 넣어줌
push_service = FCMNotification(APIKEY)

confidence_t=0.99
recognition_t=0.5
required_size = (160,160)



def get_face(img, box):
    x1, y1, width, height = box
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = img[y1:y2, x1:x2]
    return face, (x1, y1), (x2, y2)

def get_encode(face_encoder, face, size):
    face = normalize(face)
    face = cv2.resize(face, size)
    encode = face_encoder.predict(np.expand_dims(face, axis=0))[0]
    return encode


def load_pickle(path):
    with open(path, 'rb') as f:
        encoding_dict = pickle.load(f)
    return encoding_dict

def detect(img, detector, encoder, encoding_dict):
    global unknown_cnt
    global known_cnt

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = detector.detect_faces(img_rgb)
    for res in results:
        if res['confidence'] < confidence_t:
            continue
        face, pt_1, pt_2 = get_face(img_rgb, res['box'])
        encode = get_encode(encoder, face, required_size)
        encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
        name = 'unknown'

        distance = float("inf")
        for db_name, db_encode in encoding_dict.items():
            dist = cosine(db_encode, encode)
            if dist < recognition_t and dist < distance:
                name = db_name
                distance = dist

        if name == 'unknown':
            cv2.rectangle(img, pt_1, pt_2, (0, 0, 255), 2)
            cv2.putText(img, name, pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
            print('너 누구야')
            unknown_cnt += 1
            print(unknown_cnt)
        else:
            cv2.rectangle(img, pt_1, pt_2, (0, 255, 0), 2)
            cv2.putText(img, name + f'__{distance:.2f}', (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 200), 2)
            print(name + "이 맞네요")
            known_cnt += 1
            print(known_cnt)
    return img 



if __name__ == "__main__":
    required_shape = (160,160)
    face_encoder = InceptionResNetV2()
    path_m = "facenet_keras_weights.h5"
    face_encoder.load_weights(path_m)
    encodings_path = 'encodings/encodings.pkl'
    face_detector = mtcnn.MTCNN()
    encoding_dict = load_pickle(encodings_path)

    while True:
        # cap = cv2.VideoCapture('Man.mp4') # <- 사람마다 바뀌어야 되는 부분
        cap = cv2.VideoCapture('https://firebasestorage.googleapis.com/v0/b/homesitter-54d69.appspot.com/o/cctv%2FVideo%2F' + str(count) + '.mp4?alt=media&token=1') # <- 1분짜리영상마다 바뀌어야 되는 부분

        while cap.isOpened():
            ret,frame = cap.read()

            # 영상이 끝나면 실행
            if not ret:
                count += 1
                break

            frame= detect(frame , face_detector , face_encoder , encoding_dict)

            cv2.imshow('camera', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if unknown_cnt > known_cnt:
            fcm.sendPush("낯선사람", "등장등장", tokens)
            print(unknown_cnt)
            print(known_cnt)
            print(str(count) + '번 동영상')
            unknown_cnt = 0
            known_cnt = 0
        else:
            print('주인이 맞다~~`~')
            print(unknown_cnt)
            print(known_cnt)
            print(str(count) + '번 동영상')
            unknown_cnt = 0
            known_cnt = 0
