import logging

from omnia.lib.base import *

import omnia.model.helpers as h
from omnia.model.models import *

log = logging.getLogger(__name__)

class MiscController(BaseController):

    @h.json_response
    # Reverse fetch_dict's args seq. to look like json_response's
    # e.g self.fetch_dict("foobar_list", foobar())
    # so it should be defined: def fetch_dict(self, objtype, object, **kwargs):
    def fetch_dict(self, dct, objtype, **kwargs):
        res_lst = []

        for k, v in dct.iteritems():
            dict_lst = {}
            dict_lst['id'] = k
            dict_lst['name'] = v

            res_lst.append(dict_lst)

        return (objtype, res_lst)

    def get_months(self):
        return self.fetch_dict(Misc.months(), "month_optionlist")

    def get_years(self):
        return self.fetch_dict(Misc.years(), "year_optionlist")

    def get_days(self):
        return self.fetch_dict(Misc.days(), "day_optionlist")
