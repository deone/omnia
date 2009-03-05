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

    def req_and_items(self, id):
        c.req_id = id
        return render("/requisition_detail.html")

    def all(self):
        return render("/all_requisitions.html")

    def approve(self):
        return render("/open_requisitions.html")

    def items(self, id):
        c.requisition = Requisition.get_as_dict(id)
        return render("/items.html")

    
    @h.json_response
    def get(self, id, **kwargs):
        return ("object", Requisition.get_as_dict(id=id))

    @h.json_response
    def get_all(self, **kwargs):
        return ("all_reqs_list", Requisition.get_as_dict(id=None))

    @h.json_response
    def get_open(self, **kwargs):
        return ("open_reqs_list", Requisition.get_open())

    @h.json_response
    def get_items(self, id=None, **kwargs):
        items = Requisition.get_items(id)
        return ("list", items)


    @h.json_response
    @h.commit_or_rollback
    def new(self, **kwargs):
        description = request.params['description']
        req = Requisition.create(description)
        return ("object", req.todict())

    @h.json_response
    @h.commit_or_rollback
    def new_item(self, id, **kwargs):
        quantity = request.params['qty']
        name = request.params['name']
        description = request.params['desc']
        unitprice = request.params['unitprice']

        req = Requisition.get(id=id)

        return req.add_item(quantity, name, description, unitprice)
