from omnia.tests import *

class TestRequisitionController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='requisition'))
        # Test response...
