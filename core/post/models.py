import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from core.abstract.models import AbstractModel, AbstractManager


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

    def generate_qr_code(self):
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

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "core_post"
