from django.db import models

# Create your models here.

class Kid(models.Model):
    name = models.CharField(max_length=100)             
    parent_name = models.CharField(max_length=100)      
    parent_phone = models.IntegerField(max_length=20)     
    card_id = models.IntegerField() 


    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        return reverse('kid_detail', kwargs={'kid_id': self.id})