from .navbar_creator import NavbarCreator
from .product_grid_creator import ProductGridCreator
from .auth_creator import AuthCreator
from .cart_container_creator import CartContainerCreator
from .order_btn_creator import OrderBtnCreator
from .detail_form_creator import DetailFormCreator
from .product_description_layer_creator import ProductDescriptionCreator

CREATORS_DICT = {
    NavbarCreator.item_type: NavbarCreator(),
    ProductGridCreator.item_type: ProductGridCreator(),
    AuthCreator.item_type: AuthCreator(),
    CartContainerCreator.item_type: CartContainerCreator(),
    OrderBtnCreator.item_type: OrderBtnCreator(),
    DetailFormCreator.item_type: DetailFormCreator(),
    ProductDescriptionCreator.item_type: ProductDescriptionCreator(),
}
