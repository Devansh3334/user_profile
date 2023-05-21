from .serializers import UserSerializear, UserUpdateSerializear
from .models import User
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


# Create your views here.

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializear

    def post(self, request, *args, **kwargs):
        serializer = UserSerializear(data=request.data)
        serializer.validate_username(request.data['username'])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"user": serializer.data, 'msg': 'Registration Successful'})


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    obj = User.objects.filter(username=username)
    if not obj:
        return Response({"message": "Invalid Credentials"})
    else:
        data = list(obj.values('status'))
        data = data[0]
        data = data['status']
        if data == 3:
            return Response({"message": "user is not exists"})
        else:
            if username is None or password is None:
                return Response({'error': 'Please provide both username and password'},
                                status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(username=username, password=password)
            if not user:
                return Response({'error': 'Invalid Credentials'})
            token = get_token_for_user(user)
            return Response({'token': token}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_user(request, user_id):
    if request.user.id == user_id:
        try:
            emp = User.objects.get(pk=user_id)
            data = UserUpdateSerializear(instance=emp, data=request.data, partial=True)
            if data.is_valid():
                data.save()
                return Response(data.data, status=status.HTTP_200_OK)
            else:
                return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("message:You have no access to change another user details")


@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        emp = get_object_or_404(User, pk=user_id)
        if request.user.id == emp.id:
            emp.status = 3
            emp.save()
            return Response({"deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response("message : you have no access to delete another user ")
    except User.DoesNotExist:
        return Response(data={}, status=status.HTTP_404_NOT_FOUND)
