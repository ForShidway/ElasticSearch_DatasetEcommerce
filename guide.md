# 📦 Panduan Lengkap — Elasticsearch E-Commerce Project

> **Author:** Fajar Shidiq  
> **Stack:** Elasticsearch · Kibana · Python · CSV Dataset

---

## 📁 Struktur Project

```
ElasticSearch_datasetEcommerce/
│
├── dataset/
│   └── ecommerce_dataset/
│       ├── products.csv       ← data produk
│       ├── users.csv          ← data pengguna
│       ├── orders.csv         ← data pesanan
│       ├── order_items.csv    ← item per pesanan
│       ├── reviews.csv        ← ulasan produk
│       └── events.csv         ← aktivitas/event user
│
├── mapping/
│   └── products_mapping.json  ← contoh mapping untuk index products
│
├── query/
│   ├── search_product.http    ← query full-text search
│   ├── filter_price.http      ← query filter harga
│   └── autocomplete.http      ← query autocomplete/prefix
│
├── scripts/
│   ├── import_products.py     ← import products.csv
│   ├── import_users.py        ← import users.csv
│   ├── import_orders.py       ← import orders.csv
│   ├── import_order_items.py  ← import order_items.csv
│   ├── import_reviews.py      ← import reviews.csv
│   ├── import_events.py       ← import events.csv
│   └── import_all.py          ← import SEMUA dataset sekaligus
│
├── guide.md                   ← (file ini)
└── README.md
```

---

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
pip install pandas elasticsearch
```

> **Catatan:** Versi library `elasticsearch` harus sesuai dengan versi Elasticsearch yang kamu pakai.
> - Elasticsearch 8.x → `pip install elasticsearch==8.*`
> - Elasticsearch 7.x → `pip install elasticsearch==7.*`

Cek versi Elasticsearch yang terinstall:
```
http://localhost:9200  → lihat field "version.number"
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

### Membuat Index + Mapping untuk `products`
Ketik atau copy-paste di Console Dev Tools, lalu tekan tombol **▶ (Run)**:

```json
PUT products
{
  "mappings": {
    "properties": {
      "product_id":   { "type": "keyword" },
      "product_name": { "type": "text" },
      "category":     { "type": "keyword" },
      "price":        { "type": "float" },
      "rating":       { "type": "float" },
      "stock":        { "type": "integer" },
      "description":  { "type": "text" }
    }
  }
}
```

> 💡 **Catatan:** Jika kamu sudah menjalankan script import (Step 4), index sudah otomatis terbuat. Kamu tidak perlu membuat manual lagi, kecuali ingin reset/hapus dan buat ulang.

---

## 🔍 STEP 6 — Menjalankan Query di Kibana Dev Tools

Semua query ini dijalankan di **Kibana Dev Tools** (http://localhost:5601/app/dev_tools).

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
      "product_name": "asus"
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
        "gte": 5000000,
        "lte": 20000000
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
    "prefix": {
      "product_name": "lap"
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

### 7. Cari user berdasarkan negara
```json
GET users/_search
{
  "query": {
    "term": {
      "country": "United States"
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
      "status": "Completed"
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

---

## 📊 STEP 7 — Membuat Dashboard di Kibana

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

## ❓ Troubleshooting Umum

| Masalah | Solusi |
|---|---|
| `ConnectionError: http://localhost:9200` | Pastikan Elasticsearch sudah berjalan |
| `import elasticsearch` gagal | Jalankan `pip install elasticsearch` |
| `ModuleNotFoundError: pandas` | Jalankan `pip install pandas` |
| Script jalan tapi data tidak masuk | Pastikan kamu jalankan dari folder root project, bukan dari `/scripts` |
| Kibana loading lama | Normal, tunggu 1-3 menit pertama kali |
| Error `mapper_parsing_exception` | Field di CSV tidak cocok dengan mapping, cek nama kolom CSV |
| Index sudah ada & ingin reset | Jalankan `DELETE products` di Dev Tools, lalu import ulang |

---

## 🔄 Cara Hapus dan Reset Index

Jika ingin menghapus index dan mengimport ulang, jalankan di **Kibana Dev Tools**:

```json
DELETE products,users,orders,order_items,reviews,events
```

Lalu jalankan kembali script import.

---

## 📌 Ringkasan Perintah Penting

| Aksi | Perintah |
|---|---|
| Jalankan Elasticsearch | `C:\elasticsearch-8.x.x\bin\elasticsearch.bat` |
| Jalankan Kibana | `C:\kibana-8.x.x\bin\kibana.bat` |
| Install Python deps | `pip install pandas elasticsearch` |
| Import semua dataset | `python scripts/import_all.py` |
| Import products saja | `python scripts/import_products.py` |
| Import users saja | `python scripts/import_users.py` |
| Import orders saja | `python scripts/import_orders.py` |
| Import order_items saja | `python scripts/import_order_items.py` |
| Import reviews saja | `python scripts/import_reviews.py` |
| Import events saja | `python scripts/import_events.py` |
| Buka Elasticsearch | http://localhost:9200 |
| Buka Kibana | http://localhost:5601 |
| Buka Dev Tools | http://localhost:5601/app/dev_tools |

---

> 💡 **Tips:** Selalu jalankan Elasticsearch dulu sebelum Kibana dan sebelum script Python!
