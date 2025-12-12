# Kullanıcı Kılavuzu  
## EBLG341 – CPU Zamanlama Projesi

Bu kılavuz, projenin nasıl çalıştırılacağını ve sonuçların nasıl değerlendirileceğini açıklamaktadır.

---

## 1. Sistem Gereksinimleri

- Python 3.10 veya üzeri
- Bonus web paneli için:

'pip install streamlit' terminale bu komutu yazmanız yeterli.


## 2. Projenin Çalıştırılması

Terminalden proje ana klasörüne gidin:
'python src/main.py' terminale bu komutu yazmanız yeterli.


Bu komut tüm algoritmaların hem case1 hem de case2 üzerinde çalıştırılmasını sağlar.  
Üretilen sonuçlar `output/` klasöründe `.txt` dosyaları olarak kaydedilir.


## 3. Çıktı Dosyaları

Her sonuç dosyasında şu bilgiler yer alır:

- Zaman çizelgesi  
- Maksimum & ortalama bekleme süresi  
- Maksimum & ortalama turnaround süresi  
- T = 50, 100, 150, 200 için throughput  
- CPU verimliliği  
- Toplam context switch sayısı  

Bu bilgiler ilgili algoritmanın performansını değerlendirmek için kullanılır.


## 4. Bonus: Etkileşimli Web Paneli

Raporları görsel şekilde incelemek için dashboard kullanılabilir:

'streamlit run src/dashboard.py' terminale yazmanız yeterli.


Panel üzerinden:

- Veri seti seçimi  
- Algoritma seçimi  
- Round Robin quantum ayarı  
- Zaman çizelgesi görüntüleme  
- Bekleme ve turnaround süreleri  
- Throughput ve CPU verimliliği  

gibi analizler yapılabilir.


## 5. Veri Dosyaları

`data/` klasöründeki veri dosyaları şu formatı takip eder:

Process_ID,Arrival_Time,CPU_Burst_Time,Priority
P001,0,4,high


Yeni veri dosyaları da bu yapıya uygun olduğu sürece proje sorunsuz çalışır.


## 6. Klasör Yapısı

src/ → kodlar
data/ → csv veri setleri
output/ → sonuç dosyaları
README.md → genel bilgi
USER_MANUAL.md → bu kılavuz
REPORT.md → proje raporu


Bu proje, CPU zamanlama algoritmalarının karşılaştırmalı olarak incelenmesi amacıyla geliştirilmiştir.