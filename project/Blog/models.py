from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin,Group,Permission
from django.utils import timezone


#Model to Manaage Authentication details and perform some common validations
class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **add_more):

        email = self.normalize_email(email)

        user = self.model(email=email, username=username, **add_more)

        user.set_password(password)

        user.save(using=self._db)

        return user

#Determines whether Admin or not
    def create_superuser(self, email, username, password=None, **extra):
        
        extra.setdefault('is_staff', True)

        extra.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra)
                                


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
                                                  #upload images to Image folder inside our project 
    image=models.ImageField(null=True,blank=True,upload_to='images/')

    date = models.DateTimeField(default=timezone.now) 

    post_likes = models.ManyToManyField(CustomUser, through=likes, related_name='post_likes')  
  


class UserProfile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
   
    bio = models.TextField(blank=True, null=True)

    image=models.ImageField(null=True,blank=True,upload_to='images/')

class Comment(models.Model):

    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)  
    
    user=models.ForeignKey(CustomUser,  on_delete=models.CASCADE,null=True)

    profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)
    
    comment=models.CharField(max_length=255)

    date=models.DateField(default=timezone.now)   
 

 
 

