import logging

from omnia.lib.base import *

log = logging.getLogger(__name__)

class PurchaseOrderController(BaseController):

    def index(self):
        return render('/purchase_order.html')
