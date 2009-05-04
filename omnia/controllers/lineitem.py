import logging

from omnia.lib.base import *

import omnia.model.helpers as h
from omnia.model.models import *

log = logging.getLogger(__name__)

class LineitemController(BaseController):

    @h.json_response
    def get_by_vendor_id(self, id, **kwargs):
        """This id is vendor_id, there should be a better way to do this.
           This does not read fine: /lineitem/vendor_id/get_by_vendor_id,
           Should be something like: /lineitem/get_by_vendor_id/vendor_id

           Same with get_by_invoice_no
        """
        items = LineItem.get_by_vendor_id(id)
        return ("itemname_list", items)

    @h.json_response
    def get_by_invoice_no(self, id, **kwargs):
        items = LineItem.get_by_invoice_no(id)
        return ("item_list", items)

    @h.json_response
    @h.commit_or_rollback
    def new(self, id, **kwargs):
        name = request.params['name']
        itemtype = request.params['type']
        specification = request.params['spec']
        quantity = request.params['qty']
        unitprice = request.params['unitprice']
        vendor = request.params['vendor']

        req = Requisition.get(id=id)

        req.add_line_item(name, itemtype, specification, quantity, unitprice, vendor)

    @h.json_response
    @h.commit_or_rollback
    def order(self, id, **kwargs):
        unit_price = request.params['unitprice']
        po_id = request.params['poid']

        line_item = LineItem.get(id)
        line_item.order(unit_price, po_id)

    @h.json_response
    @h.commit_or_rollback
    def invoice(self, id, **kwargs):
        specification = request.params['specification']
        quantity = request.params['quantity']
        unit_price = request.params['unit_price']
        invoice_no = request.params['invoice_no']

        line_item = LineItem.get(id)

        if specification.strip().upper() != line_item.specification.strip().upper():
            return ("error", "Specification does not match PO item specification")

        if int(quantity.strip()) != int(line_item.quantity):
            return ("error", "Quantity does not match PO item quantity")

        if int(unit_price.strip()) != int(line_item.unitprice):
            return ("error", "Unit price does not match PO item unit price")

        ret_val = line_item.invoice(specification, quantity, unit_price, invoice_no)
        return ("ok", ret_val)

    @h.json_response
    @h.commit_or_rollback
    def deliver(self, id, **kwargs):
        status = request.params['status']

        line_item = LineItem.get(id)
        ret_val = line_item.deliver(status)

        if ret_val == None:
            return ("ok", "Items Received")
        else:
            return ("error", "Error Receiving Items")
