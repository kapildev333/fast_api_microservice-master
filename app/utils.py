import os


from app.driver_license_processor import ocr_text_processor
import cv2
from pathlib import Path
import shutil

from urllib.request import urlopen
import numpy as np
from pyzbar.pyzbar import decode

# class Settings(BaseSettings):
#     env = environ.Env()
#     environ.Env.read_env()
#     EMAIL_BACKEND = env('EMAIL_BACKEND')
#     EMAIL_HOST = env('EMAIL_HOST')
#     EMAIL_USE_TLS = env('EMAIL_USE_TLS')
#     EMAIL_PORT = env('EMAIL_PORT')
#     EMAIL_HOST_USER = env('EMAIL_HOST_USER')
#     EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')


# settings = Settings()


class CommonStrings:
    mobile_app_name = 'WeedDasher'
    account_verification = 'Account Vemrification'


# async def send_email():
#     """
#     :param email_address: Email address of user to notify
#     :param user_name: Name of user to notify
#     :param valid: Check if id card is valid or not
#     """
#     # Sending mail for verification confirmation
#     print(settings.EMAIL_HOST_USER)
#     conf = ConnectionConfig(
#         MAIL_USERNAME=settings.EMAIL_HOST_USER,
#         MAIL_PASSWORD=settings.EMAIL_HOST_PASSWORD,
#         MAIL_FROM=settings.EMAIL_HOST_USER,
#         MAIL_PORT=settings.EMAIL_PORT,
#         MAIL_SERVER=settings.EMAIL_HOST,
#         MAIL_FROM_NAME=CommonStrings.mobile_app_name,
#         MAIL_STARTTLS=False,
#         MAIL_SSL_TLS=False,
#         USE_CREDENTIALS=True,
#         VALIDATE_CERTS=True
#     )
#     html = """<p>Hi this test mail, thanks for using Fastapi-mail</p>"""

#     message = MessageSchema(
#         subject="Fastapi-Mail module",
#         recipients=["kapil.soni@bacancy.com"],
#         body=html,
#         subtype=MessageType.html)

#     fm = FastMail(conf)
#     await fm.send_message(message)


def send_common_response_for_verification(send_empty, driving_license=None, qr_code_data=None):
    """
    :param send_empty: Whether to send or not send empty response
    :param driving_license: Data containing the details of id card after Ocr verification
    :return: It will return a common response in Json format
    """
    if driving_license is None:
        driving_license = {}

    if qr_code_data is None:
        qr_code_data = {}

    print(qr_code_data)
    if send_empty:

        common_response = {'message': 'Fail', 'data': {
            'verified': False,
        }}
        return common_response
    else:

        common_response = {'message': 'Success', 'data': {
            'verified': True,
            'qr_code_data': qr_code_data,
            'id_card': driving_license
        }}
        return common_response


async def process_result(result, user_name):
    """
    :param result: The list of what OCR has found in id card
    :param user_name: Name of user.so we can verify that person name is matching in id-card with user_name
    :return: It will return a Json containing details of driver license
    :example:{
            "is_valid": true,
            "document_type": "Driver License",
            "is_name_verified": false,
            "license_number": "037849448",
            "birth_date": "05-05-1963",
            "expiry_date": "06-01-2029"
        }
    """
    return ocr_text_processor.detect_details(result, user_name=user_name)


async def detect_qr_code(img_path):
    # final_path = str(settings.BASE_DIR) + img_path
    resp = urlopen(img_path)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(image, cv2.IMREAD_COLOR)
    barcodes = decode(img)
    isQrDetected = True if(len(barcodes)>0) else False
    back_side_data = {
        'is_qr_detected': isQrDetected
    }
    dir_path = str(Path(__file__).resolve().parent.parent) + '/outputs'
    dir_path1 = str(Path(__file__).resolve().parent.parent) + '/media'
    try:
        shutil.rmtree(dir_path)
        shutil.rmtree(dir_path1)
    except OSError as x:
        print("Error occured: %s : %s" % (dir_path, x.strerror))
    finally:
        return back_side_data


def return_path(file, user_name):
    # Access the user data
    upload_dir = os.path.join(os.getcwd(), "uploads", user_name)
    # Create the upload directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # get the destination path
    destination = os.path.join(upload_dir, file.filename)
    print(destination)
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return destination


def delete_directory():
    dir_path = os.path.join(os.getcwd(), "uploads")
    output_dir_path = os.path.join(os.getcwd(), "outputs")
    if os.path.exists(dir_path) or os.path.exists(output_dir_path):
        try:
            shutil.rmtree(dir_path)
            shutil.rmtree(output_dir_path)
        except OSError as x:
            print("Error occured: %s : %s" % (dir_path, x.strerror))
        finally:
            return
    else:
        return

