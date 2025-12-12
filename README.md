EBLG341 – İşletim Sistemleri  
Ödev 1 – CPU Zamanlama Algoritmaları

Bu proje, verilen iki farklı süreç veri seti (case1 ve case2) üzerinde altı CPU zamanlama algoritmasını çalıştırmak için hazırlanmıştır.  
Amaç, her algoritmanın zaman çizelgesini ve performans ölçümlerini üretmek ve sonuçları dosya olarak kaydetmektir.


- Kullanılan Algoritmalar

Projede aşağıdaki işleyiciler ayrı ayrı uygulanmıştır:

1. FCFS (First Come First Served)
2. Preemptive SJF
3. Non-Preemptive SJF
4. Round Robin (quantum = 4)
5. Preemptive Priority
6. Non-Preemptive Priority


- Proje Yapısı

EBLG341-Scheduler-Project/
│
├── src/
│ ├── main.py
│ ├── schedulers.py
│
├── data/
│ ├── data1.csv
│ ├── data2.csv
│
├── output/
│ ├── fcfs_case1.txt
│ ├── fcfs_case2.txt
│ ├── ...
│
└── README.txt

- Çalıştırma

Proje Python ile yazılmıştır. Herhangi bir ek paket gerektirmez.

Terminalden proje klasörüne girdikten sonra: terminale 'python src/main.py' yazmak yeterlidir

Çalıştırıldığında, her algoritmanın sonuçları **output/** klasörüne otomatik olarak kaydedilir.


- Üretilen Sonuçlar

Her algoritma için aşağıdaki bilgiler ayrı bir dosyaya yazdırılır:

- Zaman tablosu (başlangıç – süreç – bitiş)
- Maksimum ve ortalama bekleme süresi
- Maksimum ve ortalama turnaround süresi
- T = 50, 100, 150, 200 için throughput
- Ortalama CPU verimliliği  
- Toplam context switch sayısı

Dosya isimleri şu şekildedir:

-fcfs_case1.txt
-sjf_preemptive_case2.txt
-rr_case1.txt
-priority_nonpreemptive_case2.txt

Proje, verilen iki dataset üzerinde çalışmaktadır:

- case1 → data1.csv
- case2 → data2.csv

Dosyalardaki bilgiler:

- Process_ID  
- Arrival_Time  
- CPU_Burst_Time  
- Priority

Öncelikler metinsel olarak verilmiştir: `high`, `normal`, `low`.  
Program içerisinde bu değerler sayısal öncelik seviyelerine dönüştürülür.

- Notlar:

- Quantum değeri Round Robin için **4** olarak belirlenmiştir.
- Bağlam değiştirme süresi hesaplamasında **0.001 zaman birimi** kullanılmıştır.
- Tüm algoritmalar birbirinden bağımsız olarak çalıştırılır.
- Kodun tamamı `src/` klasöründe yer almaktadır.


- Geliştiren
Kaan Barış Bozkurt - id: 20232013066
Nişantaşı Üniversitesi – Bilgisayar Mühendisliği  
EBLG341 – İşletim Sistemleri