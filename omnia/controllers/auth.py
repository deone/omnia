import logging

from omnia.lib.base import *
import omnia.model.helpers as h
from omnia.model.models import *

log = logging.getLogger(__name__)

class User(object):
    def __init__(self, user_obj):
        self.username = user_obj.username
        self.id = user_obj.id
        self.roles = user_obj.roles
        self.firstname = user_obj.firstname
        self.lastname = user_obj.lastname

class AuthController(BaseController):

    def index(self):
        return render("/index.html")

    @h.json_response
    def login(self, **kwargs):
        username = request.params['username']
        password = request.params['password']

        user = h.authenticate(username, password)

        if not user:
            return ("error", "Login failed")
        else:
            session['user'] = User(user)
            session.save()

            return ("user", user.todict())
