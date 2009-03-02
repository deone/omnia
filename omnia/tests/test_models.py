from unittest import TestCase
from sqlalchemy import create_engine

from omnia.model.models import *
from omnia.model import init_model
import omnia.model.meta as meta
import omnia.model.helpers as h

import datetime

class ModelTests(TestCase):
    def prepare(self):
        self.engine = create_engine("mysql://omnia:omnia@localhost/omnia_test")
        init_model(self.engine)

    def setUp(self):
        self.prepare()
        meta.metadata.create_all(bind=self.engine)

    def tearDown(self):
        self.prepare()
        meta.metadata.drop_all(bind=self.engine)

    def test_req_new(self):
        req = Requisition.create("Cars")
        h.commit()

        assert req.description == "Cars"
