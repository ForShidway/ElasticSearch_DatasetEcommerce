# Elasticsearch E-Commerce Project

## Deskripsi
Project ini merupakan implementasi Elasticsearch sebagai mesin pencarian produk e-commerce menggunakan dataset CSV tanpa backend aplikasi.

## Fitur
- Full-text Search
- Filter Harga
- Sorting Produk
- Autocomplete
- Dashboard Visualisasi

## Teknologi
- Elasticsearch
- Kibana
- CSV Dataset

## Struktur Project

elasticsearch-ecommerce-project/
│
├── dataset/
├── queries/
├── mappings/
├── screenshots/
├── docs/
├── README.md
└── setup_guide.md

## Cara Menjalankan

1. Install Elasticsearch
2. Install Kibana
3. Jalankan Elasticsearch
4. Jalankan Kibana
5. Upload dataset CSV
6. Buat index menggunakan mapping
7. Jalankan query Elasticsearch

## Contoh Query Search

GET products/_search
{
  "query": {
    "match": {
      "product_name": "asus"
    }
  }
}

## Hasil
Sistem mampu melakukan pencarian produk dengan cepat menggunakan Elasticsearch serta visualisasi data menggunakan Kibana.

## Author
Fajar Shidiq