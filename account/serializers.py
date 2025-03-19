from rest_framework import serializers
from django.contrib.auth.models import User

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','password') 
        #kol wahda mel les éléments hethike n7addou kifh tebdda required wela kol wahda shnua lazém naamloulha
        extra_kwargs = {
            'first_name': {'required':True,'allow_blank':False},
            'last_name' : {'required':True,'allow_blank':False},
            'email' : {'required':True,'allow_blank':False},
            'password' : {'required':True,'allow_blank':False}
            
        }
class UserSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ('first_name', 'last_name', 'email','password')