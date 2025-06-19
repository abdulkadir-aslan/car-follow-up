from django.db import models
from account.models import User
from django.contrib.auth import get_user_model
from .middleware import get_current_user
from django.utils import timezone

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
    ("14","GENEL MÜDÜRLÜK"),
    ("15","ELEKTRİK MAKİNE VE MALZEME İKMAL"),
    ("16","KORUMA VE GÜVENLİK HİZMETLERİ"),
    ("17","MÜŞTERİ HİZMETLERİ VE KURUMSAL İLETİŞİM"),
)

FUEL_TYPE = (
    ("diesel","DİZEL"),
    ("gasoline","BENZİN"),
    ("gasoline_gas","TÜP-BENZİN"),
)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.message

class ChangeHistory(models.Model):
    model_name = models.CharField(max_length=255)
    object_id = models.PositiveIntegerField()
    field_name = models.CharField(max_length=255)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    change_type = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_name} ({self.object_id}) - {self.field_name} changed by {self.user} at {self.timestamp}"

    def get_verbose_name(self):
        # Bu yöntemi kullanarak field_name'in verbose_name'ini alabilirsiniz.
        model_class = globals()[self.model_name]  # Model ismini sınıf adı olarak çözümle
        field = model_class._meta.get_field(self.field_name)  # Modelin alanını al
        return field.verbose_name  # verbose_name değerini döndür
    
    def get_old_value_display(self):
        if hasattr(self, 'old_value') and self.old_value:
            model_class = globals()[self.model_name]
            field = model_class._meta.get_field(self.field_name)
            if field.choices:
                return dict(field.choices).get(self.old_value, self.old_value)
        return self.old_value

    def get_new_value_display(self):
        if hasattr(self, 'new_value') and self.new_value:
            model_class = globals()[self.model_name]
            field = model_class._meta.get_field(self.field_name)
            if field.choices:
                return dict(field.choices).get(self.new_value, self.new_value)
        return self.new_value
    
    class Meta:
        verbose_name = 'Change History'
        verbose_name_plural = 'Change Histories'

class Car(models.Model):
    plate = models.CharField(verbose_name="Plaka",max_length=15,unique=True,null=False,blank=False)
    brand = models.CharField(verbose_name="Marka",max_length=30,null=False,blank=False)
    model = models.CharField(verbose_name="Model",max_length=30,null=False,blank=False)
    vehicle_type = models.CharField(verbose_name="Araç Cinsi",choices=TYPE_CAR,max_length=15,blank=False)
    fuel_type = models.CharField(verbose_name="Yakıt Tipi",choices=FUEL_TYPE,default="diesel",max_length=15,blank=False)
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
    
    def save(self, *args, **kwargs):
        self.plate = self.plate.replace(" ", "").upper()
        user = get_current_user()  # Kullanıcı bilgisini almak

        if self.pk:  # Eğer nesne zaten veritabanında varsa
            old_instance = Car.objects.get(pk=self.pk)
            changed_fields = self._detect_changes(old_instance)

            # Değişiklikleri kaydet
            for field, (old_value, new_value) in changed_fields.items():
                if field == "kilometer":
                    continue
                ChangeHistory.objects.create(
                    model_name=self.__class__.__name__,
                    object_id=self.pk,
                    field_name=field,
                    old_value=old_value,
                    new_value=new_value,
                    change_type='update',
                    user=user,
                )

        super().save(*args, **kwargs)

    def _detect_changes(self, old_instance):
        """
        Mevcut nesne ile eski nesne arasındaki değişiklikleri tespit eder.
        """
        changes = {}
        for field in self._meta.fields:
            field_name = field.name
            old_value = getattr(old_instance, field_name, None)
            new_value = getattr(self, field_name, None)

            if old_value != new_value:
                changes[field_name] = (old_value, new_value)

        return changes
    
    def __str__(self):
        return self.plate
    
class Fuell(models.Model):
    user = models.ForeignKey(User,null=False,on_delete=models.PROTECT)
    car = models.ForeignKey(Car,null=False,on_delete=models.PROTECT)
    contry = models.CharField(verbose_name="iLÇE",null=False,max_length=11,blank=False)
    fuel_type = models.CharField(verbose_name="Yakıt Tipi",max_length=15,blank=True)
    kilometer = models.CharField(verbose_name="Kilometre",max_length=20,null=False,blank=False)
    average = models.FloatField(verbose_name="Ortalama Yakıt",null=False,blank=False)
    liter = models.IntegerField(verbose_name="Litre",blank=False,null=False)
    delivery = models.CharField(verbose_name="Teslim alan",max_length=30,null=False,blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at =models.DateTimeField(auto_now=True)
    comment = models.TextField(verbose_name="Açıklama",blank=True)
    
    def save(self, *args, **kwargs):
        user = get_current_user()  # Kullanıcı bilgisini almak
        if self.pk:  # Eğer nesne zaten veritabanında varsa
            old_instance = Fuell.objects.get(pk=self.pk)
            changed_fields = self._detect_changes(old_instance)
            # Değişiklikleri kaydet
            for field, (old_value, new_value) in changed_fields.items():
                ChangeHistory.objects.create(
                    model_name=self.__class__.__name__,
                    object_id=self.pk,
                    field_name=field,
                    old_value=old_value,
                    new_value=new_value,
                    change_type='update',
                    user=user,
                )

        super().save(*args, **kwargs)

    def _detect_changes(self, old_instance):
        """
        Mevcut nesne ile eski nesne arasındaki değişiklikleri tespit eder.
        """
        changes = {}
        for field in self._meta.fields:
            field_name = field.name
            old_value = getattr(old_instance, field_name, None)
            new_value = getattr(self, field_name, None)

            if old_value != new_value:
                changes[field_name] = (old_value, new_value)

        return changes
    def __str__(self):
        return self.contry
    
class ZimmetFisi(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='zimmet_fisleri')
    file = models.FileField(upload_to='zimmet_fisleri/%Y/%m/%d/', verbose_name="Zimmet Fişi", null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    uploaded_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
        
    def __str__(self):
        return f"{self.car.plate} - Zimmet Fişi - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
