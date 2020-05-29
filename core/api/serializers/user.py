from rest_framework import serializers

from core.models import User

from rest_framework.serializers import(
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    FileField,
    BooleanField,
    IntegerField,

)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


# -----------------------------------------------------------------------------
# My forked version
# -----------------------------------------------------------------------------


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            "email",
            "is_superuser",
            "is_staff",
            "is_active",
            "mobile",
            "password",
        )
        
    extra_kwargs = {"password":
                        {"write_only": True}
                    }

    def validate(self, data):
        email = data['email']
        user_qs = User.objects.filter(email = email)
        if user_qs.exists():
            raise ValidationError("Email already exixts!!")
        return data
    

    def create(self, validated_data):
                
        username = validated_data['username']
        email = validated_data['email']
        name = validated_data["name"]
        password = validated_data['password']
        mobile = validated_data['mobile']
        
        user_obj = User(
            username = username,
            name = name,
            email = email,
            mobile = mobile,
        
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data    
