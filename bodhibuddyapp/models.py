from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    ONLINE_IDLE = 'OI'
    ONLINE_CHANTING= 'OC'
    OFFLINE= 'OF'
    STATUS= (
        (ONLINE_IDLE, 'OnlineIdle'),
        (ONLINE_CHANTING, 'OnlineChanting'),
        (OFFLINE, 'Offline'),
    )
    current_state = models.CharField(
        max_length=2,
        choices=STATUS,
        default=OFFLINE,
    )



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class SharedDaimokuTarget(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    creator = models.ForeignKey(Profile, related_name='target_user')
    target_count = models.IntegerField()
    target_date_millis = models.IntegerField()
    create_date_millis = models.IntegerField()







