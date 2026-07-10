from .navbar_creator import NavbarCreator
from .product_grid_creator import ProductGridCreator
from .auth_creator import AuthCreator
from .cart_container_creator import CartContainerCreator
from .order_btn_creator import OrderBtnCreator
from .detail_form_creator import DetailFormCreator
from .product_description_layer_creator import ProductDescriptionCreator
from .new_navbar_creator import NewNavbarCreator
from .promo_strip import PromoStripCreator
from .banner import BannerCreator
from .link_creator import LinkCreator
from .footer_creator import FooterCreator
from .product_card_creator import ProductCardCreator
from .content_creator import ContentCreator
from .cart_summary_creator import CartSummaryCreator

CREATORS_DICT = {
    NavbarCreator.item_type: NavbarCreator(),
    ProductGridCreator.item_type: ProductGridCreator(),
    AuthCreator.item_type: AuthCreator(),
    CartContainerCreator.item_type: CartContainerCreator(),
    OrderBtnCreator.item_type: OrderBtnCreator(),
    DetailFormCreator.item_type: DetailFormCreator(),
    ProductDescriptionCreator.item_type: ProductDescriptionCreator(),
    NewNavbarCreator.item_type: NewNavbarCreator(),
    PromoStripCreator.item_type: PromoStripCreator(),
    BannerCreator.item_type: BannerCreator(),
    LinkCreator.item_type: LinkCreator(),
    FooterCreator.item_type: FooterCreator(),
    ProductCardCreator.item_type: ProductCardCreator(),
    ContentCreator.item_type: ContentCreator(),
    CartSummaryCreator.item_type: CartSummaryCreator(),
}
