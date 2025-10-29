from fastapi import status, HTTPException


CartNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Не найдена корзина пользователя. Создайте',
)


ProductNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Товар не найден',
)


ItemInCartNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Такой товар в корзине не найден',
)


CartEmptyException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Корзина пуста, невозможно оформить заказ'
)


IncorrectFileContentTypeException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Файл должен быть изображением (.jpeg, .png или .gif)'
)


FileSaveFailedException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Ошибка при сохранении файла'
)
