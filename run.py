from app import create_app, db

app = create_app()

# Initialize database tables
with app.app_context():
    db.create_all()

# This is needed for Vercel
if __name__ == '__main__':
    app.run(debug=True)