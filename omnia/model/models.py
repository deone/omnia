from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.orm import exc as orm_exc
from traceback import print_exc

import datetime

from omnia.model import meta

Base = declarative_base()
meta.metadata = Base.metadata

class User(Base):#{{{
    __tablename__ = 'user'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    roles = Column(String(255), nullable=False)

    def __init__(self, username, password, firstname, lastname, roles):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.roles = roles

    @staticmethod
    def create(username, password, firstname, lastname, roles):
        user = User(username, password, firstname, lastname, roles)
        meta.session.add(user)
        return user

    @staticmethod
    def get(id=None, username=None):
        try:
            if id:
                return meta.session.query(User).filter_by(id=id).one()
            elif username:
                return meta.session.query(User).filter_by(username=username).one()
            else:
                return [u for u in meta.session.query(User)]
        except Exception, e:
            print_exc()

    def todict(self):
        return {
                'id': self.id,
                'firstname': self.firstname,
                'lastname': self.lastname,
                'roles': self.roles
                }#}}}

class Requisition(Base):#{{{
    __tablename__ = 'requisition'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True, nullable=False)
    date_required = Column(DateTime, default=datetime.datetime.now())
    description = Column(Text, nullable=False)
    organization = Column(String(100), nullable=False)
    fullname = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.now())
    date_closed = Column(DateTime)
    status = Column(Integer, default='0', nullable=False)

    def __init__(self, date_required, description, organization, fullname, phone_number):
        self.date_required = date_required
        self.description = description
        self.organization = organization
        self.fullname = fullname
        self.phone_number = phone_number
        self.date_created = datetime.datetime.now()


    @staticmethod
    def create(date_required, description, organization, fullname, phone_number):
        req = Requisition(date_required, description, organization, fullname, phone_number)
        meta.session.add(req)
        meta.session.flush()
        return req

    @staticmethod
    def get(id=None):
        try:
            if id:
                return meta.session.query(Requisition).filter_by(id=id).one()
            else:
                return [r for r in meta.session.query(Requisition)]
        except Exception, e:
            print_exc()

    @staticmethod
    def get_as_dict(id=None):
        try:
            if id:
                return meta.session.query(Requisition).filter_by(id=id).one().todict()
            else:
                return [r.todict() for r in meta.session.query(Requisition)]
        except Exception, e:
            print_exc()

    STATUS_MAP = {
                    0: "Open", 
                    1: "Approved",
                    2: "Disapproved",
                    3: "Closed"
                }

    def todict(self):
        return  {
                    "id": self.id,
                    "date_required": str(self.date_required),
                    "description": self.description,
                    "organization": self.organization,
                    "full_name": self.fullname,
                    "phone_number": self.phone_number,
                    "date_created": str(self.date_created),
                    "date_closed": str(self.date_closed),
                    "status": Requisition.STATUS_MAP[int(self.status)],
                    "items": [lineitem.todict() for lineitem in self.lineitems]
                }

    def add_item(self, name, itemtype, specification, quantity, unitprice, vendor):
        self.lineitems.append(LineItem(name, itemtype, specification, quantity, unitprice, vendor))

    @staticmethod
    def get_line_items(id):
        line_items = [li.todict() for li in meta.session.query(LineItem).filter_by(requisitionid=id)]
        return line_items

    @staticmethod
    def get_open():
        reqs = [r.todict() for r in meta.session.query(Requisition).filter_by(status=0)]
        return reqs

    def approve(self, id, user_id):
        self.status = 1
        self.approvedrequisition = ApprovedRequisition(id, user_id)

    @staticmethod
    def get_approved():
        approved = []
        for r in meta.session.query(Requisition).filter_by(status=1):
            approved.append(r.todict())

        return approved#}}}

def user_dict(id):
    return meta.session.query(User).filter_by(id=id).one().todict()

def req_dict(id):
    return meta.session.query(Requisition).filter_by(id=id).one().todict()

class ApprovedRequisition(Base):#{{{
    __tablename__ = 'approvedrequisition'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True)
    requisitionid = Column(Integer, ForeignKey('requisition.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    userid = Column(Integer, ForeignKey('user.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)

    requisition = relation(Requisition, backref=backref('approvedrequisition', uselist=False))
    user = relation(User, backref=backref('approvedrequisitions', order_by=id))

    def __init__(self, req_id, user_id):
        self.requisitionid = req_id
        self.userid = user_id

    def todict(self):
        return  {
                    "id": self.id,
                    "requisition": req_dict(self.requisitionid),
                    "user": user_dict(self.userid)
                }

    @staticmethod
    def get_as_dict(id=None):
        try:
            if id:
                return meta.session.query(ApprovedRequisition).filter_by(id=id).one().todict()
            else:
                return [ar.todict() for ar in meta.session.query(ApprovedRequisition)]
        except Exception, e:
            print_exc()#}}}

class Order(Base):#{{{
    __tablename__ = 'order'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    status = Column(String(50))
    date_created = Column(DateTime, default=datetime.datetime.now())
    date_closed = Column(DateTime, default=datetime.datetime.now())
    requisitionid = Column(Integer, ForeignKey('requisition.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    vendorid = Column(Integer, ForeignKey('vendor.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)#}}}

class LineItem(Base):
    __tablename__ = 'lineitem'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    itemtype = Column(String(100), nullable=False)
    specification = Column(Text)
    quantity = Column(Integer, nullable=False)
    unitprice = Column(Integer, nullable=False)
    vendor = Column(String(100), nullable=False)
    requisitionid = Column(Integer, ForeignKey('requisition.id', ondelete='RESTRICT', onupdate='CASCADE'))

    requisition = relation(Requisition, backref=backref('lineitems', order_by=id))

    def __init__(self, name, itemtype, specification, quantity, unitprice, vendor):
        self.name = name
        self.itemtype = itemtype
        self.specification = specification
        self.quantity = quantity
        self.unitprice = unitprice
        self.vendor = vendor

    def todict(self):
        return  {
            "id": self.id,
            "name": self.name,
            "itemtype": self.itemtype,
            "specification": self.specification,
            "quantity": self.quantity,
            "unitprice": self.unitprice,
            "vendor": self.vendor
        }

class Vendor(Base):
    __tablename__ = 'vendor'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    address = Column(Text)
    phone = Column(String(20), nullable=False)

class Item(Base):
    __tablename__ = 'item'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    type = Column(String(100), nullable=False)
    vendorid = Column(Integer, ForeignKey('vendor.id', ondelete='RESTRICT', onupdate='CASCADE'))

    vendor = relation(Vendor, backref=backref('items', order_by=id))
