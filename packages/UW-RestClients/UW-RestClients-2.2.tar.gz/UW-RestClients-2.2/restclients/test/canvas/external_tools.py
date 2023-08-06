from django.test import TestCase
from restclients.canvas.external_tools import ExternalTools


class CanvasTestExternalTools(TestCase):
    def test_get_external_tools_in_account(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = ExternalTools()

            tools = canvas.get_external_tools_in_account('12345')

            self.assertEquals(len(tools), 12, "Correct tools length")
            self.assertEquals(tools[10]['name'], "Tool", "Name is Correct")

    def test_get_external_tools_in_course_by_sis_id(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = ExternalTools()

            tools = canvas.get_external_tools_in_course_by_sis_id('2015-autumn-UWBW-301-A')

            self.assertEquals(len(tools), 2, "Correct tools length")
            self.assertEquals(tools[1]['name'], 'Course Tool', "Has correct tool name")

    def test_get_sessionless_launch_from_account_sis_id(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = ExternalTools()

            launch = canvas.get_sessionless_launch_url_from_account('54321', '12345')

            self.assertEquals(launch['id'], 54321, "Has correct tool id")

    def test_get_sessionless_launch_from_course_sis_id(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = ExternalTools()

            launch = canvas.get_sessionless_launch_url_from_course_sis_id('54321', '2015-autumn-UWBW-301-A')

            self.assertEquals(launch['id'], 54321, "Has correct tool id")

