# Generated by Django 4.1.13 on 2024-11-19 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Librioteca', '0003_remove_prestamo_nombre_usuario_prestamo_devuelto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='user',
        ),
        migrations.AddField(
            model_name='usuario',
            name='apellido',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='correo',
            field=models.EmailField(default=1, max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='rut',
            field=models.CharField(default=1, max_length=12, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
    ]
