from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.conf import settings

class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    bio  = models.CharField(max_length=300)
    image = models.ImageField(upload_to='users/', blank=True, null=True, default="default.jpg")
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.fullname
    
def create_user_profile(sender, instance, created, **kwargs):
     if created:
         Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
    
class Conference(models.Model):
    _CATE= [
        ('Education', 'EDUCATION'),
        ('Technologies', 'TECHNOLOGIES'),
        ('Science', 'SCIENCE'),
        ('Culture', 'CULTURE'),
        ('Arts', 'ARTS'),
        ('Business', 'BUSINESS'),
        ('Autres', 'AUTRES')
    ]     
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    price = models.CharField(default="Gratuit", max_length=255)
    category = models.CharField(max_length=255, choices=_CATE)
    lieu = models.CharField(max_length=255)
    image = models.ImageField(upload_to='conferences/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Session(models.Model):
    conference = models.ForeignKey(Conference, related_name='sessions', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    speaker = models.CharField(max_length=100)
    profession = models.CharField(max_length=255)
    start_time = models.DateTimeField()

    def __str__(self):
        return self.title

class Registration(models.Model):
    user = models.ForeignKey(User, related_name='registrations', on_delete=models.CASCADE)
    session = models.ForeignKey(Session, related_name='registrations', on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} registered for {self.session.title}"


