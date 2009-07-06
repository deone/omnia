from omnia.tests import *

class TestReceivingController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='receiving'))
        # Test response...
