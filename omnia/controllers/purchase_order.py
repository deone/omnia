import logging
import simplejson

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

    def doc_print(self, id):
        c.po_id = id
        return render('/print_purchase_order.html')

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
    @h.commit_or_rollback
    def close(self, id, **kwargs):
        location = request.params['location']
        closed_by = request.params['closed_by']
        
        po = PurchaseOrder.get(id)
        ret_val = po.close(location, closed_by)

        return ("ok", "Items Received")

    @h.json_response
    def get_by_id(self, id, **kwargs):
        po_dict = PurchaseOrder.get_as_dict(id=id) 

        if po_dict:
            return ("po_object", po_dict)
        else:
            return ("error", "No such Purchase Order")

    @h.json_response
    def get_invoiced(self, **kwargs):
        return ("poid_list", Invoice.get_po_ids())

    @h.json_response
    def get(self, **kwargs):
        return ("po_list", PurchaseOrder.get_as_dict())

    @h.json_response
    def is_invoice_received(self, id, **kwargs):
        retval = id in simplejson.dumps([i.purchase_order_id for i in Invoice.get()])
        if not retval:
            return ("error", "Invoice not received")
        else:
            return ("ok", "Invoice received")
