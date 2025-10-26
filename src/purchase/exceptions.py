from fastapi import status, HTTPException


CartNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Не найдена корзина пользователя. Создайте',
)


ProductNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Товар не найден',
)


ItemInCartNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Такой товар в корзине не найден',
)
