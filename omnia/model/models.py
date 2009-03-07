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

    id = Column(Integer, primary_key=True, nullable=False)
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

class Requisition(Base):
    __tablename__ = 'requisition'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(Text, nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.now())
    date_closed = Column(DateTime)
    status = Column(Integer, default='0', nullable=False)

    def __init__(self, desc):
        self.description = desc
        self.date_created = datetime.datetime.now()

    @staticmethod
    def create(desc):
        req = Requisition(desc)
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
                    0: "open", 
                    1: "approved",
                    2: "disapproved",
                    3: "closed"
                }

    def todict(self):
        return  {
                    "id": self.id,
                    "description": self.description,
                    "date_created": str(self.date_created),
                    "date_closed": str(self.date_closed),
                    "status": Requisition.STATUS_MAP[int(self.status)],
                    "items": [item.todict() for item in self.items]
                }

    def add_item(self, quantity, name, description, unitprice):
        self.items.append(Item(quantity, name, description, unitprice))

    @staticmethod
    def get_items(id):
        items = [i.todict() for i in meta.session.query(Item).filter_by(requisitionid=id)]
        return items

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

        return approved

def user_dict(id):
    return meta.session.query(User).filter_by(id=id).one().todict()

def req_dict(id):
    return meta.session.query(Requisition).filter_by(id=id).one().todict()

class ApprovedRequisition(Base):
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
            print_exc()

class Order(Base):
    __tablename__ = 'order'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True, nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String(50))
    date_created = Column(DateTime, default=datetime.datetime.now())
    date_closed = Column(DateTime, default=datetime.datetime.now())
    requisitionid = Column(Integer, ForeignKey('requisition.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    vendorid = Column(Integer, ForeignKey('vendor.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)

class Item(Base):
    __tablename__ = 'item'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    unitprice = Column(Integer, nullable=False, default='0')
    requisitionid = Column(Integer, ForeignKey('requisition.id', ondelete='RESTRICT', onupdate='CASCADE'))
    orderid = Column(Integer, ForeignKey('order.id', ondelete='RESTRICT', onupdate='CASCADE'))

    requisition = relation(Requisition, backref=backref('items', order_by=id))
    order = relation(Order, backref=backref('items', order_by=id))

    def __init__(self, quantity, name, description, unitprice):
        self.quantity = quantity
        self.name = name
        self.description = description
        self.unitprice = unitprice

    def todict(self):
        return  {
            "id": self.id,
            "quantity": self.quantity,
            "name": self.name,
            "description": self.description,
            "unitprice": self.unitprice
        }

class Vendor(Base):
    __tablename__ = 'vendor'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(200), nullable=False)
    address = Column(Text)
    phone = Column(Integer)
