import logging
import datetime

from omnia.lib.base import *

import omnia.model.helpers as h
from omnia.model.models import *

log = logging.getLogger(__name__)

class RequisitionController(BaseController):

    def index(self):
        return render("/requisitions.html")

    def create(self):
        return render("/create_requisition.html")

    def add_line_item(self, id):
        c.req_id = id
        return render("/add_line_item.html")

    def req_and_items(self, id):
        c.req_id = id
        return render("/requisition.html")

    def doc_print(self, id):
        c.req_id = id
        return render("/print_requisition.html")

    def approve(self):
        return render("/approve.html")


    @h.json_response
    def get_by_id(self, id, **kwargs):
        return ("req_object", Requisition.get_as_dict(id=id))

    @h.json_response
    def get(self, id=None, **kwargs):
        return ("req_list", Requisition.get_as_dict(id=id))

    @h.json_response
    def get_open(self, **kwargs):
        return ("openreqs_list", Requisition.get_open())

    @h.json_response
    def get_approved(self, **kwargs):
        return ("approvedreqs_list", ApprovedRequisition.get_as_dict(id=None))


    @h.json_response
    @h.commit_or_rollback
    def new(self, **kwargs):
        date_required = request.params['datereq']
        description = request.params['reqdesc']
        organization = request.params['organization']
        fullname = request.params['fullname']
        phone_number = request.params['phone']

        req = Requisition.create(date_required, description, organization, fullname, phone_number)
        return ("object", req.todict())

    @h.json_response
    @h.commit_or_rollback
    def approve_req(self, id, **kwargs):
        req = Requisition.get(id=id)

        user_id = request.params['user_id']
        req.approve(id, user_id)

    @h.json_response
    @h.commit_or_rollback
    def close(self, **kwargs):
        req_id = request.params['req_id']

        items_status = LineItem.get_items_status(req_id)

        for item_status in items_status:
            if item_status != 2:
                return False

        req = Requisition.get(req_id)
        ret_val = req.close()

        if ret_val != None:
            return ("error", ret_val)
        else:
            return ("ok", ret_val)
