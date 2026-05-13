# Elasticsearch E-Commerce Project

## Deskripsi
Project ini merupakan implementasi Elasticsearch sebagai mesin pencarian produk e-commerce menggunakan dataset CSV tanpa backend aplikasi.

## Teknologi
- Elasticsearch
- Kibana
- CSV Dataset

## 📁 Struktur Project

```text
ElasticSearch_datasetEcommerce/
├── dataset/
│   └── ecommerce_dataset/
│       ├── products.csv       ← data produk
│       ├── users.csv          ← data pengguna
│       ├── orders.csv         ← data pesanan
│       ├── order_items.csv    ← item per pesanan
│       ├── reviews.csv        ← ulasan produk
│       └── events.csv         ← aktivitas/event user
│
├── scripts/
│   ├── import_products.py     ← import products.csv
│   ├── import_users.py        ← import users.csv
│   ├── import_orders.py       ← import orders.csv
│   ├── import_order_items.py  ← import order_items.csv
│   ├── import_reviews.py      ← import reviews.csv
│   ├── import_events.py       ← import events.csv
│   └── import_all.py          ← import semua dataset
│
└── README.md
```

## Cara Menjalankan

1. Install Elasticsearch, Install Kibana, dan Jalankan Elasticsearch
2. Jalankan Kibana
3. Install Dependensi Python
4. Import Dataset ke Elasticsearch
5. Buat Index dengan Mapping di Kibana
6. Membuat Dashboard di Kibana

## 🔧 STEP 1 — Jalankan Elasticsearch

### Windows (Manual)
Buka **Command Prompt / PowerShell** lalu jalankan:

```powershell
# Masuk ke folder instalasi Elasticsearch kamu, contoh:
cd C:\elasticsearch-8.x.x\bin

# Jalankan
elasticsearch.bat
```

> ✅ Elasticsearch berjalan di: **http://localhost:9200**

### Cara cek sudah berjalan atau belum
Buka browser dan akses:
```
http://localhost:9200
```
Kalau muncul JSON dengan `"tagline": "You Know, for Search"` → **BERHASIL** ✅

---

## 🔧 STEP 2 — Jalankan Kibana

Buka **Command Prompt / PowerShell baru** (jangan tutup Elasticsearch), lalu:

```powershell
# Masuk ke folder instalasi Kibana kamu, contoh:
cd C:\kibana-8.x.x\bin

# Jalankan
kibana.bat
```

> ✅ Kibana berjalan di: **http://localhost:5601**

Tunggu beberapa menit hingga Kibana selesai loading, lalu buka di browser:
```
http://localhost:5601
```

---

## 🐍 STEP 3 — Install Dependensi Python

Buka terminal baru di folder project ini, lalu install library yang diperlukan:

```powershell
python -m pip install --upgrade pip
python -m pip install elasticsearch
```

---

## 📤 STEP 4 — Import Dataset ke Elasticsearch

> ⚠️ **Pastikan kamu menjalankan perintah ini dari folder root project** (`ElasticSearch_datasetEcommerce/`), bukan dari dalam folder `scripts/`.

### Opsi A: Import Semua Dataset Sekaligus ⭐ (Direkomendasikan)

```powershell
python scripts/import_all.py
```

Script ini akan otomatis membuat index dan mengimport **semua 6 dataset** sekaligus:
- `products` ← dari products.csv
- `users` ← dari users.csv
- `orders` ← dari orders.csv
- `order_items` ← dari order_items.csv
- `reviews` ← dari reviews.csv
- `events` ← dari events.csv

---

### Opsi B: Import Satu per Satu (Per Dataset)

```powershell
# Import hanya Products
python scripts/import_products.py

# Import hanya Users
python scripts/import_users.py

# Import hanya Orders
python scripts/import_orders.py

# Import hanya Order Items
python scripts/import_order_items.py

# Import hanya Reviews
python scripts/import_reviews.py

# Import hanya Events
python scripts/import_events.py
```

---

## 🗺️ STEP 5 — Buat Index dengan Mapping di Kibana

Setelah Kibana terbuka di http://localhost:5601, ikuti langkah berikut:

### Cara masuk ke Dev Tools Kibana
1. Klik menu hamburger (☰) di pojok kiri atas
2. Scroll ke bawah → klik **"Dev Tools"**
3. Atau langsung akses: `http://localhost:5601/app/dev_tools`

## Contoh Query Search

### 1. Cek semua index yang ada
```json
GET _cat/indices?v
```

### 2. Full-text Search Produk
```json
GET products/_search
{
  "query": {
    "match": {
      "product_name": "Nimbus"
    }
  }
}
```

### 3. Filter Harga (range)
```json
GET products/_search
{
  "query": {
    "range": {
      "price": {
        "gte": 50.0,
        "lte": 200.0
      }
    }
  }
}
```

### 4. Autocomplete / Prefix Search
```json
GET products/_search
{
  "query": {
    "match_phrase_prefix": {
      "product_name": "Lap"
    }
  }
}
```

### 5. Lihat semua data (products)
```json
GET products/_search
{
  "query": { "match_all": {} },
  "size": 10
}
```

### 6. Cek jumlah dokumen dalam index
```json
GET products/_count
```

### 7. Cari user berdasarkan kota
```json
GET users/_search
{
  "query": {
    "term": {
      "city": "New Roberttown"
    }
  }
}
```

### 8. Filter orders berdasarkan status
```json
GET orders/_search
{
  "query": {
    "term": {
      "order_status": "completed"
    }
  }
}
```

### 9. Cari reviews dengan rating tinggi
```json
GET reviews/_search
{
  "query": {
    "range": {
      "rating": { "gte": 4.5 }
    }
  }
}
```
## 📊 STEP 6 — Membuat Dashboard di Kibana

### A. Buat Data View (Index Pattern)
Data View diperlukan agar Kibana bisa membaca data dari Elasticsearch.

1. Buka Kibana → klik menu **☰**
2. Masuk ke **Stack Management** (atau **Management**)
3. Klik **"Data Views"** (atau "Index Patterns" di versi lama)
4. Klik **"Create data view"**
5. Isi **Name**: `products*` (atau nama index yang diinginkan)
6. Isi **Index pattern**: `products*`
7. Klik **"Save data view to Kibana"**

> Ulangi untuk index lain: `users*`, `orders*`, `order_items*`, `reviews*`, `events*`

---

### B. Buat Visualisasi

1. Klik menu **☰** → **Analytics** → **Visualize Library**
2. Klik **"Create visualization"**
3. Pilih tipe visualisasi:
   - **Bar chart** → distribusi kategori produk
   - **Pie chart** → komposisi status order
   - **Line chart** → tren event per waktu
   - **Metric** → total produk, total user
4. Pilih Data View yang sesuai
5. Konfigurasi sumbu X dan Y sesuai kebutuhan
6. Klik **"Save"**

---

### C. Buat Dashboard

1. Klik menu **☰** → **Analytics** → **Dashboard**
2. Klik **"Create dashboard"**
3. Klik **"Add from library"** → pilih visualisasi yang sudah dibuat
4. Atur tata letak drag & drop
5. Klik **"Save"** → beri nama dashboard


---

## Hasil
Sistem mampu melakukan pencarian produk dengan cepat menggunakan Elasticsearch serta visualisasi data menggunakan Kibana.

## Author
Fajar Shidiq