# Generated by Django 4.0.5 on 2022-06-20 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='contry',
            field=models.CharField(choices=[('akçakale', 'AKÇAKALE'), ('birecik', 'BİRECİK'), ('bozova', 'BOZOVA'), ('ceylanpınar', 'CEYLANPINAR'), ('halfeti', 'HALFETİ'), ('harran', 'HARRAN'), ('hilvan', 'HİLVAN'), ('siverek', 'SİVEREK'), ('suruç', 'SURUÇ'), ('viranşehir', 'VİRANŞEHİR'), ('merkez', 'MERKEZ')], max_length=11, verbose_name='iLÇE'),
        ),
    ]