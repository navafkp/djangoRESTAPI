from rest_framework import serializers
from users.models import CustomUser, UserImage
class AdminCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'password']
        extra_kwargs = {
            'password': {'write_only':True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        
        
# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserImage
#         fields = '__all__'
        
