"""
Script Import: events.csv → Elasticsearch index 'events'
Jalankan dengan: python scripts/import_events.py
"""
import pandas as pd
from elasticsearch import Elasticsearch, helpers
import math

# Koneksi ke Elasticsearch
es = Elasticsearch("http://localhost:9200")
index_name = "events"

# Buat index dengan mapping jika belum ada
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body={
        "mappings": {
            "properties": {
                "event_id":         {"type": "keyword"},
                "user_id":          {"type": "keyword"},
                "product_id":       {"type": "keyword"},
                "event_type":       {"type": "keyword"},
                "event_timestamp":  {"type": "date"}
            }
        }
    })
    print(f"Index '{index_name}' berhasil dibuat.")
else:
    print(f"Index '{index_name}' sudah ada, skip pembuatan mapping.")

# Baca CSV
df = pd.read_csv("dataset/ecommerce_dataset/events.csv")
df = df.where(pd.notnull(df), None)

# Bulk insert
def gen_docs(df):
    for i, row in df.iterrows():
        doc = row.to_dict()
        doc = {k: (None if (isinstance(v, float) and math.isnan(v)) else v) for k, v in doc.items()}
        yield {
            "_index": index_name,
            "_id": doc["event_id"],
            "_source": doc
        }

helpers.bulk(es, gen_docs(df))
print(f"✅ Berhasil import {len(df)} dokumen ke index '{index_name}'")
