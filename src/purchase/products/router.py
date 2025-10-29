import loguru

from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, status
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user, get_current_admin_user
from src.auth.models import User
from src.dao.database import get_session_without_commit, get_session_with_commit
from src.purchase.products.dao import ProductsDAO
from src.purchase.exceptions import FileSaveFailedException, IncorrectFileContentTypeException, ProductNotFoundException
from src.purchase.products.schemas import ProductBaseModelSchema, ProductCreateUpdateModelSchema
from src.purchase.products.models import Product

router = APIRouter()
logger = loguru.logger


@router.get('')
async def get_all_products(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_without_commit),
) -> List[ProductBaseModelSchema]:
    return await ProductsDAO(session).find_all()


@router.post('')
async def create_product(
    product_data: ProductCreateUpdateModelSchema,
    admin_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session_with_commit),
) -> ProductBaseModelSchema:
    new_product = await ProductsDAO(session).add(**product_data.model_dump(exclude_unset=True))
    return new_product


@router.put('/{id}')
@router.patch('/{id}')
async def update_product(
    id: int,
    new_product_data: ProductCreateUpdateModelSchema,
    admin_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session_with_commit),
) -> ProductBaseModelSchema:
    dao = ProductsDAO(session)
    upd_user = await dao.get_one_by_id(id=id)
    if not upd_user:
        raise ProductNotFoundException
    return await dao.update(id=id, values=new_product_data)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    id: int,
    admin_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session_with_commit),
) -> None:
    dao = ProductsDAO(session)
    upd_user = await dao.get_one_by_id(id=id)
    if not upd_user:
        raise ProductNotFoundException
    return await dao.delete(id=id)


@router.post("/{id}/upload_image")
async def upload_product_image(  # TODO REFACTOR
    id: int, # ID продукта из пути
    file: UploadFile = File(...),
    admin_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session_with_commit),
):
    # Папка для сохранения файлов внутри static
    UPLOADS_DIR_PATH = Path("static/uploads")
    UPLOADS_DIR_PATH.mkdir(parents=True, exist_ok=True) # Создаст static/uploads если нет

    # 1. Проверить, существует ли товар
    stmt = select(Product).where(Product.id == id)
    result = await session.execute(stmt)
    db_product = result.scalar_one_or_none()

    if not db_product:
        raise ProductNotFoundException

    # 2. Проверить тип файла
    allowed_types = {"image/jpeg", "image/jpg", "image/png", "image/gif"}
    if file.content_type not in allowed_types:
        raise IncorrectFileContentTypeException

    # 3. Сгенерировать уникальное имя файла
    import uuid
    ext = file.filename.split(".")[-1] if "." in file.filename else "bin"
    unique_filename = f"{uuid.uuid4()}.{ext}"
    file_path = UPLOADS_DIR_PATH / unique_filename

    # 4. Сохранить файл
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise FileSaveFailedException

    # 5. Обновить поле image_url в БД
    # URL будет вида /static/uploads/{filename}
    image_url = f"/static/uploads/{unique_filename}"
    stmt = select(Product).where(Product.id == id)
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()
    if product:
        product.image_url = image_url
        await session.commit()
        await session.refresh(product)
    return product

    # if not updated_product:
    #     # Это маловероятно, если мы только что проверили его существование, но на всякий случай
    #     raise HTTPException(status_code=404, detail="Товар не найден после обновления")
    return updated_product


# --- Роут для обновления товара (включая image_url) ---
# @router.put("/products/{product_id}", response_model=schemas.Product)
# def update_product(
#     product_id: int,
#     product_update: schemas.ProductUpdate, # Pydantic схема для обновления
#     db: Session = Depends(get_db)
# ):
#     # Найдите товар
#     stmt = select(models.Product).where(models.Product.id == product_id)
#     result = db.execute(stmt)
#     db_product = result.scalar_one_or_none()

#     if not db_product:
#         raise HTTPException(status_code=404, detail="Товар не найден")

#     # Обновите только те поля, которые были переданы
#     update_data = product_update.model_dump(exclude_unset=True)
#     for field, value in update_data.items():
#         setattr(db_product, field, value)

#     db.commit()
#     db.refresh(db_product)
#     return db_product

# ... другие роуты ...
