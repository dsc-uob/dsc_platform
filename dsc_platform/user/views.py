from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegistrationSerializer
from .models import User
from rest_framework_simplejwt.authentication import authentication

# Create your views here.


class RegisterView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        status_code = status.HTTP_201_CREATED
        response = {
            'success': True,
            'status_code': status_code,
            'message': 'User created successfully'
        }

        return Response(response, status=status_code)


class UserProfileView(RetrieveAPIView):
    permistion_classes = (IsAuthenticated)

    def get(self, request):
        if request.user.is_authenticated:
            try:
                user = User.objects.get(id=request.user.id)

                status_code = status.HTTP_200_OK

                response = {
                    'success': True,
                    'data': {

                        'first_name': user.first_name,
                        'last_name': '' if user.last_name is None else user.last_name,
                        'username': user.username,
                        'phone_number': '' if user.phone_number is None else user.phone_number,
                        'birth_date': user.birth_date,
                        'gender': user.gender,
                        'is_active': user.is_active,
                        'is_staff': user.is_staff,
                    }
                }

            except Exception as e:
                status_code = status.HTTP_400_BAD_REQUEST
                response = {
                    'success': False,
                    'status code': status.HTTP_400_BAD_REQUEST,
                    'message': 'user does not exists',
                    'error': str(e)
                }

        else:
            status_code = status.HTTP_401_UNAUTHORIZED

            response = {
                'success': False,
                'status code': status.HTTP_401_UNAUTHORIZED,
                'message': 'missing authorization header',
            }
        return Response(response, status=status_code)
