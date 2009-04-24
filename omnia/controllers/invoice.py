import logging

from omnia.lib.base import *

import omnia.model.helpers as h
from omnia.model.models import *

log = logging.getLogger(__name__)

class InvoiceController(BaseController):

    def index(self):
        return render('/invoices.html')

    def create(self):
        c.po_id = request.params['po_id']
        return render('/create_invoice.html')

    def view(self, id):
        c.inv_no = id
        return render('/invoice.html')

    def edit(self, id):
        c.inv_no = id
        return render('/edit_invoice.html')

    def add_item(self, id):
        c.invoice_no = id
        return render('/add_inv_item.html')

    @h.json_response
    def get_by_no(self, id, **kwargs):
        return ("invoice_object", Invoice.get_as_dict(no=id))

    @h.json_response
    @h.commit_or_rollback
    def new(self, **kwargs):
        invoice_no = request.params['invoice_no']
        po_id = request.params['po_id']
        vendor_id = request.params['vendor_id']
        user_id = request.params['user_id']

        invoice = Invoice.create(invoice_no, po_id, vendor_id, user_id)

        return ("invoice_object", invoice)
