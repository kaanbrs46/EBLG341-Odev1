# Proje Raporu  
## EBLG341 – İşletim Sistemleri  
### CPU Zamanlama Algoritmaları Karşılaştırması

Bu rapor, verilen iki süreç veri seti (case1 ve case2) üzerinde altı farklı zamanlama algoritmasının performanslarını değerlendirmek amacıyla hazırlanmıştır.


# 1. Kullanılan Algoritmalar

1. FCFS  
2. SJF – Preemptive  
3. SJF – Non-Preemptive  
4. Round Robin (q = 4)  
5. Priority – Preemptive  
6. Priority – Non-Preemptive  

Her algoritma her iki veri seti üzerinde ayrı ayrı çalıştırılmıştır.


# 2. Case1 Analizi

Her algoritmanın zaman çizelgesi ve performans sonuçları `output/` klasöründe ilgili dosyalarda verilmiştir.

Genel gözlemler:

- **FCFS** sıralı çalıştığı için yüksek bekleme süreleri oluşmuştur.  
- **SJF Preemptive**, burst time kısa olan süreçleri önce işlediğinden bekleme sürelerini önemli ölçüde düşürmüştür.  
- **SJF Non-Preemptive**, CPU'yu alan süreci bitirene kadar bırakmadığı için bazı uzun işler sistemde gecikmeye neden olmuştur.  
- **Round Robin**, q=4 ile süreçler arasında daha adil bir paylaşım sağlamıştır.  
- **Priority Preemptive**, high öncelikli süreçleri sürekli öne alarak diğerlerini geciktirmiştir.  
- **Priority Non-Preemptive**, önceliği dikkate alır ancak preemption yapmadığı için bazı beklemeler daha uzundur.


# 3. Case2 Analizi

Case2’de burst time değerleri düzenli arttığı için:

- **SJF Preemptive** daha sık context switch oluşturmuştur.  
- **Priority algoritmaları**, öncelik dağılımı daha belirgin olduğu için farklı performans göstermiştir.  
- **Round Robin**, yoğunluk nedeniyle daha fazla kesme üretmiştir.  
- **FCFS**, yine en öngörülebilir fakat en yüksek toplam bekleme süresine sahip yöntemdir.


# 4. Karşılaştırmalı Performans Değerlendirmesi

### Bekleme Süreleri
- En düşük: **SJF Preemptive**  
- En yüksek: **FCFS** ve **Non-Preemptive Priority**

### Turnaround
- En düşük turnaround genelde **SJF Preemptive**  
- En yüksek turnaround **FCFS**'te gözlemlenmiştir.

### Throughput
- En yüksek throughput: **Round Robin (q=4)**  
- Öncelikli algoritmalar bazı zaman aralıklarında daha düşük throughput üretmiştir.

### CPU Verimliliği
- En yüksek verimlilik: **SJF Preemptive**  
- Düşük verimlilik: **FCFS** (IDLE aralıkları fazla)

### Context Switch
- En fazla kesme: **SJF Preemptive** ve **Round Robin**  
- En az kesme: **FCFS** ve **Non-Preemptive Priority**


# 5. Sonuç

Çalışmalar, teorik CPU zamanlama prensipleriyle uyumlu sonuçlar üretmiştir:

- **Adalet önemliyse → Round Robin**
- **Bekleme süresi en düşük olsun → SJF Preemptive**
- **Basitlik isteniyorsa → FCFS**
- **Öncelik kritikse → Priority Preemptive**

Bu proje, farklı algoritmaların gerçek veri setleri üzerinde nasıl performans gösterdiğini karşılaştırmalı şekilde ortaya koymuştur.


Bu rapor, EBLG341 İşletim Sistemleri dersi için hazırlanmıştır.
