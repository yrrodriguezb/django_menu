from rest_framework import serializers
from apps.menu.models import Menu


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Menu

        fields = [ 
            'code',
            'name', 
            'path', 
            'level'
        ]

        read_only_fields = [
            'code',
        ]