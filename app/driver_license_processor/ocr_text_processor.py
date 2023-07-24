import re

def detect_details(result, user_name):
    type_of_license: int  # type_of_license will determine if license is type 0 or 1
    occurrence_list = []  # occurrence_list will determine in which index we found license number
    license_number: str = ''
    expiry_date: str = ''
    birth_date: str = ''
    is_name_verified = False  # to determine if name coming from api and license matches
    is_valid = True  # to determine if license is valid or not
    number_list = []  # to store numeric value of all digits

    if len(result) > 0:
        type_of_license = determine_type_of_license(result=result)
        is_name_verified = verify_user_name(result=result, user_name=user_name)
        number_list, occurrence_list = find_numbers_from_ocr_result(result=result)
        try:
            """
            Make str values from list of items
            """
            license_number = "".join(number_list[0])  # as per new mexico driving license first value will be license number
            birth_date = "-".join(number_list[2])  # as per new mexico driving license second value will be birthdate
            expiry_date = "-".join(number_list[3])  # as per new mexico driving license third value will be expiry date
            """
            Validation for driver license number
            """
            if len(license_number) <= 7 or len(license_number) >= 10:
                is_valid = False
            if type_of_license == 1 and occurrence_list[0] < 2:
                is_valid = False
            if type_of_license == 0 and occurrence_list[0] < 5:
                is_valid = False
        except:
            is_valid = False
            is_name_verified = False
            license_number = "0"
            birth_date = "0"
            expiry_date = "0"
        finally:
            return {
                'is_valid': is_valid,
                'document_type': 'Driver License',
                'is_name_verified': is_name_verified,
                'license_number': license_number,
                'birth_date': birth_date,
                'expiry_date': expiry_date
            }


def verify_user_name(result, user_name) -> bool:
    """
    :param result:  list of strings found by OCR
    :param user_name: user's name given by post api
    :return: it will give true or false based on if we found name in driver license
    """
    list_of_names = user_name.split()
    # print(list_of_names)
    for string_data in result:
        for name in list_of_names:
            if string_data.lower().find(name.lower()) != -1:
                return True

    return False


def determine_type_of_license(result) -> int:
    """
    :param result: list of strings found by OCR
    :return: it will return either 0 or 1 based on type of license for e.g. if we found not or intended
    then value will be 0 else 1
    """
    if str(result[0]).find('not') != -1 or str(result[0]).find('intended') != -1:
        return 0
    else:
        return 1


def find_numbers_from_ocr_result(result):
    """
    :param result: list of strings found by OCR
    :return: list of strings containing list of characters which are digits
    """
    number_list = []
    occurrence_list = []
    for index, string_data in enumerate(result, start=0):
        if re.search(r'\d+', string_data) is not None:
            number_list.append((list(map(str, re.findall('\d+', string_data)))))
            occurrence_list.append(index)

    return number_list, occurrence_list
