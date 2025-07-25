# Generated by Django 5.2.2 on 2025-06-05 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cineBox', '0010_alter_horario_fecha_alter_horario_hora'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='horario',
            options={'permissions': [('ver_horario', 'Puede ver los horarios'), ('crear_horario', 'Puede crear horarios'), ('editar_horario', 'Puede editar horarios'), ('eliminar_horario', 'Puede eliminar horarios')]},
        ),
        migrations.AlterModelOptions(
            name='sala',
            options={'permissions': [('ver_sala', 'Puede ver las salas'), ('crear_sala', 'Puede crear salas'), ('editar_sala', 'Puede editar salas'), ('eliminar_sala', 'Puede eliminar salas')]},
        ),
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.CharField(choices=[('cliente', 'Cliente'), ('admin', 'Administrador'), ('gerente', 'Gerente')], default='cliente', max_length=10),
        ),
    ]
