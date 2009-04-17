import logging

from omnia.lib.base import *

import omnia.model.helpers as h
from omnia.model.models import *

log = logging.getLogger(__name__)

class InvoiceController(BaseController):

    def create(self, id):
        c.po_id = request.params['po_id']
        return render('/create_invoice.html')

    @h.json_response
    @h.commit_or_rollback
    def new(self, **kwargs):
        invoice_no = request.params['invoice_no']
        po_id = request.params['po_id']
        vendor_id = request.params['vendor_id']
        user_id = request.params['user_id']

        invoice = Invoice.create(invoice_no, po_id, vendor_id, user_id)

        return ("invoice_object", invoice)
