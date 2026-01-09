from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_booking_models"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="avatar",
            field=models.ImageField(blank=True, null=True, upload_to="avatars/"),
        ),
        migrations.AddField(
            model_name="service",
            name="masters",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={"profile__role": "admin"},
                related_name="services",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="booking",
            name="master",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"profile__role": "admin"},
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="master_bookings",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
