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
            2009: 2009,
            2010: 2010,
            2011: 2011,
            2012: 2012
        }

    #}}}

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
    full_name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.now())
    date_closed = Column(DateTime)
    status = Column(Integer, default='0', nullable=False)

    def __init__(self, date_required, description, organization, full_name, phone_number):
        self.date_required = date_required
        self.description = description
        self.organization = organization
        self.full_name = full_name
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
                    "full_name": self.full_name,
                    "phone_number": self.phone_number,
                    "date_created": str(self.date_created),
                    "date_closed": str(self.date_closed),
                    "status": Requisition.STATUS_MAP[int(self.status)],
                    "lineitems": [lineitem.todict() for lineitem in self.lineitems]
                }

    def add_line_item(self, name, itemtype, specification, quantity, unitprice, vendorid):
        self.lineitems.append(LineItem(name, itemtype, specification, quantity, unitprice, vendorid))

    @staticmethod
    def get_line_items(id):
        line_items = [li.todict() for li in meta.session.query(LineItem).filter_by(requisitionid=id)]
        return line_items

    @staticmethod
    def get_open():
        reqs = [r.todict() for r in meta.session.query(Requisition).filter_by(status=0)]
        return reqs

    @staticmethod
    def get_approved():
        return [r.todict() for r in meta.session.query(Requisition).filter_by(status=1)]

    def approve(self, id, user_id):
        self.status = 1
        self.approvedrequisition = ApprovedRequisition(id, user_id)

    #}}}

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
            print_exc()

    #}}}

