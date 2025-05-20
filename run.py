from app import app, db
from app.models import Product
import json

def load_products():
    try:
        with open('data/products.json') as f:
            products = json.load(f)
            for p in products:
                if not Product.query.filter_by(barcode=p['barcode']).first():
                    product = Product(barcode=p['barcode'], name=p['name'], instructions=p['instructions'])
                    db.session.add(product)
            db.session.commit()
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading products: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        load_products()
    app.run(debug=True)