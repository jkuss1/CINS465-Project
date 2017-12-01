from channels import route_class

from .consumers import *

channel_routing = [
	route_class(Consumer, path=r''),
]
