from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_plan_models"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start_at", models.DateTimeField(db_index=True)),
                ("end_at", models.DateTimeField(db_index=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("scheduled", "Запланирована"),
                            ("cancelled", "Отменена"),
                            ("completed", "Завершена"),
                        ],
                        default="scheduled",
                        max_length=20,
                    ),
                ),
                ("client_name", models.CharField(max_length=150)),
                ("client_phone", models.CharField(blank=True, max_length=50)),
                ("client_email", models.EmailField(max_length=254)),
                ("comment", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "service",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="core.service"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-start_at"]},
        ),
    ]
