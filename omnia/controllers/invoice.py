import logging

from omnia.lib.base import *

import omnia.model.helpers as h
from omnia.config.config import Config
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
    def get_by_poid(self, id, **kwargs):
        return ("invoice_object", Invoice.get_by_poid(id))

    @h.json_response
    @h.commit_or_rollback
    def new(self, **kwargs):
        invoice_no = request.params['invoice_no']
        amount = request.params['amount']
        po_id = request.params['po_id']
        vendor_id = request.params['vendor_id']
        user_id = request.params['user_id']

        po_amount = PurchaseOrder.get_amount(po_id)

        if int(amount) != int(po_amount):
            return ("error", "Invoice amount does not match PO amount.");

        invoice = Invoice.create(invoice_no, po_id, vendor_id, user_id, amount)

        warehouse = Warehouse.get(1)
        
        # Send email
        config = Config()
        server = config.get("mailserver", "server")
        port =  config.get("mailserver", "port")
        username = config.get("mailserver", "username") 
        password = config.get("mailserver", "password")
        
        sender = config.get("email", "sender")
        recipient = warehouse.manager_email

        subject = config.get("email", "subject2")
        message = "Hi " + User.get(warehouse.manager).firstname + " " + User.get(warehouse.manager).lastname + ",\r\n\r\n"
        message += "Invoice %s has been received for purchase order %s. %sRegards %s" % (invoice_no, po_id, "\r\n\r\n", "\r\n\r\n")

        h.send_mail(server, port, username, password, sender, recipient, subject, message)

        return ("invoice_object", invoice)
