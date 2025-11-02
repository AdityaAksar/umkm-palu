# Dashboard Business Intelligence - Ekspor UMKM Sulawesi Tengah

Dashboard interaktif untuk analisis ekspor UMKM Sulawesi Tengah dalam mendukung Cross Border Trade.

## 📋 Deskripsi Proyek

Dashboard ini dikembangkan sebagai bagian dari tugas akhir dengan judul:
**"PERANCANGAN DASHBOARD BUSINESS INTELLIGENCE UNTUK ANALISIS EKSPOR UMKM SULAWESI TENGAH DALAM MENDUKUNG CROSS BORDER TRADE"**

Dashboard ini menyediakan visualisasi data ekspor UMKM Sulawesi Tengah dengan fitur analisis yang komprehensif, termasuk:
- Analisis tren temporal ekspor
- Identifikasi komoditas unggulan
- Pemetaan negara tujuan ekspor
- Clustering UMKM berdasarkan performa (K-Means)

## 🚀 Instalasi dan Cara Menjalankan

### Prasyarat
Pastikan Anda telah menginstall Python 3.8 atau versi yang lebih baru.

### Langkah Instalasi

1. **Clone atau download repositori ini**

2. **Install dependencies**
   ```bash
   pip install streamlit pandas plotly numpy
   ```

3. **Jalankan dashboard**
   ```bash
   streamlit run dashboard_bi_ekspor_sulteng.py
   ```

4. **Akses dashboard**
   Dashboard akan otomatis terbuka di browser Anda pada alamat:
   ```
   http://localhost:8501
   ```

## 📁 Struktur File

```
project/
│
├── dashboard_bi_ekspor_sulteng.py      # File utama aplikasi Streamlit
├── data_ekspor_umkm_sulteng.csv        # Dataset ekspor UMKM (2020-2024)
├── data_umkm_clustering.csv            # Dataset hasil clustering UMKM
├── README.md                            # Dokumentasi ini
└── requirements.txt                     # Daftar dependencies
```

## 🎯 Fitur Dashboard

### 1. Dashboard Utama
- **KPI Cards**: Total nilai ekspor, volume, jumlah komoditas, dan negara tujuan
- **Tren Bulanan**: Grafik line chart untuk melihat pergerakan ekspor
- **Top 5 Komoditas**: Bar chart horizontal untuk komoditas terbesar
- **Distribusi Negara**: Pie chart negara tujuan ekspor
- **Cluster UMKM**: Visualisasi proporsi cluster performa UMKM

### 2. Tren Ekspor
- **Multi-Line Chart**: Perbandingan tren antar komoditas
- **Analisis Pertumbuhan**: YoY growth rate dengan dual axis
- **Heat Map**: Pola ekspor bulanan lintas tahun
- **Area Chart**: Komposisi kontribusi setiap komoditas

### 3. Komoditas Unggulan
- **Tree Map**: Proporsi nilai ekspor per komoditas
- **Bubble Chart**: Analisis multidimensi (volume vs nilai vs frekuensi)
- **Tabel Detail**: Data lengkap dengan harga per ton

### 4. Negara Tujuan
- **Ranking Chart**: Urutan negara berdasarkan nilai ekspor
- **Heat Map Matrix**: Distribusi komoditas × negara
- **Tren Komparatif**: Perbandingan tren antar negara tujuan

### 5. Clustering UMKM
- **Scatter Plot**: Distribusi UMKM berdasarkan nilai dan volume ekspor
- **Box Plot**: Distribusi nilai ekspor per cluster
- **Ringkasan Cluster**: KPI untuk setiap kategori UMKM
- **Tabel Detail**: Data lengkap semua UMKM dengan filter cluster

## 📊 Data Dummy

Dashboard ini menggunakan **data dummy** yang dibuat secara sintesis dengan karakteristik:

### Data Ekspor UMKM:
- **Periode**: Januari 2020 - Desember 2024 (5 tahun)
- **Total Records**: 3,840 transaksi
- **Komoditas**: 8 jenis (Kakao, Besi dan Baja, Kelapa, Jagung, Produk Perikanan, dll)
- **Negara Tujuan**: 8 negara (Tiongkok, Malaysia, Jepang, AS, dll)
- **Variabel**: Tanggal, Komoditas, Negara Tujuan, Nilai Ekspor (USD), Volume (Ton)

### Data Clustering UMKM:
- **Total UMKM**: 100 unit
- **Cluster 1 - High Performers**: 20 UMKM (20%)
  - Nilai ekspor: US$ 100,000 - 300,000
  - Frekuensi: 20-40 kali ekspor
- **Cluster 2 - Medium Performers**: 30 UMKM (30%)
  - Nilai ekspor: US$ 20,000 - 100,000
  - Frekuensi: 10-20 kali ekspor
- **Cluster 3 - Low Performers**: 50 UMKM (50%)
  - Nilai ekspor: US$ 5,000 - 20,000
  - Frekuensi: 2-10 kali ekspor

## 🎨 Fitur Interaktif

1. **Filter Sidebar**:
   - Filter berdasarkan tahun
   - Multi-select komoditas
   - Multi-select negara tujuan

2. **Responsive Charts**:
   - Semua grafik interaktif dengan hover tooltips
   - Zoom, pan, dan export chart
   - Cross-filtering antar visualisasi

3. **Tab Navigation**:
   - Navigasi mudah antar modul analisis
   - UI yang clean dan profesional

## 🛠️ Teknologi yang Digunakan

- **Streamlit**: Framework untuk membuat web app Python
- **Pandas**: Library untuk manipulasi dan analisis data
- **Plotly**: Library untuk visualisasi interaktif
- **NumPy**: Library untuk komputasi numerik

## 📝 Catatan Penting

- Data yang digunakan adalah **data dummy** untuk keperluan demonstrasi
- Untuk implementasi real, ganti dengan data aktual dari BPS atau sumber resmi
- Dashboard dapat dikustomisasi sesuai kebutuhan
- Pastikan semua file CSV berada dalam folder yang sama dengan file .py

## 👨‍💻 Developer

Dashboard ini dikembangkan sebagai bagian dari tugas akhir:
- **Nama**: Felicia Claudia Pandelaki
- **NIM**: F 521 23 048
- **Program Studi**: S1 Sistem Informasi
- **Universitas**: Universitas Tadulako
- **Tahun**: 2025

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademis dan pembelajaran.

## 🤝 Kontribusi

Jika Anda ingin mengembangkan atau memperbaiki dashboard ini, silakan:
1. Fork repositori
2. Buat branch untuk fitur baru
3. Commit perubahan
4. Push ke branch
5. Buat Pull Request

## 📧 Kontak

Untuk pertanyaan atau saran, silakan hubungi melalui email atau issue di repositori ini.

---

**Selamat menggunakan Dashboard BI Ekspor UMKM Sulawesi Tengah! 🎉**
