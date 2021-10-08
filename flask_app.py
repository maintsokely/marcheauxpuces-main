# A simple Flask app...

from flask import Flask,render_template, url_for,request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
db = SQLAlchemy(app)

class Objet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    vendu = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Objet %r>' % self.id

@app.route('/details/<int:id>')
def showDetails(id):
        objetDetails=Objet.query.get_or_404(id)
        return render_template('details.html', objetDetails=objetDetails)

@app.route('/ajouter', methods=['POST','GET'])
def ajout():
    if request.method == 'POST':
        imageObject = request.form['image']
        descriptionObjet = request.form['description']
        nouvelObjet = Objet(description=descriptionObjet, image=imageObject)
        try:
            db.session.add(nouvelObjet)
            db.session.commit()
            return redirect('/')
        except:
            return 'Houtson, we have a problem...'

    else:
        return render_template('add.html')

@app.route('/delete/<int:id>')
def deleteObjet(id):
    if request.method == 'GET':
        objet=Objet.query.get_or_404(id)
        try:
            db.session.delete(objet)
            db.session.commit()
            return redirect('/')
        except:
            return 'Houtson, we have a problem...'
    return render_template('index.html')


@app.route('/reserve/<int:id>')
def reserve(id):
    if id == 5:
        resp = Response('Désolé! Cet article est déjà réservé par Réal...', status=200);
        return resp
    elif id == 4:
        resp = "Désolé! Cet article est déjà réservé par François..."
        return resp
    else :
        resp = "Désolé! Cet article est déjà réservé par Éric..."
        return resp

@app.route('/')
def index():
        objets = Objet.query.order_by(Objet.date_created).filter_by(vendu=0).all()
        return render_template('index.html', objets=objets )

