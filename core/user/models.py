from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from core.abstract.models import AbstractModel, AbstractManager
from thor_devkit import cry


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.public_id, filename)


class HDWallet(models.Model):
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        related_name='hd_wallet')
    mnemonic = models.TextField()
    public_key = models.CharField(max_length=128)
    private_key = models.CharField(max_length=128)
    address = models.CharField(max_length=42)

    def __str__(self):
        return f"HD Wallet for {self.user.email}"


class UserManager(BaseUserManager, AbstractManager):
    def create_user(self, username, email, password=None, **kwargs):
        if username is None:
            raise TypeError("Users must have a username.")
        if email is None:
            raise TypeError("Users must have an email.")
        if password is None:
            raise TypeError("User must have a password.")

        user = self.model(
            username=username, email=self.normalize_email(email), **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        # Generate mnemonic
        mnemonic = cry.mnemonic.generate()

        # Create HD wallet for the user
        hd_node = cry.HDNode.from_mnemonic(
            mnemonic,
            init_path=cry.hdnode.VET_EXTERNAL_PATH)
        hd_wallet = HDWallet.objects.create(
            user=user,
            mnemonic=mnemonic,
            public_key=hd_node.public_key().hex(),
            private_key=hd_node.private_key().hex(),
            address=hd_node.address().hex()
        )

        return user

    def create_superuser(self, username, email, password, **kwargs):
        if password is None:
            raise TypeError("Superusers must have a password.")
        if email is None:
            raise TypeError("Superusers must have an email.")
        if username is None:
            raise TypeError("Superusers must have an username.")

        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    bio = models.TextField(null=True)
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to=user_directory_path
    )
    total_activities = models.PositiveBigIntegerField(
        default=0,
    )
    wallet_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    def increment_total_activities(self):
        self.total_activities += 1
        self.save(update_fields=['total_activities'])
