import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from core.abstract.models import AbstractModel, AbstractManager
from core.user.models import HDWallet
from thor_devkit import cry


def post_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/post_<id>/<filename>
    return "post_{0}/{1}".format(instance.id, filename)


class PostManager(AbstractManager):
    def get_last_author_posts(self, author_id):
        return self.filter(author_id=author_id).order_by('-created')[:5]


class Post(AbstractModel):

    ECO_TYPE_CHOICES = [
        ('paper', 'Paper'),
        ('bottle', 'Bottle'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    images = models.ImageField(
        upload_to=post_directory_path,
        null=True,
        blank=True)
    eco_type = models.CharField(max_length=6, choices=ECO_TYPE_CHOICES)
    weight = models.DecimalField(max_digits=10, decimal_places=3)
    approved = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    last_updates = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    author = models.ForeignKey(
        to='core_user.User',
        on_delete=models.CASCADE,
        related_name='posts'
    )

    objects = PostManager()

    def __str__(self):
        return self.name

    def generate_token(self):
        # author_hd_wallet = self.author.hd_wallet
        # if author_hd_wallet and isinstance(author_hd_wallet.private_key, str):
        #     token = cry.blake2b256(author_hd_wallet.private_key.encode()).hex()
        #     return token
        # else:
        #     return None
        pass

    def generate_qr_code(self):
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.name)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            img.save(buffer, format='PNG')
            filename = f'qr_code_{self.id}.png'

            self.qr_code.save(filename, File(buffer), save=False)
            buffer.close()
        except Exception as e:
            print(f"Error generating QR code: {e}")

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.generate_qr_code()

        author = self.author

        hd_wallet, created = HDWallet.objects.get_or_create(user=author)

        if created or hd_wallet.token != self.generate_token():
            hd_wallet.token = self.generate_token()
            hd_wallet.save()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "core_post"
