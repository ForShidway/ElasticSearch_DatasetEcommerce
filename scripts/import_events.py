"""
=============================================================
 Script Import: events.csv → Elasticsearch index 'events'
 Cara jalankan: python scripts/import_events.py
 Requirement  : pip install pandas elasticsearch
=============================================================
"""

# ─────────────────────────────────────────────
# BAGIAN 1: IMPORT LIBRARY
# ─────────────────────────────────────────────

# pandas → library untuk membaca dan mengolah file CSV
# kita singkat jadi "pd" supaya lebih mudah diketik
import pandas as pd

# Elasticsearch → class utama untuk konek ke Elasticsearch
# helpers      → utilitas bantu, khususnya untuk "bulk insert"
#                (insert banyak data sekaligus, jauh lebih cepat
#                 daripada insert satu per satu)
from elasticsearch import Elasticsearch, helpers

# math → dibutuhkan untuk cek nilai NaN (Not a Number)
# CSV sering punya cell kosong, dan pandas mengisinya dengan NaN
# Elasticsearch tidak bisa terima NaN, jadi harus diganti None
import math


# ─────────────────────────────────────────────
# BAGIAN 2: KONEKSI KE ELASTICSEARCH
# ─────────────────────────────────────────────

# Buat koneksi ke Elasticsearch yang berjalan di komputer lokal
# port default Elasticsearch adalah 9200
es = Elasticsearch("http://localhost:9200")

# Nama index yang akan dibuat di Elasticsearch
# Index = seperti "tabel" kalau di database biasa (MySQL, dsb)
index_name = "events"


# ─────────────────────────────────────────────
# BAGIAN 3: BUAT INDEX + MAPPING
# ─────────────────────────────────────────────

# Cek dulu apakah index sudah ada atau belum
# Kalau belum ada → buat baru dengan mapping
# Kalau sudah ada → skip, langsung ke import data
if not es.indices.exists(index=index_name):

    # es.indices.create() → perintah untuk membuat index baru
    # "mappings" → mendefinisikan struktur data / tipe setiap field
    # Ini seperti mendefinisikan kolom di tabel database
    es.indices.create(index=index_name, body={
        "mappings": {
            "properties": {

                # "keyword" → teks yang TIDAK dianalisis/dipecah
                # cocok untuk ID, kode, status, dsb
                # bisa dipakai untuk filter exact match
                "event_id":   {"type": "keyword"},
                "user_id":    {"type": "keyword"},
                "product_id": {"type": "keyword"},
                "event_type": {"type": "keyword"},  # contoh: "view", "purchase", "cart"
                "session_id": {"type": "keyword"},

                # "date" → tipe khusus untuk tanggal/waktu
                # "format" → mendaftarkan format tanggal yang diizinkan
                # karena CSV bisa punya format tanggal yang berbeda-beda
                "event_time": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                }
            }
        }
    })
    print(f"Index '{index_name}' berhasil dibuat.")


# ─────────────────────────────────────────────
# BAGIAN 4: BACA FILE CSV
# ─────────────────────────────────────────────

# pd.read_csv() → membaca file CSV dan mengubahnya jadi DataFrame
# DataFrame = semacam tabel data di Python (mirip Excel)
df = pd.read_csv("dataset/ecommerce_dataset/events.csv")

# df.where(pd.notnull(df), None) → ganti semua nilai NaN jadi None
# NaN = cell kosong di CSV
# Elasticsearch tidak bisa menerima NaN, harus diubah ke None
df = df.where(pd.notnull(df), None)


# ─────────────────────────────────────────────
# BAGIAN 5: FUNGSI GENERATOR DOKUMEN
# ─────────────────────────────────────────────

# Fungsi ini menghasilkan dokumen satu per satu (generator)
# Dipakai oleh helpers.bulk() untuk mengirim data secara efisien
def gen_docs(df):

    # df.iterrows() → loop baris per baris di DataFrame
    # i = nomor baris (0, 1, 2, ...)
    # row = isi satu baris data
    for i, row in df.iterrows():

        # Ubah satu baris menjadi dictionary Python
        # contoh: {"event_id": "E001", "user_id": "U123", ...}
        doc = row.to_dict()

        # Bersihkan nilai NaN yang tersisa (double-check)
        # isinstance(v, float) → cek apakah nilainya float
        # math.isnan(v)       → cek apakah nilainya NaN
        # Kalau NaN → ganti dengan None (null di JSON)
        doc = {
            k: (None if (isinstance(v, float) and math.isnan(v)) else v)
            for k, v in doc.items()
        }

        # "yield" → mengembalikan data satu per satu (generator)
        # Lebih hemat memori daripada return list sekaligus
        yield {
            "_index": index_name,   # nama index tujuan
            "_id": i + 1,           # ID dokumen (mulai dari 1)
            "_source": doc          # isi/konten dokumen
        }


# ─────────────────────────────────────────────
# BAGIAN 6: KIRIM DATA KE ELASTICSEARCH
# ─────────────────────────────────────────────

# helpers.bulk() → kirim BANYAK dokumen sekaligus ke Elasticsearch
# Jauh lebih cepat daripada es.index() satu per satu
# Bayangkan: kalau ada 100.000 baris, bulk bisa 10x lebih cepat
helpers.bulk(es, gen_docs(df))

print(f"✅ Berhasil import {len(df)} dokumen ke index '{index_name}'")
