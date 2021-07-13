# Generated by Django 3.2.4 on 2021-07-02 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0002_auto_20210622_0531'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='number',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Transcription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contente', models.TextField(blank=True, null=True)),
                ('checked', models.BooleanField(default=False)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_transcription', to='document.images')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
    ]