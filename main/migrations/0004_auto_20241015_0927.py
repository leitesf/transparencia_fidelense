# Generated by Django 3.2 on 2024-10-15 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20240828_0921'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pagamento',
            options={'ordering': ['-folha__ordenacao', 'contrato__pessoa__nome'], 'verbose_name': 'Pagamento', 'verbose_name_plural': 'Pagamentos'},
        ),
        migrations.AddField(
            model_name='contrato',
            name='data_desligamento',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Desligamento'),
        ),
    ]
