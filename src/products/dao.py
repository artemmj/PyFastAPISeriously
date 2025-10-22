from src.dao.base import BaseDAO
from src.products.models import Product


class ProductsDAO(BaseDAO):
    model = Product
