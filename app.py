from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
db = SQLAlchemy(app)

# Veritabanı modelleri
class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(200))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    tag = db.relationship('Tag', backref=db.backref('links', lazy=True))
    color = db.Column(db.String(20))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    color = db.Column(db.String(20))

# Veritabanı modellerini oluştur
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    with app.app_context():
        links = Link.query.all()
        tags = Tag.query.all()
        colors = [
            {"name": "Renk Seçiniz", "value": ""},
            {"name": "Kırmızı", "value": "#ff0000"},
            {"name": "Yeşil", "value": "#00ff00"},
            {"name": "Mavi", "value": "#0000ff"},
            {"name": "Sarı", "value": "#ffff00"},
            {"name": "Turuncu", "value": "#ffa500"},
            {"name": "Mor", "value": "#800080"},
            {"name": "Pembe", "value": "#ffc0cb"},
            {"name": "Turkuaz", "value": "#40e0d0"},
            {"name": "Gri", "value": "#808080"},
            {"name": "Siyah", "value": "#000000"},
            {"name": "Beyaz", "value": "#ffffff"},
            {"name": "Sarımsı Yeşil", "value": "#adff2f"}
        ]
        return render_template('index.html', links=links, colors=colors, tags=tags)

@app.route('/add_link', methods=['POST'])
def add_link():
    name = request.form['name']
    url = request.form['url']
    tag_name = request.form['tag']
    color = request.form['colorSelect']

    with app.app_context():
        tag = None
        if not tag_name:
            default_tag = Tag.query.filter_by(name="Etiket Seçiniz").first()
            if default_tag:
                tag_name = default_tag.name
                color = default_tag.color
        else:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name, color=color)
                db.session.add(tag)
                db.session.commit()
            else:
                color = tag.color

        new_link = Link(name=name, url=url, tag=tag, color=color)
        db.session.add(new_link)
        db.session.commit()

        links = Link.query.all()
        tags = Tag.query.all()
        colors = [
            {"name": "Renk Seçiniz", "value": ""},
            {"name": "Kırmızı", "value": "#ff0000"},
            {"name": "Yeşil", "value": "#00ff00"},
            {"name": "Mavi", "value": "#0000ff"},
            {"name": "Sarı", "value": "#ffff00"},
            {"name": "Turuncu", "value": "#ffa500"},
            {"name": "Mor", "value": "#800080"},
            {"name": "Pembe", "value": "#ffc0cb"},
            {"name": "Turkuaz", "value": "#40e0d0"},
            {"name": "Gri", "value": "#808080"},
            {"name": "Siyah", "value": "#000000"},
            {"name": "Beyaz", "value": "#ffffff"},
            {"name": "Sarımsı Yeşil", "value": "#adff2f"}
        ]

        return render_template('index.html', links=links, colors=colors, tags=tags, selected_tag_name=tag_name, selected_color=color)

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    with app.app_context():
        filtered_links = Link.query.filter(Link.name.contains(query)).all()
        tags = Tag.query.all()
        colors = [
            {"name": "Renk Seçiniz", "value": ""},
            {"name": "Kırmızı", "value": "#ff0000"},
            {"name": "Yeşil", "value": "#00ff00"},
            {"name": "Mavi", "value": "#0000ff"},
            {"name": "Sarı", "value": "#ffff00"},
            {"name": "Turuncu", "value": "#ffa500"},
            {"name": "Mor", "value": "#800080"},
            {"name": "Pembe", "value": "#ffc0cb"},
            {"name": "Turkuaz", "value": "#40e0d0"},
            {"name": "Gri", "value": "#808080"},
            {"name": "Siyah", "value": "#000000"},
            {"name": "Beyaz", "value": "#ffffff"},
            {"name": "Sarımsı Yeşil", "value": "#adff2f"}
        ]
        return render_template('index.html', links=filtered_links, colors=colors, tags=tags)

if __name__ == '__main__':
    app.run(debug=True)
