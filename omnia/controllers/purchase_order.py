import logging

from omnia.lib.base import *

import omnia.model.helpers as h
from omnia.model.models import *

log = logging.getLogger(__name__)

class PurchaseOrderController(BaseController):

    def index(self):
        return render('/purchase_orders.html')

    def create(self):
        return render('/create_purchase_order.html')

    def view(self, id):
        c.po_id = id
        return render('/purchase_order.html')

    def edit(self, id):
        c.po_id = id
        return render('/edit_purchase_order.html')

    def add_line_item(self, id):
        c.po_id = id
        return render('/add_po_line_item.html')

    @h.json_response
    @h.commit_or_rollback
    def new(self, **kwargs):
        vendor_id = request.params['vendor']
        user_id = request.params['user']

        return ("po_object", PurchaseOrder.create(vendor_id, user_id))

    @h.json_response
    def get_by_id(self, id, **kwargs):
        return ("po_object", PurchaseOrder.get_as_dict(id=id))

    @h.json_response
    def get(self, **kwargs):
        return ("po_list", PurchaseOrder.get_as_dict())
