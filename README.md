# fatima-innovaxel-najam

# URL Shortener 

This is a simple RESTful URL shortener built with Flask, SQLAlchemy, and a responsive frontend.

## 🔧 Setup Instructions

1.Clone and switch to dev branch
git clone https://github.com/najamfatim/fatima-innovaxel-najam.git
cd fatima-innovaxel-najam
git checkout dev

2. Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run the app
flask db init
flask db migrate
flask db upgrade
python app.py
Visit: http://localhost:5000/

✨ Features
Create short URLs from long links

Redirect short link to original

View stats (access count, creation time, etc.)

Delete short URLs

Modern responsive frontend

⚙️ Technologies
Flask

SQLAlchemy

JavaScript (Fetch API)

HTML/CSS

