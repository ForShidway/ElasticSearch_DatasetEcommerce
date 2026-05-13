"""
Script Import: reviews.csv → Elasticsearch index 'reviews'
Jalankan dengan: python scripts/import_reviews.py
"""
import pandas as pd
from elasticsearch import Elasticsearch, helpers
import math

# Koneksi ke Elasticsearch
es = Elasticsearch("http://localhost:9200")
index_name = "reviews"

# Buat index dengan mapping jika belum ada
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body={
        "mappings": {
            "properties": {
                "review_id":    {"type": "keyword"},
                "order_id":     {"type": "keyword"},
                "product_id":   {"type": "keyword"},
                "user_id":      {"type": "keyword"},
                "rating":       {"type": "float"},
                "review_text":  {"type": "text"},
                "review_date":  {"type": "date"}
            }
        }
    })
    print(f"Index '{index_name}' berhasil dibuat.")
else:
    print(f"Index '{index_name}' sudah ada, skip pembuatan mapping.")

# Baca CSV
df = pd.read_csv("dataset/ecommerce_dataset/reviews.csv")
df = df.where(pd.notnull(df), None)

# Bulk insert
def gen_docs(df):
    for i, row in df.iterrows():
        doc = row.to_dict()
        doc = {k: (None if (isinstance(v, float) and math.isnan(v)) else v) for k, v in doc.items()}
        yield {
            "_index": index_name,
            "_id": doc["review_id"],
            "_source": doc
        }

helpers.bulk(es, gen_docs(df))
print(f"✅ Berhasil import {len(df)} dokumen ke index '{index_name}'")
