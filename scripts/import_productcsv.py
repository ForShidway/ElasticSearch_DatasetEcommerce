# jalankan dulu : pip install pandas elasticsearch
import pandas as pd
from elasticsearch import Elasticsearch

# Koneksi ke Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Baca file CSV
df = pd.read_csv("../dataset/products.csv")

# nama index
index_name = "products"

#  import data ke elasticsearch
for i, row in df.iterrows():
    doc = {
        "product_id": row["product_id"],
        "product_name": row["product_name"],
        "category": row["category"],
        "price": float(row["price"]),
        "rating": float(row["rating"]),
        "stock": int(row["stock"]),
        "description": row["description"]
    }
    es.index(index=index_name, id=i+1, document=doc)
    
print("Data berhasil di import ke Elasticsearch")