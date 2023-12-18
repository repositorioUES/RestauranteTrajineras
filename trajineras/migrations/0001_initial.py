# Generated by Django 3.2.4 on 2023-12-17 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(help_text='Nombre del producto', max_length=50)),
                ('tipo', models.CharField(blank=True, choices=[('c', 'Comida'), ('b', 'Bebida')], help_text='Tipo de producto', max_length=10)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=5)),
                ('activo', models.BooleanField(blank=True, default=1)),
            ],
        ),
        migrations.CreateModel(
            name='OrdenTemp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('mesa', models.IntegerField(blank=True, null=True)),
                ('fechaHora', models.DateTimeField(auto_now_add=True)),
                ('cocina', models.BooleanField(blank=True, default=0)),
                ('bebida', models.BooleanField(blank=True, default=0)),
                ('cobrable', models.BooleanField(blank=True, default=0)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cliente', models.CharField(help_text='Nombre del cliente', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='OrdenMenu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(blank=True, null=True)),
                ('idMenu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='trajineras.menu')),
                ('idOrden', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='trajineras.ordentemp')),
            ],
        ),
    ]