class PurchaseOrder(Base):#{{{
    __tablename__ = 'purchaseorder'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True)
    vendorid = Column(Integer, ForeignKey('vendor.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    total_amount = Column(Integer, default='0', nullable=False)
    status = Column(Integer, default='0', nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.now())
    date_closed = Column(DateTime)

    def __init__(self, vendor_id):
        self.vendorid = vendor_id
        self.date_created = datetime.datetime.now()

    STATUS_MAP = {
                    0: "Open", 
                    1: "Closed"
                }

    @staticmethod
    def create(vendor):
        po = PurchaseOrder(vendor)
        meta.session.add(po)
        meta.session.flush()
        return po.todict()

    def todict(self):
        return  {
                    "id": self.id,
                    "vendorid": self.vendorid,
                    "total_amount": self.total_amount,
                    "status": PurchaseOrder.STATUS_MAP[int(self.status)],
                    "line_items": [li.todict() for li in self.lineitems],
                    "date_created": str(self.date_created),
                    "date_closed": str(self.date_closed)
                }

    @staticmethod
    def get(id=None):
        try:
            if id:
                return meta.session.query(PurchaseOrder).filter_by(id=id).one()
            else:
                return [po for po in meta.session.query(PurchaseOrder)]
        except Exception, e:
            print_exc()

    @staticmethod
    def get_as_dict(id=None):
        try:
            if id:
                return meta.session.query(PurchaseOrder).filter_by(id=id).one().todict()
            else:
                return [po.todict() for po in meta.session.query(PurchaseOrder)]
        except Exception, e:
            print_exc()

    #}}}

class Vendor(Base):#{{{
    __tablename__ = 'vendor'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    address = Column(Text)
    phone = Column(String(20), nullable=False)

    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    @staticmethod
    def create(name, address, phone):
        vendor = Vendor(name, address, phone)
        meta.session.add(vendor)
        meta.session.flush()
    
    @staticmethod
    def get_as_dict(id=None):
        try:
            if id:
                return meta.session.query(Vendor).filter_by(id=id).one().todict()
            else:
                return [v.todict() for v in meta.session.query(Vendor)]
        except Exception, e:
            print_exc()

    def approved_line_items(self):
        return [
            vl.todict() for vl in meta.session.query(Vendor).filter_by(id=self.id).one().lineitems if vl.requisitionid in 
                [ar.requisitionid for ar in meta.session.query(ApprovedRequisition)]
                and vl.status == 0
            ]

    # How do I extract id and name from get_as_dict() dictionary such that I would not 
    # need to write these two functions, get_name_dict() and to_name_dict()?
    @staticmethod
    def get_names():
        return [v.to_name_dict() for v in meta.session.query(Vendor)]

    @staticmethod
    def get_vendors_with_line_items():
        # Bug: To avoid creating POs without having line items to add,
        # I decided to return only vendor objects that have line items to the create PO template.
        # But if a vendor object used to have line items and one or more have been ordered,
        # It should only be returned if it still has unordered line items.
        # The opposite is happening here.

        # Solution: Remove all line items which have status:1 (I don't know how they got here 'cos I'm returning only line items with status:0<see approved_line_items() above>) from vendor lineitems list before returning vendor object list
        for v in meta.session.query(Vendor):
            line_items = v.lineitems
            #Bug: When remove() is done through a loop or list comprehension, it leaves one value in list even if all values meet requirement for removal. We might have to come back to this later.
            [line_items.remove(l) for l in line_items if l.status == 1]
            print line_items

        return [v.to_name_dict() for v in meta.session.query(Vendor) if v.lineitems != []]

    def to_name_dict(self):
        return  {
            "id": self.id,
            "name": self.name
        }

    def todict(self):
        return  {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            # Vendor objects contain only approved line items
            "lineitems": self.approved_line_items()
        }#}}}

class LineItem(Base):#{{{
    __tablename__ = 'lineitem'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    itemtype = Column(String(100), nullable=False)
    specification = Column(Text)
    quantity = Column(Integer, default='0', nullable=False)
    unitprice = Column(Integer, nullable=False)
    totalprice = Column(Integer, nullable=False)
    vendorid = Column(Integer, ForeignKey('vendor.id', ondelete='RESTRICT', onupdate='CASCADE'))
    requisitionid = Column(Integer, ForeignKey('requisition.id', ondelete='RESTRICT', onupdate='CASCADE'))
    purchaseorderid = Column(Integer, ForeignKey('purchaseorder.id', ondelete='RESTRICT', onupdate='CASCADE'))
    status = Column(Integer, default='0', nullable=False)

    requisition = relation(Requisition, backref=backref('lineitems', order_by=id))
    vendor = relation(Vendor, backref=backref('lineitems', order_by=id))
    purchaseorder = relation(PurchaseOrder, backref=backref('lineitems', order_by=id))

    STATUS_MAP = {
                    0: "Requested", 
                    1: "Ordered",
                    2: "Delivered",
                    3: "Deployed"
                }

    def __init__(self, name, itemtype, specification, quantity, unitprice, vendorid):
        self.name = name
        self.itemtype = itemtype
        self.specification = specification
        self.quantity = quantity
        self.unitprice = unitprice
        self.totalprice = int(quantity) * int(unitprice)
        self.vendorid = vendorid

    @staticmethod
    def get(id=None):
        try:
            if id:
                return meta.session.query(LineItem).filter_by(id=id).one()
            else:
                return [li for li in meta.session.query(LineItem)]
        except Exception, e:
            print_exc()

    def todict(self):
        return  {
            "id": self.id,
            "name": self.name,
            "itemtype": self.itemtype,
            "specification": self.specification,
            "quantity": self.quantity,
            "unitprice": self.unitprice,
            "totalprice": self.totalprice,
            "vendorid": self.vendorid,
            "requisitionid": self.requisitionid,
            "purchaseorderid": self.purchaseorderid,
            "status": LineItem.STATUS_MAP[int(self.status)]
        }

    def remove_from_PO(self):
        pass

    def order(self, unitprice, purchaseorderid):
        self.unitprice = unitprice
        self.purchaseorderid = purchaseorderid
        self.totalprice = int(unitprice) * int(self.quantity)
        self.status = 1

        po = PurchaseOrder.get(purchaseorderid)
        po.total_amount = po.total_amount + self.totalprice
    
    #}}}

class Item(Base):#{{{
    __tablename__ = 'item'
    __table_args__ = {'mysql_engine': 'innodb'}

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    type = Column(String(100), nullable=False)

    def __init__(self, name, type):
        self.name = name
        self.type = type

    @staticmethod
    def create(name, type):
        item = Item(name, type)
        meta.session.add(item)
        meta.session.flush()

    def todict(self):
        return  {
            "id": self.id,
            "name": self.name,
            "type": self.type,
        }

    @staticmethod
    def types():
        return lst_to_dictlst(set([i.type for i in meta.session.query(Item)]))

    @staticmethod
    def item_by_type(type):
        return lst_to_dictlst([i.name for i in meta.session.query(Item).filter_by(type=type)])
    
    #}}}

# Refactor these helpers and add them to Misc#{{{

def user_dict(id):
    return meta.session.query(User).filter_by(id=id).one().todict()

def req_dict(id):
    return meta.session.query(Requisition).filter_by(id=id).one().todict()

def lst_to_dictlst(lst):
    new_lst = []

    for t in lst:
        type = {}
        type['id'] = t
        type['name'] = t
        new_lst.append(type)

    return new_lst#}}}
