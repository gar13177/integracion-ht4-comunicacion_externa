from django.db import models
from orchestrator.apiendpoints.constants import Constants

class LoginUser(models.Model):
    """
    Clase con parametros para hacer login
    """
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        # evitar persistencia
        managed = False

    # override: modelo sin persistencia
    def save(self, *args, **kwargs):
        pass 

class AppUser(models.Model):
    """
    Token: usuario logeado correctamente y presente en nuestro sistema
    """
    created = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()
    user_token = models.CharField(max_length=100, primary_key=True)
    user_rights = models.CharField(max_length=100, default=Constants.USER_RIGHTS_CLIENT)

    #owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)

class OrderRequested(models.Model):
    """
    Clase con parametros para hacer una orden
    """
    user_token = models.CharField(max_length=100)
    request_type = models.CharField(choices=((1,'check'), (2,'pay')),max_length=5)
    order = models.TextField()

    class Meta:
        # evitar persistencia
        managed = False

    # override: modelo sin persistencia
    def save(self, *args, **kwargs):
        pass

class OrderStored(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_token = models.ForeignKey(AppUser,db_column='user_token', related_name ='orders', on_delete=models.CASCADE)
    order_token = models.CharField(max_length=100, primary_key=True)
    status = models.CharField(max_length=100, default=Constants.ORDER_INVOICED)

    class Meta:
        ordering = ('created',)


class OrderUpdateRequest(models.Model):
    order_token = models.CharField(max_length=100)
    order_status = models.CharField(max_length=100)

    class Meta:
        # evitar persistencia
        managed = False

#aqui hago mi promocionModel
class Promotion(models.Model):
    """
    promotion_description: es la descripcion de la promocion que se le presenta al usuario
    expiration_date: es la fecha de expiracion de la promocion
    """
    promotion_description = models.CharField(max_length=100)
    expiration_date = models.DateTimeField()