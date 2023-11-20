from flask_login import UserMixin
from project_app import db, manager
from datetime import datetime



class User(db.Model, UserMixin):
    __tablename__ = "user_login"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True)
    user_passw = db.Column(db.String, nullable=False)
    vardas = db.Column(db.Text)
    pavarde = db.Column(db.Text)
    skyrius = db.Column(db.Text)


    def __init__(self, user_name, user_passw, vardas, pavarde, skyrius):
        self.user_name = user_name
        self.user_passw = user_passw
        self.vardas = vardas
        self.pavarde = pavarde
        self.skyrius = skyrius

    def __repr__(self):
        return f'{self.id} {self.user_name} {self.user_passw} {self.vardas} {self.pavarde} {self.skyrius}'



class Gyventojas(db.Model):
    __tablename__ = 'duomenys1'
    id = db.Column(db.Integer, primary_key=True)
    bylos_id = db.Column(db.TEXT)
    statusas = db.Column(db.TEXT)
    gim_data = db.Column(db.TEXT)
    lytis = db.Column(db.TEXT)
    vpavarde = db.Column(db.TEXT)
    pr_data = db.Column(db.TEXT)
    kas_pristate = db.Column(db.TEXT)
    religija = db.Column(db.TEXT)
    kalba = db.Column(db.TEXT)
    maitinimas = db.Column(db.TEXT)
    kur_isvyko = db.Column(db.TEXT)
    papildomai = db.Column(db.TEXT)
    nuotrauka = db.Column(db.String)

    def __init__(self, bylos_id, statusas, gim_data, lytis, vpavarde, pr_data, kas_pristate, religija, kalba,
                 maitinimas, kur_isvyko, papildomai, nuotrauka):
        self.bylos_id = bylos_id
        self.statusas = statusas
        self.gim_data = gim_data
        self.lytis = lytis
        self.vpavarde = vpavarde
        self.pr_data = pr_data
        self.kas_pristate = kas_pristate
        self.religija = religija
        self.kalba = kalba
        self.maitinimas = maitinimas
        self.kur_isvyko = kur_isvyko
        self.papildomai = papildomai
        self.nuotrauka = nuotrauka

class Salys(db.Model):
    __tablename__ = 'countries'
    salies_pav = db.Column(db.Text(30))
    salies_id = db.Column(db.Text(2), primary_key=True)
    country_name = db.Column(db.Text(30))

    def __init__(self, salies_pav, salies_id, coutry_name):
        self.salies_pav = salies_pav
        self.salies_id = salies_id
        self.country_name = coutry_name


class Sklaida(db.Model):
    __tablename__ = 'sklaidos_info'
    id = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.String(50))
    author = db.Column(db.String(50))
    datos = db.Column(db.DateTime, default=datetime.utcnow)
    tekstas = db.Column(db.Text)

    def __init__(self, tittle, author, tekstas):
        self.tittle = tittle
        self.author = author
        self.tekstas = tekstas




@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
