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

        self.req = Requisition.create("Cars")
        self.user = User.create("deone", "dune369", "Dayo", "Osikoya", "Administrator")
        h.commit()

    def tearDown(self):
        self.prepare()
        meta.metadata.drop_all(bind=self.engine)

    def test_create(self):
        assert self.req.id == 1
        assert self.req.description == "Cars"

    def test_get(self):
        res = Requisition.get(id=1)
        assert res.id == 1
        assert res.description == "Cars"

        res = Requisition.get()
        assert res[0].id == 1
        assert res[0].description == "Cars"

    def test_get_as_dict(self):
        res = Requisition.get_as_dict(id=1)
        assert res['id'] == 1
        assert res['description'] == "Cars"

    def test_add_item(self):
        self.req.add_item(5, "Toyota", "Model Corolla 09", 30000)
        h.commit()
        res = Requisition.get(id=1)
        assert res.items[0].quantity == 5
        assert res.items[0].name == "Toyota"
        assert res.items[0].description == "Model Corolla 09"
        assert res.items[0].unitprice == 30000

    def test_get_items(self):
        self.req.add_item(5, "Toyota", "Model Corolla 09", 30000)
        self.req.add_item(10, "Rolls Royce", "Model Flyer 2010", 50000)

        items = self.req.get_items(1)
        assert items[0]['name'] == "Toyota"
        assert items[0]['description'] == "Model Corolla 09"
        assert items[0]['unitprice'] == 30000

        assert items[1]['name'] == "Rolls Royce"
        assert items[1]['description'] == "Model Flyer 2010"
        assert items[1]['unitprice'] == 50000

    def test_get_open(self):
        Requisition.create("Sports Wear")
        Requisition.create("Salary")
        Requisition.create("Provisions")
        h.commit()

        open_reqs = Requisition.get_open()
        open_reqs[0]['description'] == "Cars"
        open_reqs[1]['status'] == "open"
        open_reqs[2]['status'] == "open"
        open_reqs[3]['status'] == "open"

    def test_approve(self):
        self.req.approve(1, 1)
        h.commit()

        assert self.req.approvedrequisition.requisitionid == self.req.id
        assert self.req.approvedrequisition.userid == self.user.id
