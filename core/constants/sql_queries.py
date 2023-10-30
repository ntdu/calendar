# -*- coding: utf-8 -*-
# flake8: noqa
SQL_COMMAND_INSERT_MESSAGE_ROOM = '''
    INSERT INTO public.app_connect_message(
        uuid, fb_message_id, sender_id, recipient_id, reaction, is_forward,
        reply_id, text, sender_name, is_seen, is_sender, remove_for_you, created_at, "timestamp", room_id_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''

SQL_COMMAND_SELECT_MESSAGE = '''
    SELECT id, uuid, fb_message_id, sender_id, recipient_id, text, sender_name, is_seen, is_sender, created_at, "timestamp", room_id_id
	FROM public.app_connect_message
    WHERE room_id_id = %s AND fb_message_id = %s
    ORDER BY id DESC;
'''

SQL_COMMAND_INSERT_ATTACHMENT = '''
    INSERT INTO public.app_connect_attachment(
        attachment_id, file, type, url, name, size, mid_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
'''
