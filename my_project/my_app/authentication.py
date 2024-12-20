from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from datetime import datetime
from my_app.models import MyUser
from rest_framework.serializers import ValidationError
from django.contrib.auth import get_user_model


class TimeRestrictedBackend(BaseBackend):

    def authenticate(self, request, email=None, password=None, **kwargs):
        
        try:
            user = MyUser.objects.get(email=email)

            if user.check_password(password):

                # Define allowed roles and time ranges
                allowed_roles = {
                    'admin': (0, 24),  # Admins can log in at any time
                    'manager': (9, 20), # Editors can log in between 9 AM and 6 PM
                    'employee': (12, 15) # Viewers can log in between 12 PM and 8 PM
                }

                # Get the current hour
                currentHour = datetime.now().hour

                # Get the user's role
                userRole = user.role  
                
                if userRole in allowed_roles:
                    start_hour, end_hour = allowed_roles[userRole]
                
                    # Check if the current time is within the allowed range
                    if start_hour <= currentHour < end_hour:
                        # 9 23 18
                        print("hy")
                        return user
                    
                    print("pass89", user)
                    raise ValidationError("User Time Out")
            
        except MyUser.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        User = get_user_model()  # Dynamically get the correct User model
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        

# ref - https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#writing-an-authentication-backend
