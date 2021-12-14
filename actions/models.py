from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Action(models.Model):
    user = models.ForeignKey(get_user_model(),
                            related_name='actions',
                            on_delete=models.CASCADE,
                            db_index=True)
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType,
                                    blank=True,
                                    null=True,
                                    related_name='target_obj',
                                    on_delete=models.CASCADE)
    target_id = models.PositiveBigIntegerField(null=True,
                                                blank=True,
                                                db_index=True)
    target = GenericForeignKey('target_ct','target_id')
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created']