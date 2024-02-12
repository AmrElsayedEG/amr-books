from django.db import models

class UserRoleChoices(models.IntegerChoices):
    ADMIN = 0, "Admin"
    VISITOR = 1, "Visitor"