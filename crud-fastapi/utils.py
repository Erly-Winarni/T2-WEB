def get_token_from_header(authorization: str):
    return authorization.split(" ")[1]


def success_response(message: str):
    return {"message": message}