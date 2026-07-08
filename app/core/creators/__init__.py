from .navbar_creator import NavbarCreator
from .product_grid_creator import ProductGridCreator

CREATORS_DICT = {
    NavbarCreator.item_type: NavbarCreator(),
    ProductGridCreator.item_type: ProductGridCreator(),
}
