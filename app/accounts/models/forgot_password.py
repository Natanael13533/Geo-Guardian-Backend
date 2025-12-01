from django.db import models

# Create your models here.
class ForgotPassword(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'forgot_password'
        
    def __str__(self):
        return self.email