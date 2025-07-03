# uvoz potrebnih biblioteka
from pickle import APPEND
from flask import Flask, render_template, url_for, request, redirect, session
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text

# deklaracija Flask aplikacije
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'  # Povezivanje sa SQLite bazom
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Isključivanje praćenja promena objekata
db = SQLAlchemy(app)

def get_db_connection():
    conn = sqlite3.connect('baza.db')
    conn.row_factory = sqlite3.Row
    return conn


class Knjiga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    datum_izdanja = db.Column(db.String(20), nullable=False)
    stanje = db.Column(db.String(20), nullable=False)
    cena = db.Column(db.Integer, nullable=False)

class Korisnik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(100), nullable=False)
    prezime = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    datum_upisa = db.Column(db.String(20), nullable=False)
    lozinka = db.Column(db.String(100), nullable=False)

class Bibliotekar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(100), nullable=False)
    prezime = db.Column(db.String(100), nullable=False)
    obrazovanje = db.Column(db.String(255), nullable=False)
    radno_iskustvo = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefon = db.Column(db.String(20), nullable=False)

# logika aplikacije
@app.before_request
def init_db():
    db.create_all()  # Kreira tabele ako ne postoje

@app.route('/korisnici', methods=['GET'])
def render_korisnici():
    korisnici = Korisnik.query.all()  # Uzmi sve korisnike iz baze
    return render_template('korisnici.html', korisnici=korisnici)

@app.route('/korisnik-novi', methods=["GET", "POST"])
def korisnik_novi():
    if request.method == 'POST':
        forma = request.form
        novi_korisnik = Korisnik(
            ime=forma['ime'],
            prezime=forma['prezime'],
            email=forma['email'],
            datum_upisa=forma['datum_upisa'],
            lozinka=forma['lozinka']
        )
        db.session.add(novi_korisnik)
        db.session.commit()
        return redirect(url_for('render_korisnici'))

    return render_template('korisnik-novi.html')

@app.route('/korisnik_izmena/<id>', methods=["GET", "POST"])
def korisnik_izmena(id):
    korisnik = Korisnik.query.get(id)

    if not korisnik:
        return "Korisnik nije pronađen", 404

    if request.method == 'POST':
        korisnik.ime = request.form['ime']
        korisnik.prezime = request.form['prezime']
        korisnik.email = request.form['email']
        korisnik.datum_upisa = request.form['datum_upisa']
        db.session.commit()
        return redirect(url_for('render_korisnici'))

    return render_template('korisnik-izmena.html', korisnik=korisnik)

@app.route('/korisnik_brisanje/<id>', methods=["POST"])
def korisnik_brisanje(id):
    korisnik = Korisnik.query.get(id)
    db.session.delete(korisnik)
    db.session.commit()
    return redirect(url_for('render_korisnici'))
@app.route('/', methods=['GET'])
def render_login():
    return render_template('login.html')

@app.route('/bibliotekari', methods=['GET'])
def render_bibliotekari():
    bibliotekari = Bibliotekar.query.all()  # Uzmi sve bibliotekare iz baze
    return render_template('bibliotekari.html', bibliotekari=bibliotekari)

@app.route('/bibliotekari_novi', methods=['GET', 'POST'])
def bibliotekari_novi():
    if request.method == 'POST':
        forma = request.form
        novi_bibliotekar = Bibliotekar(
            ime=forma['ime'],
            prezime=forma['prezime'],
            obrazovanje=forma['obrazovanje'],
            radno_iskustvo=forma['radno_iskustvo'],
            email=forma['mail'],
            telefon=forma['telefon']
        )
        db.session.add(novi_bibliotekar)
        db.session.commit()
        return redirect(url_for('render_bibliotekari'))
    
    print(request.form)
    
    return render_template('bibliotekari-novi.html')

@app.route('/bibliotekari_izmena/<int:id>', methods=['GET', 'POST'])
def bibliotekari_izmena(id):
    bibliotekar = Bibliotekar.query.get(id)

    if not bibliotekar:
        return "Bibliotekar nije pronađen", 404

    if request.method == 'POST':
        bibliotekar.ime = request.form['ime']
        bibliotekar.prezime = request.form['prezime']
        bibliotekar.obrazovanje = request.form['obrazovanje']
        bibliotekar.radno_iskustvo = request.form['radno_iskustvo']
        bibliotekar.email = request.form['mail']
        bibliotekar.telefon = request.form['telefon']
        db.session.commit()
        return redirect(url_for('render_bibliotekari'))
    
    print(request.form)

    return render_template('bibliotekari-izmena.html', bibliotekar=bibliotekar)

@app.route('/bibliotekar_brisanje/<int:id>', methods=["POST"])
def bibliotekar_brisanje(id):
    bibliotekar = Bibliotekar.query.get(id)
    if not bibliotekar:
        return "Bibliotekar nije pronađen", 404
    db.session.delete(bibliotekar)
    db.session.commit()
    return redirect(url_for('render_bibliotekari'))


@app.route('/knjige', methods=['GET'])
def render_knjige():
    knjige = Knjiga.query.all()  # Uzmi sve knjige iz baze
    return render_template('knjige.html', knjige=knjige)

@app.route('/knjiga_nova', methods=["GET", "POST"])
def knjiga_nova():
    if request.method == 'POST':
        forma = request.form
        nova_knjiga = Knjiga(
            ime=forma['ime'],
            autor=forma['autor'],
            datum_izdanja=forma['datum_izdanja'],
            stanje=forma['stanje'],
            cena=forma['cena']
        )
        db.session.add(nova_knjiga)
        db.session.commit()
        return redirect(url_for('render_knjige'))
    
    return render_template('knjiga-nova.html')

@app.route('/knjiga_izmena/<int:id>', methods=['GET', 'POST'])
def knjiga_izmena(id):
    knjiga = Knjiga.query.get(id)

    if not knjiga:
        return "Knjiga nije pronađena", 404

    if request.method == 'POST':
        knjiga.ime = request.form['ime']
        knjiga.autor = request.form['autor']
        knjiga.datum_izdanja = request.form['datum_izdanja']
        knjiga.stanje = request.form['stanje']
        knjiga.cena = request.form['cena']
        db.session.commit()
        return redirect(url_for('render_knjige'))

    return render_template('knjiga-izmena.html', knjiga=knjiga)

@app.route('/knjiga_brisanje/<int:id>', methods=["POST"])
def knjiga_brisanje(id):
    knjiga = Knjiga.query.get(id)
    if not knjiga:
        return "Knjiga nije pronađena", 404
    db.session.delete(knjiga)
    db.session.commit()
    return redirect(url_for('render_knjige'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)