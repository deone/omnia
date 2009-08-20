import logging

from omnia.lib.base import *

log = logging.getLogger(__name__)

class DashboardController(BaseController):

    def index(self):
        return render("/dashboard.html")
