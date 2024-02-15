from Cronos_API.serializers import *

class UserSerializer(serializers.ModelSerializer):
    """ Serializer for Users """
    email = serializers.EmailField(
        validators = [
            UniqueValidator(
                queryset=User.objects.all(),
                message="This email already exists."
            )
        ]
    )
    class Meta(object):
        model = User
        fields = ["id", "username", "password", "email"]

    def create(self, validated_data) -> User:
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
