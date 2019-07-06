# Generated by Django 2.2.2 on 2019-07-06 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projetos', '0001_initial'),
        ('perfis', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='gestor',
            name='projetos',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projetos', to='projetos.Projeto'),
        ),
        migrations.AddField(
            model_name='gestor',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='gestor', to=settings.AUTH_USER_MODEL),
        ),
    ]
