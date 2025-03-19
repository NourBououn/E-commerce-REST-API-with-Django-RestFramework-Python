from datetime import datetime
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

# Create your views here.
#les données mta3 l user bsh naamloulha add l database so we use POST

@api_view(['POST'])
def register(request):
    data = request.data 
    user = SignUpSerializer(data=data)
    
    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                username = data['email'],
                email = data['email'],
                password = make_password(data['password']),
            )
            return Response({'details':'Your account registerred successfully!'},status=status.HTTP_201_CREATED)
        else:
            return Response({'error':'This email already exists!'},status=status.HTTP_400_BAD_REQUEST)
    else:
        # n'a pas rempli les données
        return Response(user.errors)    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = SignUpSerializer(request.user)
    fields = ('first_name', 'last_name', 'email','password')
    return Response(user.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data
    
    user.first_name = data ['first_name']
    user.last_name = data ['last_name']
    user.email = data ['email']
    user.password = data ['password']
    
    #Lahne lazem naamlou condition aal password
    if data['password'] != "":
        user.password = make_password(data['password'])
        
    user.save()
    serializer = UserSerializer(user,many=False)
    return Response(serializer.data)


def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)

@api_view(['POST'])
def forget_password(request):
    data = request.data
    user = get_object_or_404(User,email=data['email'])
    token = get_random_string(40)
    expire_date = datetime.now()+datetime.timedelta(minutes=30)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()
    host = get_current_host(request)
    link = "http://localhost:8000/api/reset_password/token"
    body = "Your password reset link is : {link}".format(link=link)
    send_mail(
        "Password reset from eMarket",
        body,
        "emMarket@gmail.com",
        [data['email']]
    )
    
    return Response({'details':'Password reset sent to {email}'.format(email=data['email'])})

        
        