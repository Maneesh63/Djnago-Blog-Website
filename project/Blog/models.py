from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin,Group,Permission
from django.utils import timezone

class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **add_more):

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **add_more)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


 

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100,unique=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

     
   
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



class likes(models.Model):
    
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    post=models.ForeignKey('Post', on_delete=models.CASCADE)

    date=models.DateField(auto_now_add=True)
    
    


class Post(models.Model):
    
    post_id=models.AutoField(primary_key=True)

    title=models.CharField(max_length=200)

    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
 
    description=models.TextField()

    image=models.ImageField(null=True,blank=True,upload_to='images/')

    date = models.DateTimeField(default=timezone.now) 

    post_likes = models.ManyToManyField(CustomUser, through=likes, related_name='post_likes')  
    

class dashboard(models.Model):

    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)

    profile_pic=models.ImageField(null=True,blank=True,upload_to='images/profile/')

    bio=models.TextField()

    def __str__(self):
        return self.title
    
    def user_id(self):
        return self.user.user_id
    

 
 

