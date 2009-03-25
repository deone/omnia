from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.orm import exc as orm_exc
from traceback import print_exc

import datetime

from omnia.model import meta

Base = declarative_base()
meta.metadata = Base.metadata

class Misc(object):#{{{

    @staticmethod
    def days():
        return {
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9,
            10: 10,
            11: 11,
            12: 12,
            13: 13,
            14: 14,
            15: 15,
            16: 16,
            17: 17,
            18: 18,
            19: 19,
            20: 20,
            21: 21,
            22: 22,
            23: 23,
            24: 24,
            25: 25,
            26: 26,
            27: 27,
            28: 28,
            29: 29,
            30: 30,
            31: 31
        }

    @staticmethod
    def months():
        return {
            1: "January", 
            2: "February", 
            3: "March", 
            4: "April", 
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }

    @staticmethod
    def years():
        return {
            1990: 1990,
            1991: 1991,
            1992: 1992,
            1993: 1993,
            1994: 1994,
            1995: 1995,
            1996: 1996,
            1997: 1997,
            1998: 1998,
            1999: 1999,
            2000: 2000,
            2001: 2001,
            2002: 2002,
            2003: 2003,
            2004: 2004,
            2005: 2005,
            2006: 2006,
            2007: 2007,
            2008: 2008,
            2009: 2009
        }#}}}

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
                    "requisition_id": self.requisitionid,
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

class PurchaseOrder(Base):#{{{
    __tablename__ = 'purchaseorder'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    status = Column(String(50))
    date_created = Column(DateTime, default=datetime.datetime.now())
    date_closed = Column(DateTime, default=datetime.datetime.now())#}}}

class Vendor(Base):#{{{
    __tablename__ = 'vendor'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    address = Column(Text)
    phone = Column(String(20), nullable=False)
    
    @staticmethod
    def get():
        return dict([(i.id, i.name) for i in meta.session.query(Vendor)])#}}}

    @staticmethod
    def get_name_by_id(id):
        return meta.session.query(Vendor).filter_by(id=id).one().name

class LineItem(Base):#{{{
    __tablename__ = 'lineitem'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    itemtype = Column(String(100), nullable=False)
    specification = Column(Text)
    quantity = Column(Integer, nullable=False)
    unitprice = Column(Integer, nullable=False)
    vendorid = Column(Integer, ForeignKey('vendor.id', ondelete='RESTRICT', onupdate='CASCADE'))
    requisitionid = Column(Integer, ForeignKey('requisition.id', ondelete='RESTRICT', onupdate='CASCADE'))

    requisition = relation(Requisition, backref=backref('lineitems', order_by=id))
    vendor = relation(Vendor, backref=backref('lineitems', order_by=id))

    def __init__(self, name, itemtype, specification, quantity, unitprice, vendorid):
        self.name = name
        self.itemtype = itemtype
        self.specification = specification
        self.quantity = quantity
        self.unitprice = unitprice
        self.vendorid = vendorid

    def todict(self):
        return  {
            "id": self.id,
            "name": self.name,
            "itemtype": self.itemtype,
            "specification": self.specification,
            "quantity": self.quantity,
            "unitprice": self.unitprice,
            "vendor": Vendor.get_name_by_id(self.vendorid)
        }#}}}

class Item(Base):#{{{
    __tablename__ = 'item'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    type = Column(String(100), nullable=False)

    def todict(self):
        return  {
            "id": self.id,
            "name": self.name,
            "type": self.type,
        }

    @staticmethod
    def get():
        return dict([(i.id, i.name) for i in meta.session.query(Item)]) 

    @staticmethod
    def get_types():
        return dict([(i.type, i.type) for i in meta.session.query(Item)])

    @staticmethod
    def get_by_type(type):
        return dict([(i.name, i.name) for i in meta.session.query(Item).filter_by(type=type)])#}}}
