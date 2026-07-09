from .generate_data import generate_route
from .pages import pages_route
from .auth import auth_route
from .cart import cart_route
from .track import track_route
from .order import order_route

routes = [generate_route, pages_route, auth_route, cart_route, order_route, track_route]
