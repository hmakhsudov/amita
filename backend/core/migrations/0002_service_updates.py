from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="servicecategory",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name="service",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.RenameField(
            model_name="service",
            old_name="base_price",
            new_name="price",
        ),
        migrations.AlterField(
            model_name="service",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
