"""

CONFIGURATOR VIEWS UNIT TESTS

"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from configurator.views import ConfigView


class TestUrls(SimpleTestCase):

    def test_config_view_url(self):
        url = reverse('config:Config', args=[1])
        self.assertEqual(resolve(url).func.view_class, ConfigView)
