from django.contrib.auth.models import AbstractUser, UserManager, Group, Permission
from django.db import models


class CustomUserManager(UserManager):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]

    def males(self):
        return self.filter(gender=self.GENDER_MALE)

    def females(self):
        return self.filter(gender=self.GENDER_FEMALE)


class Userkill(AbstractUser):
    avatar = models.ImageField(upload_to="avatars", verbose_name='Аватар')
    description = models.TextField(max_length=2000, verbose_name="Информация", blank=True, null=True)
    phone = models.CharField(max_length=30, verbose_name="Номер телефона", blank=True, null=True)
    gender = models.IntegerField(choices=CustomUserManager.GENDER_CHOICES)
    followers = models.ManyToManyField('self', related_name='following', verbose_name="Подписки", symmetrical=False)

    objects = CustomUserManager()
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        related_name='userkill_groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='userkill_user_permissions'
    )

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'
