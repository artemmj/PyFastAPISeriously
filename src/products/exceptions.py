from fastapi import status, HTTPException


ProductNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Товар не найден',
)
