from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0013_block_requested'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='bill_hash',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]
