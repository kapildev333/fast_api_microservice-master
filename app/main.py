from fastapi import FastAPI, UploadFile, File, Form
from typing import Annotated
from app.utils import process_result, delete_directory, detect_qr_code, \
    send_common_response_for_verification
from app.driver_license_processor import processor

app = FastAPI()


@app.post("/process")
async def process_data(user_name: Annotated[str, Form()],
                       id_card: Annotated[str, Form()],
                       id_card_back: Annotated[str, Form()]):
    result = await processor.driver_license_processor(id_card)
    license_details = await process_result(result, user_name=user_name)
    back_side_data = await detect_qr_code(id_card_back)
    delete_directory()
    return send_common_response_for_verification(qr_code_data=back_side_data, send_empty=False,
                                                 driving_license=license_details)
