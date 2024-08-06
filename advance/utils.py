from .models import Setting

def get_setting(name, default=None):
    try:
        setting = Setting.objects.get(name=name)
        return setting.get_value()
    except Setting.DoesNotExist:
        return default
