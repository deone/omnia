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
    @h.commit_or_rollback
    def new(self, **kwargs):
        description = request.params['description']
        req = Requisition.create(description)

    @h.json_response
    def get(self, id, **kwargs):
        return ("requisition", Requisition.get(id))

    @h.json_response
    def get_all(self, **kwargs):
        return ("requisition", Requisition.get(id=None))
