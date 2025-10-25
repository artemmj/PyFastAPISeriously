from src.dao.base_dao import BaseDAO
from src.products.models import Product


class ProductsDAO(BaseDAO):
    model = Product
