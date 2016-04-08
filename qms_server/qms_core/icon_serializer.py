from rest_framework.serializers import BaseSerializer


class IconSerializer(BaseSerializer):

    def to_representation(self, obj):
        return obj.icon
