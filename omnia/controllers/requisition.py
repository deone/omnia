import logging
import datetime

from omnia.lib.base import *

import omnia.model.helpers as h
from omnia.model.models import *

log = logging.getLogger(__name__)

class RequisitionController(BaseController):

    def index(self):
        return render("/requisition.html")

    def add_item(self, id):
        c.req_id = id
        return render("/add_item.html")

    def details(self, id):
        c.req_id = id
        return render("/requisition_detail.html")

    def all(self):
        return render("/all_requisitions.html")

    @h.json_response
    @h.commit_or_rollback
    def new(self, **kwargs):
        description = request.params['description']
        req = Requisition.create(description)
        return ("new", req)

    @h.json_response
    def get(self, id, **kwargs):
        return ("requisition", Requisition.get_as_dict(id))

    @h.json_response
    def get_all(self, **kwargs):
        return ("requisitions", Requisition.get_as_dict(id=None))

    @h.json_response
    @h.commit_or_rollback
    def new_item(self, id, **kwargs):
        quantity = request.params['qty']
        name = request.params['name']
        description = request.params['desc']
        unitprice = request.params['unitprice']

        req = Requisition.get(id=id)

        return req.add_item(quantity, name, description, unitprice)

    def items(self, id):
        c.requisition = Requisition.get_as_dict(id)

        return render("/items.html")

    @h.json_response
    def get_items(self, id=None, **kwargs):
        items = Requisition.get_items(id)
        return ("list", items)
