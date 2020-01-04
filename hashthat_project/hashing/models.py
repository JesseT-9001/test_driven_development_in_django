from django.db import models


class Hash(models.Model):
    """
    Hash Model

    :var field text: Text field
    :var field hash: Char field
    """
    text = models.TextField()
    hash = models.CharField(max_length=64)

