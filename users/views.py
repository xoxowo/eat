import json
import re


from unittest     import result
from django.http  import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

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
"""
로그인을 위한 View를 작성해야합니다. ****로그인 정보(이메일, 비밀번호)

로그인을 할 때는 사용자 계정과 비밀번호가 필수입니다. 

계정이나 패스워드 키가 전달되지 않았을 경우, {"message": "KEY_ERROR"}, status code 400 을 반환합니다. 했음..ㅠㅠ
ff
계정을 잘 못 입력한 경우 {"message": "INVALID_USER"}, status code 401을 반환합니다. vvv드디어 했다...

비밀번호를 잘 못 입력한 경우 {"message": "INVALID_USER"}, status code 401을 반환합니다. 이건 했어..ㅠㅠ

로그인이 성공하면 {"message": "SUCCESS"}, status code 200을 반환합니다. 건 했어..ㅠㅠ
"""
class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try: 
            # StoreUser에 email 키 값에 클라이언트가 준 email 정보가 일치하지 않으면 오류 
            if not StoreUser.objects.filter(email=data['email']).exists() :
                return JsonResponse({"message": "NOT MATCH"}, status = 401)   
            # StoreUser에 email 키 값에 클라이언트가 준 email 정보가 일치하면 내부 if 문 으로 들어감
            if StoreUser.objects.filter(email=data['email']):
                # email은 일치하고 클라이언트가 준 password값도 일치하니까 리턴 
                if StoreUser.objects.filter(password = data['password']):
                    return JsonResponse({"message": "SUCCESS"}, status = 200)
                # email 값은 일치하나 password 값은 일치하지 않아 에러 리턴 ..
                else:
                    return JsonResponse({"message": "INVALID_USER_password error"}, status = 401) 

        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)