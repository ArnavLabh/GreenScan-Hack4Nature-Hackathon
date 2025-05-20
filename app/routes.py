from flask import render_template, request, jsonify
from app import app
import json
import os

def load_products():
    with open('data/products.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    barcode = None
    error = None
    
    if request.method == 'POST':
        barcode = request.form.get('barcode')
    elif request.method == 'GET':
        barcode = request.args.get('barcode')
    
    if not barcode:
        error = "No barcode provided"
        return render_template('result.html', error=error)
    
    products = load_products()
    product = next((p for p in products if p['barcode'] == barcode), None)
    
    if not product:
        error = f"Product with barcode {barcode} not found"
        return render_template('result.html', error=error)
    
    return render_template('result.html', product=product)

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    category = request.args.get('category', '')
    
    products = load_products()
    
    if not query and not category:
        return render_template('search.html', products=products, query='', category='')
    
    results = []
    for product in products:
        if category and product['category'].lower() != category.lower():
            continue
        if query and query not in product['name'].lower():
            continue
        results.append(product)
    
    return render_template('search.html', products=results, query=query, category=category)

@app.route('/categories')
def get_categories():
    products = load_products()
    categories = list(set(p['category'] for p in products))
    return jsonify(categories)

@app.route('/api/scan', methods=['POST'])
def api_scan():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Here you would implement the barcode scanning logic
    # For now, we'll return a mock response
    return jsonify({
        'success': True,
        'barcode': '8906017290064'  # Example barcode
    })