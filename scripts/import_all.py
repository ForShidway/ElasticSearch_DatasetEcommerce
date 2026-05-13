"""
Script Import All Datasets: products, users, orders, order_items, reviews, events
Jalankan dengan: python scripts/import_all.py
"""
import os

print("Memulai proses import semua dataset...\n")

scripts = [
    "import_products.py",
    "import_users.py",
    "import_orders.py",
    "import_order_items.py",
    "import_reviews.py",
    "import_events.py"
]

for script in scripts:
    script_path = os.path.join("scripts", script)
    print(f"--- Menjalankan {script} ---")
    os.system(f"python {script_path}")
    print("\n")

print("✅ Semua dataset berhasil diimport!")
