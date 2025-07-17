# url_shortener/app.py
from flask import Flask, request, jsonify, render_template, redirect
from flask_migrate import Migrate
from database import db
from models import ShortURL
from utils import generate_short_code

app = Flask(__name__)

# ✅ Configure your MySQL credentials here
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/shortener'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Initialize DB
db.init_app(app)
migrate = Migrate(app, db)
# Home Route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400

    short_code = generate_short_code()
    while ShortURL.query.filter_by(short_code=short_code).first():
        short_code = generate_short_code()

    new_url = ShortURL(url=data['url'], short_code=short_code)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        'id': new_url.id,
        'url': new_url.url,
        'shortCode': new_url.short_code,
        'createdAt': new_url.created_at.isoformat(),
        'updatedAt': new_url.updated_at.isoformat()
    }), 201

@app.route('/shorten/<string:short_code>', methods=['GET'])
def get_original_url(short_code):
    record = ShortURL.query.filter_by(short_code=short_code).first()
    if not record:
        return jsonify({'error': 'Short URL not found'}), 404

    record.access_count += 1
    db.session.commit()

    return jsonify({
        'id': record.id,
        'url': record.url,
        'shortCode': record.short_code,
        'createdAt': record.created_at.isoformat(),
        'updatedAt': record.updated_at.isoformat()
    })

@app.route('/shorten/<string:short_code>', methods=['PUT'])
def update_short_url(short_code):
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400

    record = ShortURL.query.filter_by(short_code=short_code).first()
    if not record:
        return jsonify({'error': 'Short URL not found'}), 404

    record.url = data['url']
    db.session.commit()

    return jsonify({
        'id': record.id,
        'url': record.url,
        'shortCode': record.short_code,
        'createdAt': record.created_at.isoformat(),
        'updatedAt': record.updated_at.isoformat()
    })
#Delete Short URL
@app.route('/shorten/<string:short_code>', methods=['DELETE'])
def delete_short_url(short_code):
    record = ShortURL.query.filter_by(short_code=short_code).first()
    if not record:
        return '', 404

    db.session.delete(record)
    db.session.commit()
    return '', 204
# Get URL Stats
@app.route('/shorten/<string:short_code>/stats', methods=['GET'])
def get_url_stats(short_code):
    record = ShortURL.query.filter_by(short_code=short_code).first()
    if not record:
        return jsonify({'error': 'Short URL not found'}), 404

    return jsonify({
        'id': record.id,
        'url': record.url,
        'shortCode': record.short_code,
        'createdAt': record.created_at.isoformat(),
        'updatedAt': record.updated_at.isoformat(),
        'accessCount': record.access_count
    })

# Redirect to original URL
@app.route('/r/<string:short_code>')
def redirect_short_code(short_code):
    record = ShortURL.query.filter_by(short_code=short_code).first()
    if not record:
        return jsonify({'error': 'Short URL not found'}), 404
    record.access_count += 1
    db.session.commit()
    return redirect(record.url)



if __name__ == '__main__':
    app.run(debug=True)
#url_shortener/app.py
