# Generated by Django 4.2.2 on 2023-06-16 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='bid',
            name='item',
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='listing',
            name='image_url',
            field=models.URLField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='auctions.category'),
            preserve_default=False,
        ),
    ]