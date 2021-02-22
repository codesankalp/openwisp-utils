from collections import OrderedDict
from unittest import TestCase
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from openwisp_utils.admin_theme import (
    register_dashboard_chart,
    register_dashboard_template,
    unregister_dashboard_chart,
    unregister_dashboard_template,
)


class TestDashboardConfig(TestCase):
    @patch('openwisp_utils.admin_theme.dashboard.DASHBOARD_CHARTS', OrderedDict())
    def test_register_dashboard_chart(self):
        from openwisp_utils.admin_theme.dashboard import DASHBOARD_CHARTS

        dashboard_element = {
            'name': 'Test Chart',
            'query_params': {
                'app_label': 'app_label',
                'model': 'model_name',
                'group_by': 'property',
            },
            'colors': {'value1': 'red', 'value2': 'green'},
        }

        with self.subTest('Registering new dashboard element'):
            register_dashboard_chart(-1, dashboard_element)
            self.assertIn(-1, DASHBOARD_CHARTS)

        with self.subTest('Registering a chart at existing position'):
            with self.assertRaises(ImproperlyConfigured):
                register_dashboard_chart(-1, dashboard_element)

        with self.subTest('Unregistering a chart that does not exists'):
            with self.assertRaises(ImproperlyConfigured):
                unregister_dashboard_chart('Chart Test')

        with self.subTest('Unregistering "Test Chart"'):
            unregister_dashboard_chart('Test Chart')
            self.assertNotIn(-1, DASHBOARD_CHARTS)

    def test_miscellaneous_DASHBOARD_CHARTS_validation(self):
        with self.subTest('Registering with incomplete config'):
            with self.assertRaises(AssertionError):
                register_dashboard_chart(-1, dict())

        with self.subTest('Registering with invalid position argument'):
            with self.assertRaises(ImproperlyConfigured):
                register_dashboard_chart(['Test Chart'], dict())

        with self.subTest('Registering with invalid config'):
            with self.assertRaises(ImproperlyConfigured):
                register_dashboard_chart('Test Chart', tuple())

        with self.subTest('Unregistering with invalid name'):
            with self.assertRaises(ImproperlyConfigured):
                unregister_dashboard_chart(dict())

        with self.subTest('Test filters required when not group_by'):
            with self.assertRaises(AssertionError) as ctx:
                register_dashboard_chart(
                    -1,
                    {
                        'name': 'Test Chart',
                        'query_params': {
                            'app_label': 'app_label',
                            'model': 'model_name',
                            'annotate': {},
                        },
                    },
                )
            self.assertIn('filters', str(ctx.exception))

    @patch('openwisp_utils.admin_theme.dashboard.DASHBOARD_TEMPLATES', OrderedDict())
    def test_register_dashboard_template(self):
        from openwisp_utils.admin_theme.dashboard import DASHBOARD_TEMPLATES

        dashboard_element = {
            'template': 'password_change_done.html',
        }

        with self.subTest('Registering new dashboard template'):
            register_dashboard_template(-1, dashboard_element)
            self.assertIn(-1, DASHBOARD_TEMPLATES)
            self.assertEqual(DASHBOARD_TEMPLATES[-1], dashboard_element)

        with self.subTest('Registering a dashboard template at existing position'):
            with self.assertRaises(ImproperlyConfigured):
                register_dashboard_template(-1, dashboard_element)

        with self.subTest('Unregistering a dashboard template that does not exists'):
            with self.assertRaises(ImproperlyConfigured):
                unregister_dashboard_template('test.html')

        with self.subTest('Unregistering "password_change_done.html"'):
            unregister_dashboard_template('password_change_done.html')
            self.assertNotIn(-1, DASHBOARD_TEMPLATES)

    def test_miscellaneous_DASHBOARD_TEMPLATES_validation(self):
        with self.subTest('Registering with incomplete config'):
            with self.assertRaises(AssertionError):
                register_dashboard_template(-1, dict())

        with self.subTest('Registering with invalid position argument'):
            with self.assertRaises(ImproperlyConfigured):
                register_dashboard_template(['template.html'], dict())

        with self.subTest('Registering with invalid config'):
            with self.assertRaises(ImproperlyConfigured):
                register_dashboard_template(0, tuple())

        with self.subTest('Unregistering with invalid template path'):
            with self.assertRaises(ImproperlyConfigured):
                unregister_dashboard_template(dict())
