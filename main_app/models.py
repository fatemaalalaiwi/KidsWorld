from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import timedelta



type_of_card =(
    ('N' , 'Normal'),
    ('G' , 'Gold')
)


class cards(models.Model) :   
    card_type = models.CharField(max_length=1 , choices=type_of_card, default=type_of_card[0][0])    
    card_duration_time = models.FloatField(default=10)
    # credit = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.get_card_type_display()} ({self.card_duration_time} min)'

    def get_card_type_display(self):
        return dict(type_of_card).get(self.card_type)


#  Toy
class kids(models.Model):
    kid_name = models.CharField(max_length=100)             
    parent_name = models.CharField(max_length=100)      
    parent_phone = models.CharField(max_length=20)
    fk_card_id = models.ForeignKey( cards , on_delete=models.CASCADE)
    kid_image = models.ImageField(upload_to='main_app/static/uploads/', default="")
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    credit = models.FloatField(default=0.0)

    def __str__(self):
        return self.kid_name
    

    def get_absolute_url(self):
        return reverse('kid_detail', kwargs={'kid_id': self.id})


# cat
class games(models.Model):
    game_name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    game_image = models.ImageField(upload_to='main_app/static/uploads/', default="")
    game_price = models.FloatField(default=0.0)


    def __str__(self):
        return self.game_name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'game_id': self.id})
    

class employees(models.Model):
    employee_name = models.CharField(max_length=100)
    password = models.CharField(max_length=10)


class kids_games(models.Model):
    fk_kid_id = models.ForeignKey(kids, on_delete=models.CASCADE)
    fk_game_id = models.ForeignKey(games, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    user = models.ForeignKey(User , on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.end_time:
            self.end_time = self.start_time + timedelta(minutes=self.kid.card.card_duration_time)
        super().save(*args, **kwargs)    
