from omnia.tests import *

class TestItemController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='item'))
        # Test response...
