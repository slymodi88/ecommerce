def jwt_get_username_from_payload_handler(payload):
    return payload.get('user_name', None)
