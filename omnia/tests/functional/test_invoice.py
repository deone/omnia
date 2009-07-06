from omnia.tests import *

class TestInvoiceController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='invoice'))
        # Test response...
