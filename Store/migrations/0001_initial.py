# Generated by Django 3.1.6 on 2021-07-29 22:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('General', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreItem',
            fields=[
                ('Id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('Image', models.ImageField(upload_to='')),
                ('Headline', models.CharField(max_length=50)),
                ('Description', models.TextField()),
                ('Price', models.FloatField()),
                ('Published', models.BooleanField(default=False)),
                ('Created_on', models.DateTimeField(default=datetime.datetime.now)),
                ('Updated_on', models.DateTimeField(default=datetime.datetime.now)),
                ('Like_count', models.IntegerField(default=0)),
                ('Owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='General.profile')),
                ('User', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
