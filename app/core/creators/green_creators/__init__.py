from .MainCreator import MainCreator
from .AuthCreator import AuthCreator
from .CartCreator import CartCreator
from app.core.creators.static_creator import StaticCreator

green_creators_list = [
    MainCreator(),
    MainCreator("product_grid", "Каталог"),
    AuthCreator(),
    CartCreator(),
    StaticCreator("hero_banner"),
    StaticCreator("footer"),
    StaticCreator("about_block"),
    StaticCreator("filter_sort_bar"),
    StaticCreator("sort_label"),
    StaticCreator("detail_form"),
]
