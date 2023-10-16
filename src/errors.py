from fastapi import HTTPException
from fastapi import status


class HTTPUnauthorizedError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=None
        )


class HTTPMachineStateError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=None
        )
