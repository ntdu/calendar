# -*- coding: utf-8 -*-
from typing import Any, Dict

from core.constants import facebook_error_msg as error
from rest_framework import status
from rest_framework.response import Response


def make_response(
    message: str,
    data: Any = None,
    status: int = 200
) -> Dict:
    return {"status": status, "message": message, "data": data}


def custom_response(status_code=status.HTTP_200_OK, message='', data=[]):
    return Response(
        {
            "status": status_code,
            "message": message,
            "data": data
        },
        status=status_code
    )


def handle_message_errors(data):
    code = str('FB_') + str(data['error']['code'])
    if data['error'].get('error_subcode', None):
        error_subcode = data['error']['error_subcode']
        code += f"_{error_subcode}"
    msg = msg_errors(code)
    return msg


def msg_errors(code):       # NOSONAR
    msg = ""
    if code == 'FB_1200':
        msg = error.FB_1200
    elif code == "FB_4_2018022":
        msg = error.FB_4_2018022
    elif code == "FB_100_2018109":
        msg = error.FB_100_2018109
    elif code == "FB_613":
        msg = error.FB_613
    elif code == "FB_613_2018338":
        msg = error.FB_613_2018338
    elif code == "FB_100_2018144":
        msg = error.FB_100_2018144
    elif code == "FB_2022":
        msg = error.FB_2022
    elif code == "FB_100":
        msg = error.FB_100
    elif code == "FB_100_2018001":
        msg = error.FB_100_2018001
    elif code == "FB_100_2018014":
        msg = error.FB_100_2018014
    elif code == "FB_100_2018164":
        msg = error.FB_100_2018164
    elif code == "FB_100_2018320":
        msg = error.FB_100_2018320
    elif code == "FB_100_2018328":
        msg = error.FB_100_2018328
    elif code == "FB_190":
        msg = error.FB_190
    elif code == "FB_10_2018278":
        msg = error.FB_10_2018278
    elif code == "FB_10_2018065":
        msg = error.FB_10_2018065
    elif code == "FB_10_2018108":
        msg = error.FB_10_2018108
    elif code == "FB_200_1545041":
        msg = error.FB_200_1545041
    elif code == "FB_200_2018028":
        msg = error.FB_200_2018028
    elif code == "FB_200_2018027":
        msg = error.FB_200_2018027
    elif code == "FB_200_2018021":
        msg = error.FB_200_2018021
    elif code == "FB_551_1545041":
        msg = error.FB_551_1545041
    elif code == "FB_10303":
        msg = error.FB_10303
    elif code == "FB_2018171":
        msg = error.FB_2018171
    elif code == "FB_2018234":
        msg = error.FB_2018234
    elif code == "FB_2018237":
        msg = error.FB_2018237
    elif code == "FB_2018321":
        msg = error.FB_2018321
    elif code == "FB_2018300":
        msg = error.FB_2018300
    elif code == "FB_36007":
        msg = error.FB_36007
    elif code == "FB_2_2018344":
        msg = error.FB_2_2018344
    elif code == "FB_100_33":
        msg = error.FB_100_33
    elif code == "FB_100_36007":
        msg = error.FB_100_36007
    else:
        msg = error.E_FB_DEFAULT
    return msg
