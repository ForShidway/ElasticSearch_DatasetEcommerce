"""
Script Import: reviews.csv → Elasticsearch index 'reviews'
Jalankan dengan: python scripts/import_reviews.py
Pastikan sudah install: pip install pandas elasticsearch
"""
import pandas as pd
from elasticsearch import Elasticsearch, helpers
import math

# Koneksi ke Elasticsearch
es = Elasticsearch("http://localhost:9200")
index_name = "reviews"

# Buat index dengan mapping
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body={
        "mappings": {
            "properties": {
                "review_id":    {"type": "keyword"},
                "order_id":     {"type": "keyword"},
                "user_id":      {"type": "keyword"},
                "product_id":   {"type": "keyword"},
                "rating":       {"type": "float"},
                "comment":      {"type": "text"},
                "created_at":   {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"}
            }
        }
    })
    print(f"Index '{index_name}' berhasil dibuat.")

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
            "_id": i + 1,
            "_source": doc
        }

helpers.bulk(es, gen_docs(df))
print(f"✅ Berhasil import {len(df)} dokumen ke index '{index_name}'")
