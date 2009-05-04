import logging

from omnia.lib.base import *

log = logging.getLogger(__name__)

class ReceivingController(BaseController):

    def index(self):
        return render('/receiving.html')
