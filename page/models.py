from django.db import models
from account.models import User
from django.utils.text import slugify


STATUS= (
    ('active','Aktif'),
    ('passive','Pasif'),
)

DEFAULT_STATUS = 'active'

TYPE_CAR = (
    ("mount","BİNEK"),
    ("pick_up","PİCK UP"),
    ("truck","KAMYON"),
    ("water_tanker","SU TANKERİ"),
    ("motorcycle","MOTOSİKLET"),
    ("loader_exvator","YÜKLEYİCİ EKSKAVATÖR"),
    ("screwer","VİDANJÖR"),
    ("driling_machine","SONDAJ MAKİNASI"),
    ("forklift","FORKLIFT"),
    ("generator","JENERATÖR"),
    ("bucget","KEPÇE JCB"),
    ("tractor","TRAKTÖR"),
    ("transit","TRANSİT"),
)

OWNERSHİP = (
    ("contractor","MÜTAHİT"),
    ("corporation","KURUM"),
    ("forrent","KİRALIK")
)

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

HEAD_OF_DEPARTMENT = (
    ("1","İNSAN KAYNAKLARI"),
    ("2","MALİ HİZMETLER"),
    ("3","ARITMA TESİSLERİ"),
    ("4","BİLGİ İŞLEM"),
    ("5","DESTEK HİZMETLERİ"),
    ("6","İÇME SUYU VE KANALİZASYON"),
    ("7","PLAN VE PROJE"),
    ("8","STRATEJİ GELİŞTİRME"),
    ("9","SU VE ATIK SU TEKNOLOJİLERİ"),
    ("10","YATIRIM İNŞAAT"),
    ("11","ABONE İŞLERİ"),
    ("12","TEFTİŞ KURULU"),
    ("13","HUKUK MÜŞAVİRLİĞİ"),
    ("14","GENEL MÜDÜRLÜK")
)
    
class Car(models.Model):
    plate = models.CharField(verbose_name="Plaka",max_length=15,unique=True,null=False,blank=False)
    brand = models.CharField(verbose_name="Marka",max_length=30,null=False,blank=False)
    model = models.CharField(verbose_name="Model",max_length=30,null=False,blank=False)
    vehicle_type = models.CharField(verbose_name="Araç Cinsi",choices=TYPE_CAR,max_length=15,blank=False)
    debit = models.CharField(verbose_name="Zimmet",max_length=30,null=False,blank=True)
    title = models.CharField(verbose_name="Ünvan",max_length=50,null=False,blank=True) 
    kilometer = models.CharField(verbose_name="Kilometre",max_length=20,null=False,blank=False)
    possession = models.CharField(verbose_name="Sahiplik",choices=OWNERSHİP,max_length=11,null=False,blank=False)
    comment = models.TextField(verbose_name="Açıklama",blank=True)
    department =  models.CharField(verbose_name="Daire Başkanlığı",null=False,choices=HEAD_OF_DEPARTMENT,max_length=2,blank=False)
    contry = models.CharField(verbose_name="iLÇE",null=False,choices=CONTRY,max_length=11,blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at =models.DateTimeField(auto_now=True)
    status = models.CharField(verbose_name="Durum",choices=STATUS,default=DEFAULT_STATUS,max_length=7,blank=False)
    
    def __str__(self):
        return self.plate
    
    def save(self, *args, **kwargs):
        self.plate = self.plate.replace(" ", "").upper()
        return super(Car, self).save(*args, **kwargs)
    
   
   
class Fuell(models.Model):
    user = models.ForeignKey(User,null=False,on_delete=models.PROTECT)
    car = models.ForeignKey(Car,null=False,on_delete=models.PROTECT)
    contry = models.CharField(verbose_name="iLÇE",null=False,max_length=11,blank=False)
    kilometer = models.CharField(verbose_name="Kilometre",max_length=20,null=False,blank=False)
    average = models.FloatField(verbose_name="ortalamaYakıt",null=False,blank=False)
    liter = models.IntegerField(verbose_name="Litre",blank=False,null=False)
    delivery = models.CharField(verbose_name="Teslim alan",max_length=30,null=False,blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at =models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.contry