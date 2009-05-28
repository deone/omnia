import logging

from omnia.lib.base import *

import omnia.model.helpers as h
from omnia.model.models import *

log = logging.getLogger(__name__)

def build_spec_list(items):
    items_specs = {}

    for i in names_set(items):
        spec_lst = []
        for j in items:
            if i == j['name']:
                spec_lst.append(j['specification'])

        items_specs[i] = spec_lst

    return items_specs

def names_set(items):
    names = []

    for i in items:
        names.append(i['name'])

    return list(set(names))

def items_set(items):
    lst = []

    for i in items:
        if i not in lst:
            lst.append(i)

    return lst
    

class LineitemController(BaseController):

    @h.json_response
    def get(self, **kwargs):
        items = LineItem.get_item_dict()

        specs = build_spec_list(items)

        for i in items:
            i['specification'] = specs[i['name']]
            i['quantity'] = len(specs[i['name']])

        return ("item_list", items_set(items))

    @h.json_response
    def get_types(self, **kwargs):
        types = LineItem.get_types()
        type_set = list(set(types))

        return ("item_type_list", type_set)

    @h.json_response
    def get_for_invoice(self, id, **kwargs):
        """This id is vendor_id, there should be a better way to do this.
           This does not read fine: /lineitem/vendor_id/get_by_vendor_id,
           Should be something like: /lineitem/get_by_vendor_id/vendor_id

           Same with get_by_invoice_no

           Solution: Use querystring param instead of url param.
        """
        po_id = request.params['po_id']

        items = LineItem.get_for_invoice(id, po_id)
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
        line_item.deliver(status)

        return ("ok", "Items Received")
