from fastapi import HTTPException, status


def credential_error(detail: str, auth_type: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers={"WWW-Authenticate": auth_type},
    )
