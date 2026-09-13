import uuid
from django.db import models

class Experience(models.Model): # experience adalah nama model yang kamu definisikan.\, 
                                #models.Model adalah kelas dasar yang digunakan untuk mendefinisikan model dalam django
    EXPERIENCE_CHOICES = [ #adalah tuple yang mendefinisikan pilihan kategori pengalaman yang tersedia.
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #adalah field bertipe UUIDField yang digunakan sebagai primary key dan nilainya di-generate otomatis menggunakan uuid.uuid4.
    title = models.CharField(max_length=255) #adalah field bertipe CharField untuk judul pengalaman, dengan panjang maksimal 255 karakter.
    description = models.TextField() #adalah field bertipe TextField untuk deskripsi pengalaman yang dapat menampung teks panjang.
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time') #adalah field bertipe CharField dengan pilihan terbatas sesuai EXPERIENCE_CHOICES, dengan nilai default 'full-time'.
    thumbnail = models.URLField(blank=True, null=True) #adalah field bertipe URLField untuk menyimpan URL gambar thumbnail pengalaman (opsional).
    started_at = models.DateTimeField(auto_now_add=True) # adalah field bertipe DateTimeField yang otomatis berisi tanggal dan waktu saat data dibuat.
    ended_at = models.DateTimeField(blank=True, null=True) #adalah field bertipe DateTimeField yang dapat dibiarkan kosong dan nilainya dapat diatur ke None.
    def __str__(self): #digunakan untuk mengembalikan representasi string dari objek (dalam hal ini judul pengalaman).
        return self.title 
    
    @property #digunakan untuk membuat atribut read-only yang nilainya merupakan hasil perhitungan dari atribut lain. Dalam kasus ini, is_ongoing akan bernilai True jika ended_at adalah None.
    def is_ongoing(self):
        return self.ended_at is None

class Education(models.Model): 

    EDUCATION_CHOICES = [
        ('SIC', 'Sekolah Indonesia Cairo'),
        ('LIS', 'La Royba Islamic School'),
        ('MBI', 'MAU Amanatul Ummah Program MBI'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #adalah field bertipe UUIDField yang digunakan sebagai primary key dan nilainya di-generate otomatis menggunakan uuid.uuid4.
    title = models.CharField(max_length=255) #adalah field bertipe CharField untuk judul pengalaman, dengan panjang maksimal 255 karakter.
    description = models.TextField() #adalah field bertipe TextField untuk deskripsi pengalaman yang dapat menampung teks panjang.
    category = models.CharField(max_length=20, choices=EDUCATION_CHOICES, default='full-time') #adalah field bertipe CharField dengan pilihan terbatas sesuai EXPERIENCE_CHOICES, dengan nilai default 'full-time'.
    thumbnail = models.URLField(blank=True, null=True) #adalah field bertipe URLField untuk menyimpan URL gambar thumbnail pengalaman (opsional).
    started_at = models.DateTimeField(auto_now_add=True) # adalah field bertipe DateTimeField yang otomatis berisi tanggal dan waktu saat data dibuat.
    ended_at = models.DateTimeField(blank=True, null=True) #adalah field bertipe DateTimeField yang dapat dibiarkan kosong dan nilainya dapat diatur ke None.

    def __str__(self): #digunakan untuk mengembalikan representasi string dari objek (dalam hal ini judul pengalaman).
        return self.title 
        
    @property #digunakan untuk membuat atribut read-only yang nilainya merupakan hasil perhitungan dari atribut lain. Dalam kasus ini, is_ongoing akan bernilai True jika ended_at adalah None.
    def is_ongoing(self):
        return self.ended_at is None
