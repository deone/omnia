"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('error/:action/:id', controller='error')

    # CUSTOM ROUTES HERE
    map.connect('root', '/', controller='auth', action='index')
    map.connect('logout', '/logout', controller='auth', action='logout')

    map.connect('misc', '/misc/:action', controller='misc')

    map.connect('vendor', '/vendor/:action', controller='vendor')
    map.connect('vendor_action', '/vendor/:id/:action', controller='vendor')

    map.connect('item', '/item/:action', controller='item')
    map.connect('item_others', '/item/:action/:type', controller='item')

    map.connect('requisition', '/requisition', controller='requisition', action='index')
    map.connect('requisition_action', '/requisition/:action', controller='requisition')
    map.connect('requisition_others', '/requisition/:id/:action', controller='requisition')

    map.connect('lineitem_action', '/lineitem/:action', controller='lineitem')
    map.connect('lineitem_others', '/lineitem/:id/:action', controller='lineitem')

    map.connect('invoice_action', '/invoice/:action', controller='invoice')
    map.connect('invoice_other', '/invoice/:id/:action', controller='invoice')

    map.connect('purchase_order', '/purchase_order', controller='purchase_order', action='index')
    map.connect('purchase_order_action', '/purchase_order/:action', controller='purchase_order')
    map.connect('purchase_order_other', '/purchase_order/:id/:action', controller='purchase_order')
    
    map.connect(':controller/:action/:id')
    map.connect('*url', controller='template', action='view')

    return map
