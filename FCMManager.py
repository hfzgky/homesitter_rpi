
import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("C:/Users/01026580634/faceR/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

#def sendPush(title, msg, registration_token, dataObject=None, click_action=None):
def sendPush(title, msg, registration_token, dataObject=None):
    # See documentation on defining a message payload.
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg

        ),
        data={
            'imgUri': 'abc.PNG'
        }, # 여기서 동영상의 링크를 넘겨주기!!
        tokens=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send_multicast(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)