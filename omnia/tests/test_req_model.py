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

        self.req = Requisition.create("2002-01-01 00:00:00", "Cars", "Engineering", "Adedayo Olukoya", "08033442234")
        self.user = User.create("deone", "dune369", "Dayo", "Osikoya", "Administrator")
        self.vendor = Vendor.create("Toyota Nigeria", "Isolo Way", "08023456789")
        self.item = Item.create("Corolla 09", "Vehicle")
        h.commit()

    def tearDown(self):
        self.prepare()
        meta.metadata.drop_all(bind=self.engine)

    def test_create(self):
        assert self.req.id == 1
        assert self.req.date_required == datetime.datetime(2002, 1, 1, 00, 00, 00)
        assert self.req.description == "Cars"
        assert self.req.organization == "Engineering"
        assert self.req.full_name == "Adedayo Olukoya"
        assert self.req.phone_number == "08033442234"

    def test_get(self):
        res = Requisition.get(id=1)
        assert res.id == 1
        assert res.date_required == datetime.datetime(2002, 1, 1, 00, 00, 00)
        assert res.description == "Cars"
        assert res.organization == "Engineering"
        assert res.full_name == "Adedayo Olukoya"
        assert res.phone_number == "08033442234"

        res = Requisition.get()
        assert res[0].id == 1
        assert res[0].description == "Cars"
        assert res[0].date_required == datetime.datetime(2002, 1, 1, 00, 00, 00)
        assert res[0].organization == "Engineering"
        assert res[0].full_name == "Adedayo Olukoya"
        assert res[0].phone_number == "08033442234"

    def test_get_as_dict(self):
        res = Requisition.get_as_dict(id=1)
        assert res['id'] == 1
        assert res['date_required'] == "2002-01-01 00:00:00"
        assert res['description'] == "Cars"
        assert res['organization'] == "Engineering"
        assert res['full_name'] == "Adedayo Olukoya"
        assert res['phone_number'] == "08033442234"

        res = Requisition.get_as_dict()
        assert res[0]['id'] == 1
        assert res[0]['date_required'] == "2002-01-01 00:00:00"
        assert res[0]['description'] == "Cars"
        assert res[0]['organization'] == "Engineering"
        assert res[0]['full_name'] == "Adedayo Olukoya"
        assert res[0]['phone_number'] == "08033442234"

    def test_add_line_item(self):
        self.req.add_line_item("Corolla 09", "Vehicle", "2009 Model", 5, 3000000, 1)
        h.commit()
        res = Requisition.get(id=1)
        assert res.lineitems[0].name == "Corolla 09"
        assert res.lineitems[0].itemtype == "Vehicle"
        assert res.lineitems[0].specification == "2009 Model"
        assert res.lineitems[0].quantity == 5
        assert res.lineitems[0].unitprice == 3000000
        assert res.lineitems[0].vendorid == 1

    def test_get_line_items(self):
        self.req.add_line_item("Toyota Camry", "Vehicle", "Model Corolla 09", 5, 300000, 1)
        self.req.add_line_item("Toyota Avensis", "Vehicle", "Model 2010", 10, 400000, 1)

        line_items = self.req.get_line_items(1)

        assert line_items[0]['name'] == "Toyota Camry"
        assert line_items[0]['itemtype'] == "Vehicle"
        assert line_items[0]['specification'] == "Model Corolla 09"
        assert line_items[0]['quantity'] == 5
        assert line_items[0]['unitprice'] == 300000
        assert line_items[0]['vendorid'] == 1

    def test_get_open(self):
        open_reqs = Requisition.get_open()

        assert open_reqs[0]['status'] == "Open"

    def test_approve(self):
        self.req.approve(1, 1)
        h.commit()

        assert self.req.approvedrequisition.requisitionid == self.req.id
        assert self.req.approvedrequisition.userid == self.user.id

    def test_get_approved(self):
        self.req.approve(1, 1)

        approved_reqs = Requisition.get_approved()
        assert approved_reqs[0]['status'] == "Approved"
