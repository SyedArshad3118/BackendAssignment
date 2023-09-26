from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class UserProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='profile')
    followers = models.ManyToManyField('User', related_name='following', blank=True)

    def __str__(self):
        return self.user.username

class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    class Meta:
        db_table = 'custom_user'

    def __str__(self):
        return self.username

    @property
    def profile(self):
        try:
            return self.profile
        except UserProfile.DoesNotExist:
            return None

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title
