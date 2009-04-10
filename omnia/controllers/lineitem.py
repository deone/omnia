import logging

from omnia.lib.base import *

import omnia.model.helpers as h
from omnia.model.models import *

log = logging.getLogger(__name__)

class LineitemController(BaseController):

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
