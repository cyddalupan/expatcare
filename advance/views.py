from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Setting
from .serializers import SettingSerializer

class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer

    @action(detail=False, methods=['get'], url_path='by-name/(?P<name>[^/.]+)')
    def get_by_name(self, request, name=None):
        """Custom action to retrieve a setting by name."""
        try:
            setting = Setting.objects.get(name=name)
            serializer = self.get_serializer(setting)
            return Response(serializer.data)
        except Setting.DoesNotExist:
            return Response({'detail': 'Setting not found.'}, status=404)
