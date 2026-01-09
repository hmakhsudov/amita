from django.db import migrations


def seed_categories(apps, schema_editor):
    ServiceCategory = apps.get_model("core", "ServiceCategory")
    names = ["Уход за лицом", "Массаж", "Маникюр", "Брови"]
    for name in names:
        ServiceCategory.objects.get_or_create(name=name)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_service_updates"),
    ]

    operations = [
        migrations.RunPython(seed_categories, migrations.RunPython.noop),
    ]
