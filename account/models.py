from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

STATUS= (
    ('active','Aktif'),
    ('passive','Pasif'),
)

DEFAULT_STATUS = 'passive'

CONTRY = (
    ('akçakale','AKÇAKALE'),
    ('birecik','BİRECİK'),
    ('bozova','BOZOVA'),
    ('ceylanpınar','CEYLANPINAR'),
    ('halfeti','HALFETİ'),
    ('harran','HARRAN'),
    ('hilvan','HİLVAN'),
    ('siverek','SİVEREK'),
    ('suruç','SURUÇ'),
    ('viranşehir','VİRANŞEHİR'),
    ('merkez','MERKEZ'),
)


class User(AbstractUser):
    status = models.CharField(verbose_name="Durum",choices=STATUS,default=DEFAULT_STATUS,max_length=7,blank=False)
    contry = models.CharField(verbose_name="iLÇE",null=False,choices=CONTRY,max_length=11,blank=False)


