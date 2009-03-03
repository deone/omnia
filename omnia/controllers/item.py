import logging

from omnia.lib.base import *

import omnia.model.helpers as h
from omnia.model.models import *

log = logging.getLogger(__name__)

class ItemController(BaseController):

    @h.json_response
    @h.commit_or_rollback
    def new(self, id, **kwargs):
        return ("Hello World")
        
