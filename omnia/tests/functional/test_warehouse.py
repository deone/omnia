from omnia.tests import *

class TestWarehouseController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='warehouse'))
        # Test response...
