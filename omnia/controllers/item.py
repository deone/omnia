import logging

from omnia.lib.base import *

import omnia.model.helpers as h
from omnia.model.models import *

log = logging.getLogger(__name__)

class ItemController(BaseController):

    def index(self):
        return 'Hello World'

    @h.json_response
    def get(self, **kwargs):
        return (Item.get(), "items")

    @h.json_response
    def get_types(self, **kwargs):
        return ("itemtype_list", Item.types())

    @h.json_response
    def get_by_type(self, type, **kwargs):
        return ("itemname_list", Item.item_by_type(type))
