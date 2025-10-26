from src.dao.base_dao import BaseDAO
from src.purchase.products.models import Product


class ProductsDAO(BaseDAO):
    model = Product
