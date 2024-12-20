from my_app.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse



@csrf_exempt
def home(request):
    return HttpResponse("Your Test response")

# View for user registration
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = MyUserSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                return Response({"message": "User Registered Successfully"}, status=status.HTTP_201_CREATED)
                       
        except:
            context = {
                "User Registaration Error": serializer.errors,
                "Valid Role Types" : "'admin', 'manager' or 'employee' "
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)



# View for user login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        # Check if email exists
        chkEmail = MyUser.objects.filter(email=email).first()
        if not chkEmail:
            return Response({'msg': 'Email Not Found, Please Register first'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Authenticate the user using the custom Backend
            user = authenticate(email=email, password=password)
            
            # Check if Authentication is successful
            if user is None:
                return Response({"msg": "Invalid login credentials"}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"msg": "Login Succesful"}, status=status.HTTP_200_OK)

        except ValidationError as e:
            # Catch ValidationError (for time restrictions) and return appropriate message
            return Response({"msg": "User Time Out"}, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            # Handle unexpected errors
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
