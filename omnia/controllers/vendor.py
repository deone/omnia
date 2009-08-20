import logging

from omnia.lib.base import *
import omnia.model.helpers as h
from omnia.model.models import *

log = logging.getLogger(__name__)

class VendorController(BaseController):

    def index(self):
        return 'Hello World'

    @h.json_response
    def get_by_id(self, id, **kwargs):
        return ("vendor_object", Vendor.get_as_dict(id))

    @h.json_response
    def get_names(self, **kwargs):
        return ("vendorname_list", Vendor.get_names())

    @h.json_response
    def get_vendors_with_line_items(self, **kwargs):
        return ("vendorname_list", Vendor.get_vendors_with_line_items())
