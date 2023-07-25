import os

import cv2
import numpy as np

import easyocr
from .processor_modules.face_detection_module import find_face as detect_face
from urllib.request import urlopen


async def driver_license_processor(img_path):
    # ori_thresh = 3  # Orientation angle threshold for skew correction
    # use_cuda = "cuda" if torch.cuda.is_available() else "cpu"
    # model = UnetModel(Res34BackBone(), use_cuda)
    face_detector = detect_face.face_factory(face_model="ssd")
    find_face_id = face_detector.get_face_detector()

    resp = urlopen(img_path)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    src_image = cv2.imdecode(image, cv2.IMREAD_COLOR)  # The image object
    # src_image = cv2.imread(img_path)

    crop = cv2.resize(src_image, (640, 448))
    img1 = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)

    final_img = find_face_id.changeOrientationUntilFaceFound(img1, 30)

    # txt_heat_map, regions = utils.createHeatMapAndBoxCoordinates(final_img)
    #
    # txt_heat_map = cv2.cvtColor(txt_heat_map, cv2.COLOR_BGR2RGB)
    #
    # predicted_mask = model.predict(txt_heat_map)
    #
    # orientation_angle = utils.findOrientationofLines(predicted_mask.copy())
    #
    # if abs(orientation_angle) > ori_thresh:
    #     final_img = utils.rotateImage(orientation_angle, final_img)

    models_path = os.path.abspath(os.getcwd() + "/app" + "/ease_ocr_models")
    reader = easyocr.Reader(['en'], model_storage_directory=models_path, download_enabled=False)
    result = reader.readtext(final_img, detail=0)
    return result
