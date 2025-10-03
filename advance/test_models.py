
from django.test import TestCase
from .models import Setting
import json

class SettingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Setting.objects.create(name="test_str", value="hello", value_type="str")
        Setting.objects.create(name="test_int", value="123", value_type="int")
        Setting.objects.create(name="test_bool_true", value="True", value_type="bool")
        Setting.objects.create(name="test_bool_false", value="False", value_type="bool")
        Setting.objects.create(name="test_float", value="123.45", value_type="float")
        Setting.objects.create(name="test_json", value='{"key": "value"}', value_type="json")

    def test_get_value_str(self):
        setting = Setting.objects.get(name="test_str")
        self.assertEqual(setting.get_value(), "hello")

    def test_get_value_int(self):
        setting = Setting.objects.get(name="test_int")
        self.assertEqual(setting.get_value(), 123)

    def test_get_value_bool_true(self):
        setting = Setting.objects.get(name="test_bool_true")
        self.assertTrue(setting.get_value())

    def test_get_value_bool_false(self):
        setting = Setting.objects.get(name="test_bool_false")
        self.assertFalse(setting.get_value())

    def test_get_value_float(self):
        setting = Setting.objects.get(name="test_float")
        self.assertEqual(setting.get_value(), 123.45)

    def test_get_value_json(self):
        setting = Setting.objects.get(name="test_json")
        self.assertEqual(setting.get_value(), {"key": "value"})

    def test_set_value_str(self):
        setting = Setting.objects.get(name="test_str")
        setting.set_value("world")
        self.assertEqual(setting.value, "world")

    def test_set_value_int(self):
        setting = Setting.objects.get(name="test_int")
        setting.set_value(456)
        self.assertEqual(setting.value, "456")

    def test_set_value_bool(self):
        setting = Setting.objects.get(name="test_bool_true")
        setting.set_value(False)
        self.assertEqual(setting.value, "False")

    def test_set_value_float(self):
        setting = Setting.objects.get(name="test_float")
        setting.set_value(54.321)
        self.assertEqual(setting.value, "54.321")

    def test_set_value_json(self):
        setting = Setting.objects.get(name="test_json")
        setting.set_value({"new_key": "new_value"})
        self.assertEqual(setting.value, '{"new_key": "new_value"}')
