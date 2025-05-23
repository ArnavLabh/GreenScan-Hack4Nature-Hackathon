# GreenScan - Sustainable Product Scanner

GreenScan is an innovative web application that helps users make environmentally conscious decisions by scanning product barcodes and providing detailed information about their recyclability and environmental impact.

---

## ⚠️ Prototype Notice

This is a prototype version of GreenScan. Currently, only 10 products are available in the database.

### Available Products
- **Bisleri Mineral Water Bottle** : 8906017290033  
- **Lay's Classic Potato Chips** : 8901012000022  
- **Coca-Cola Glass Bottle** : 8901012000039  
- **Amul Milk Tetra Pack** : 8901012000046  
- **Maggi Noodles Pack** : 8901012000053  
- **Parle-G Biscuit Pack** : 8901012000060  
- **Dabur Honey Glass Jar** : 8901012000077  
- **Kurkure Snack Pack** : 8901012000084  
- **Amul Butter Paper Pack** : 8901012000091  
- **Sprite Plastic Bottle** : 8901012000107  

### 🔗 Barcode Image Access
You can access the barcode images (which can be used on the barcode scanner to test the app) through the following link:  
[Barcode Image Folder on Google Drive](https://drive.google.com/drive/folders/1iaKOzFiKthmpcbKhoKwxVl65RhNtJZae?usp=sharing)

---

## ✨ Features

- 📱 **Barcode Scanning**: Scan product barcodes using your device's camera
- 📸 **Image Upload**: Upload product images for barcode detection
- 🔍 **Product Search**: Search for products by name or barcode
- ♻️ **Recyclability Info**: Get detailed information about product recyclability
- 📊 **Environmental Impact**: View carbon footprint and sustainability scores
- 💡 **Alternative Suggestions**: Discover eco-friendly alternatives
- 📝 **Recycling Instructions**: Get specific recycling guidelines
- 👤 **User Profiles**: Track your scanning history and environmental impact

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A modern web browser

### Installation (Locally)

1. Clone the repository:
```bash
git clone https://github.com/ArnavLabh/GreenScan-Hack4Nature-Hackathon.git
cd greenscan
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Run the application:
```bash
flask run
```

The application will be available at `http://localhost:5000`

---

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite
- **Barcode Scanning**: HTML5-QRCode
- **Styling**: Bootstrap 5
- **Icons**: Font Awesome

---

## 📱 Usage

1. **Scan a Product**:
   - Click the "Scan" button
   - Use your camera to scan a product barcode
   - Or upload an image containing a barcode

2. **View Results**:
   - Get detailed information about the product
   - Check recyclability status
   - View environmental impact
   - See alternative suggestions

3. **Search Products**:
   - Use the search bar to find products
   - Filter by name or barcode
   - View detailed product information

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
