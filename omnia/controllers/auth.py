import logging
import md5

from omnia.lib.base import *
import omnia.model.helpers as h
from omnia.model.models import *

log = logging.getLogger(__name__)

class AuthController(BaseController):

    def index(self):
        return render("/index.html")

    @h.json_response
    def login(self, **kwargs):
        username = request.params['username']
        password = request.params['password']

        user = h.authenticate(username, password)

