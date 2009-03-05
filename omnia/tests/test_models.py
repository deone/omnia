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

    def test_create(self):
        req = Requisition.create("Cars")
        h.commit()

        assert req.id == 1
        assert req.description == "Cars"

    def test_get(self):
        req = Requisition.create("Cars")

        res = Requisition.get(id=1)
        assert res.id == 1
        assert res.description == "Cars"

        res = Requisition.get()
        assert res[0].id == 1
        assert res[0].description == "Cars"

    def test_get_as_dict(self):
        req = Requisition.create("Cars")

        res = Requisition.get_as_dict(id=1)
        assert res['id'] == 1
        assert res['description'] == "Cars"

    def test_add_item(self):
        req = Requisition.create("Cars")

        req.add_item(5, "Toyota", "Model Corolla 09", 30000)
        res = Requisition.get(id=1)
        assert res.items[0].quantity == 5
        assert res.items[0].name == "Toyota"
        assert res.items[0].description == "Model Corolla 09"
        assert res.items[0].unitprice == 30000

    def test_get_items(self):
        req = Requisition.create("Cars")
        req.add_item(5, "Toyota", "Model Corolla 09", 30000)
        req.add_item(10, "Rolls Royce", "Model Flyer 2010", 50000)

        items = req.get_items(1)
        assert items[0]['name'] == "Toyota"
        assert items[0]['description'] == "Model Corolla 09"
        assert items[0]['unitprice'] == 30000

        assert items[1]['name'] == "Rolls Royce"
        assert items[1]['description'] == "Model Flyer 2010"
        assert items[1]['unitprice'] == 50000

    def test_get_open(self):
        req = Requisition.create("Cars")
        req = Requisition.create("Sports Wear")
        req = Requisition.create("Salary")
        req = Requisition.create("Provisions")

        open_reqs = Requisition.get_open()
        open_reqs[0]['status'] == "open"
        open_reqs[1]['status'] == "open"
        open_reqs[2]['status'] == "open"
        open_reqs[3]['status'] == "open"
