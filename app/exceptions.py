from fastapi import HTTPException, status


class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token has expired')


class TokenNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')


UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
PasswordMismatchException = HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Passwords mismatch')
IncorrectEmailOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password')
NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='JWT not valid')
NoUserIdException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
ForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Forbidden')