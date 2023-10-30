# -*- coding: utf-8 -*-

RESP_MSG_SUCCESS = 'success'
RESP_MSG_ERROR_IN_SERVER = 'Error In Server'

RESP_MSG_NOT_FOUND_CLIENT_ID = 'not found client id'
RESP_MSG_NOT_MATCH = 'not match'
RESP_MSG_FORBIDDEN = 'forbidden'
RESP_MSG_FILE_NOT_FOUND = 'file not found'
RESP_MSG_MIMETYPES_NOT_FOUND = 'mimetypes not found'
RESP_MSG_FCHAT_NOT_FOUND = 'fchat not found'
RESP_MSG_FCHAT_CONFIG_NOT_FOUND = 'live chat configs not found'
RESP_MSG_FCHAT_CONFIG_AGENT_STATUS = 'live chat configs and agent status'
RESP_MSG_FCHAT_CONFIG_AGENT_NOT_FOUND = 'Livechat/Agent not found'
RESP_MSG_ROOM_NOT_FOUND = 'Room not found'
RESP_MSG_ROOM_EXISTED = 'room is existed'
RESP_MSG_ROOM_NOT_EXISTED = 'room is NOT existed'
RESP_MSG_ROOM_EXPIRED = 'room is expired'
RESP_MSG_ROOM_INVALID = 'Invalid room'
RESP_MSG_UPDATE_ROOM_STATUS_FAILED = 'Không thể cập nhật trạng thái room chat.'
RESP_MSG_SYSTEM_ERROR = 'Lỗi trong hệ thống'

RESP_MSG_SEEN_MESSAGE_SUCCESS = 'Seen messages successfully'


def get_error_response(error_code: int):
    message_error = ERROR_CODE.get(error_code)
    return {
        "success": False,
        "error_code": error_code,
        "error": message_error,
        "data": []
    }


ERROR_CODE = {
    4000100: 'Bad Request',
    4000101: 'unverified token',
    4000102: 'kid not match',
    4000103: 'User info already existed',
    4000104: 'Role already existed',
    4000105: 'Team already existed',
    4000106: 'Only allow offset as number and start from 1.',
    4000107: "current | size pagination must be an instance of int",
    4000108: "current | size pagination must >= 1",
    4000109: "field sort only 2 value: -1 (desc) or 1 (asc)",
    4000110: 'File\'s extension is not allowed',
    4000201: 'phone number already exists',
    4010100: 'Unauthenticated',
    4010101: 'token expire',
    4010102: 'Not found user',
    4010103: 'token is invalid',
    4010104: 'Already existed role with the same code',
    4010105: 'Call data already existed',
    4010106: 'Call data not found',
    4010107: 'Call record not found',
    4010108: 'Call note not found',
    4030100: 'Unauthorized',
    4030101: 'Forbidden',
    4030102: 'Forbidden reason no permissions',
    4030103: 'Forbidden reason lack of permissions',
    4040100: 'Not found',
    4040101: 'redirect url not valid',
    4040102: 'Team not found',
    4040103: 'Role not found',
    4040104: 'Can\'t find any user',
    4040105: 'Cannot find avatar',
    4040204: 'ObjectID not found',
    4220100: 'Unprocessable Entity',
    4220101: 'Invalid object id format',
    5000100: 'Application Error',
    5000101: 'Failed to create team',
    5000102: 'Failed to read team',
    5000103: 'Failed to delete team',
    5000104: 'Failed to read role data',
    5000105: 'Failed to delete user',
    5000106: 'Failed to upload file',
    5000107: 'Failed to get file \'s url',
}
