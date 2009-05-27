import logging

from omnia.lib.base import *

import omnia.model.helpers as h
from omnia.model.models import *

log = logging.getLogger(__name__)

class WarehouseController(BaseController):

    def index(self):
        return render ("/warehouse.html")

    @h.json_response
    def check(self, **kwargs):
        location = request.params['location']
        reg_location = Warehouse.get(1).location

        if location != reg_location:
            return ("error", "Unknown Location")

        return ("ok", "Good to go")
