from django.db import models

class StoreUser(models.Model) :
    name         = models.CharField(max_length = 20)
    email        = models.EmailField(max_length = 50, unique = True)
    password     = models.CharField(max_length = 200)
    phone_number = models.CharField(max_length = 50)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)
    
    class Meta :
        db_table = 'stores_users'