from Cronos_API.serializers import *

class ProfileSerializer(serializers.ModelSerializer):
    """ Serializer for Users """
    class Meta(object):
        model = Profiles
        fields = ["id", "first_name", "last_name"]