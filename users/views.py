import json
import re

from unittest     import result
from django.http  import JsonResponse
from django.views import View
from users.models import StoreUser

class SignUpView(View):
       def post(self, request):
        data = json.loads(request.body) 
        email_form = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        password_form = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')

        try :
            if data['password'] and data['email'] == None :
                return JsonResponse({"message": "Email or Password is Empyt"}, status = 400)   

            if StoreUser.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "Already registered Email"}, status = 400)   

            if not email_form.match(data['email']) :
                return JsonResponse({"message": "Invalid email format"}, status = 400)   

            if not password_form.match(data['password']):
                return JsonResponse({"message": "Invalid password format"}, status = 400)
            
            StoreUser.objects.create(
                name         = data['name'],
                email        = data['email'],
                password     = data['password'],
                phone_number = data['phone_number'],
            )
            return JsonResponse({"message": "SUCCESS"}, status = 201)
            
        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)  

