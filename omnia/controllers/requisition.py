import logging
import datetime

from omnia.lib.base import *

import omnia.model.helpers as h
from omnia.model.models import *

log = logging.getLogger(__name__)

class RequisitionController(BaseController):

    def index(self):
        return render("/requisition.html")

    @h.json_response
    def get(self, id, **kwargs):
        return ("requisition", Requisition.get_as_dict(id))

    @h.json_response
    def get_all(self, **kwargs):
        return ("requisitions", Requisition.get_as_dict(id=None))

    @h.json_response
    @h.commit_or_rollback
    def new(self, **kwargs):
        description = request.params['description']
        req = Requisition.create(description)
        return ("new", req)

    def edit(self, id, **kwargs):
        c.req_id = id
        return render("requisition_edit.html")

    @h.json_response
    @h.commit_or_rollback
    def add_item(self, id, **kwargs):
        quantity = request.params['qty']
        name = request.params['name']
        description = request.params['desc']
        unitprice = request.params['unitprice']

        req = Requisition.get(id=id)

        return req.add_item(quantity, name, description, unitprice)
