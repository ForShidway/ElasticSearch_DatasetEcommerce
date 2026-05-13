"""
Script Import ALL — Import semua dataset sekaligus ke Elasticsearch
Jalankan dengan: python scripts/import_all.py
Pastikan sudah install: pip install pandas elasticsearch
Pastikan Elasticsearch sedang berjalan di http://localhost:9200
"""
import pandas as pd
from elasticsearch import Elasticsearch, helpers
import math
import time

es = Elasticsearch("http://localhost:9200")

# ============================================================
# Konfigurasi semua dataset
# Format: (nama_index, path_csv, mapping_properties)
# ============================================================
DATASETS = [
    (
        "products",
        "dataset/ecommerce_dataset/products.csv",
        {
            "product_id":   {"type": "keyword"},
            "product_name": {"type": "text"},
            "category":     {"type": "keyword"},
            "price":        {"type": "float"},
            "rating":       {"type": "float"},
            "stock":        {"type": "integer"},
            "description":  {"type": "text"}
        }
    ),
    (
        "users",
        "dataset/ecommerce_dataset/users.csv",
        {
            "id":             {"type": "keyword"},
            "first_name":     {"type": "text"},
            "last_name":      {"type": "text"},
            "email":          {"type": "keyword"},
            "age":            {"type": "integer"},
            "gender":         {"type": "keyword"},
            "state":          {"type": "keyword"},
            "city":           {"type": "keyword"},
            "country":        {"type": "keyword"},
            "zip":            {"type": "keyword"},
            "latitude":       {"type": "float"},
            "longitude":      {"type": "float"},
            "traffic_source": {"type": "keyword"},
            "created_at":     {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"}
        }
    ),
    (
        "orders",
        "dataset/ecommerce_dataset/orders.csv",
        {
            "order_id":     {"type": "keyword"},
            "user_id":      {"type": "keyword"},
            "status":       {"type": "keyword"},
            "created_at":   {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
            "returned_at":  {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
            "shipped_at":   {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
            "delivered_at": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
            "num_of_item":  {"type": "integer"}
        }
    ),
    (
        "order_items",
        "dataset/ecommerce_dataset/order_items.csv",
        {
            "id":                {"type": "keyword"},
            "order_id":          {"type": "keyword"},
            "user_id":           {"type": "keyword"},
            "product_id":        {"type": "keyword"},
            "inventory_item_id": {"type": "keyword"},
            "status":            {"type": "keyword"},
            "created_at":        {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
            "shipped_at":        {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
            "delivered_at":      {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
            "returned_at":       {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
            "sale_price":        {"type": "float"}
        }
    ),
    (
        "reviews",
        "dataset/ecommerce_dataset/reviews.csv",
        {
            "review_id":  {"type": "keyword"},
            "order_id":   {"type": "keyword"},
            "user_id":    {"type": "keyword"},
            "product_id": {"type": "keyword"},
            "rating":     {"type": "float"},
            "comment":    {"type": "text"},
            "created_at": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"}
        }
    ),
    (
        "events",
        "dataset/ecommerce_dataset/events.csv",
        {
            "event_id":   {"type": "keyword"},
            "user_id":    {"type": "keyword"},
            "product_id": {"type": "keyword"},
            "event_type": {"type": "keyword"},
            "event_time": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
            "session_id": {"type": "keyword"}
        }
    ),
]


def clean_doc(row_dict):
    """Bersihkan nilai NaN agar tidak error saat insert"""
    return {k: (None if (isinstance(v, float) and math.isnan(v)) else v) for k, v in row_dict.items()}


def gen_docs(df, index_name):
    for i, row in df.iterrows():
        yield {
            "_index": index_name,
            "_id": i + 1,
            "_source": clean_doc(row.to_dict())
        }


def import_dataset(index_name, csv_path, mapping_props):
    print(f"\n{'='*55}")
    print(f"📂 Memproses: {csv_path}")
    print(f"   → Index target: {index_name}")

    # Buat index jika belum ada
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body={"mappings": {"properties": mapping_props}})
        print(f"   ✔ Index '{index_name}' berhasil dibuat.")
    else:
        print(f"   ℹ  Index '{index_name}' sudah ada, skip pembuatan.")

    # Baca dan import CSV
    df = pd.read_csv(csv_path)
    df = df.where(pd.notnull(df), None)

    success, failed = helpers.bulk(es, gen_docs(df, index_name), stats_only=False, raise_on_error=False)
    print(f"   ✅ Import selesai: {success} dokumen berhasil, {len(failed)} gagal.")


# ============================================================
# Jalankan semua
# ============================================================
print("🚀 Memulai import semua dataset ke Elasticsearch...")
start = time.time()

for idx_name, csv_path, mapping in DATASETS:
    try:
        import_dataset(idx_name, csv_path, mapping)
    except Exception as e:
        print(f"   ❌ Error pada '{idx_name}': {e}")

elapsed = time.time() - start
print(f"\n{'='*55}")
print(f"🎉 Semua dataset selesai diimport! (waktu: {elapsed:.1f} detik)")
print("Buka Kibana di http://localhost:5601 untuk melihat data.")
