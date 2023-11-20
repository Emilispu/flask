from datetime import datetime
from project_app import app, db
from flask import render_template, request, redirect, flash, url_for, send_from_directory, send_file, current_app, session
from project_app.models import Gyventojas, Salys, Sklaida, User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user
import os
import matplotlib.pyplot as plt
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from docx import Document
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image
from io import BytesIO


def check_admin_status():
    # Assuming 'is_admin' is a key that holds the admin status in the session
    return session.get('is_admin', False)
def get_info_about_incoming():
    start = 1997
    finisas = 2024
    metai = range(start, finisas)
    incoming_date_male = []
    incoming_date_female = []
    incoming_date = []

    for year in metai:
        how_many_pro_year_male = Gyventojas.query.filter(Gyventojas.pr_data.startswith(str(year)),
                                                         Gyventojas.lytis.startswith('Vyr')).count()
        how_many_pro_year_female = Gyventojas.query.filter(Gyventojas.pr_data.startswith(str(year)),
                                                           Gyventojas.lytis.startswith('Mot')).count()
        how_many_pro_year = Gyventojas.query.filter(Gyventojas.pr_data.startswith(str(year))).count()
        incoming_date_male.append(how_many_pro_year_male)
        incoming_date_female.append(how_many_pro_year_female)
        incoming_date.append(how_many_pro_year)
    return metai, incoming_date_male, incoming_date_female, incoming_date

def get_info_by_month():
    incoming_date_by_month = []
    menuo = range(1, 12)
    for el in menuo:
        el = '2023-'+str(el).zfill(2)
        how_many_this_year = Gyventojas.query.filter(Gyventojas.pr_data.startswith(el)).count()
        incoming_date_by_month.append(how_many_this_year)
    return menuo, incoming_date_by_month

def get_info_by_month_mw():
    incoming_date_by_month_male = []
    incoming_date_by_month_female = []
    menuo = range(1, 12)
    for el in menuo:
        el = '2023-'+str(el).zfill(2)
        how_many_this_year_m = Gyventojas.query.filter(Gyventojas.pr_data.startswith(el), Gyventojas.lytis.startswith('Vyras')).count()
        incoming_date_by_month_male.append(how_many_this_year_m)
        how_many_this_year_w = Gyventojas.query.filter(Gyventojas.pr_data.startswith(el), Gyventojas.lytis.startswith('Moteris')).count()
        incoming_date_by_month_female.append(how_many_this_year_w)
    return menuo, incoming_date_by_month_male, incoming_date_by_month_female

def draw_line():
    metai, incoming_date_male, incoming_date_female, incoming_date = get_info_about_incoming()
    plt.figure(figsize=(8, 6))
    plt.plot(metai, incoming_date, marker='o', linestyle='-', label='Viso', color='black')
    plt.title('Apgyvendinimo statistika pagal metus')
    plt.xlabel('Metai')
    plt.ylabel('Užsieneičių skaičius')

    for i, j in zip(metai, incoming_date):
        plt.annotate(f'{j}', (i, j), textcoords="offset points", xytext=(0, 10), ha='center')

    info_apie_uzsieniecius0 = f'Viso (juoda)'
    plt.figtext(0.3, 0.01, info_apie_uzsieniecius0, fontsize=10, ha='left', color='black')

    grafikas_filepath = 'project_app/uploads/grafikas.png'
    plt.savefig(grafikas_filepath)

    return grafikas_filepath

def draw_line_by_month():
    menuo, incoming_date_by_month = get_info_by_month()
    plt.figure(figsize=(8, 6))
    plt.plot(menuo, incoming_date_by_month, marker='o', linestyle='-', label='Viso', color='black')
    plt.title('Šių metų apgyvendinimo statistika pagal mėnesius')
    plt.xlabel('Mėnuo')
    plt.ylabel('Užsieneičių skaičius')

    for i, j in zip(menuo, incoming_date_by_month):
        plt.annotate(f'{j}', (i, j), textcoords="offset points", xytext=(0, 10), ha='center')

    info_apie_uzsieniecius0 = f'Viso (juoda)'
    plt.figtext(0.3, 0.01, info_apie_uzsieniecius0, fontsize=10, ha='left', color='black')

    grafikas_filepath3 = 'project_app/uploads/grafikas2.png'
    plt.savefig(grafikas_filepath3)

    return grafikas_filepath3

def draw_line_by_month_fm():
    menuo, incoming_date_by_month_male, incoming_date_by_month_female = get_info_by_month_mw()
    plt.figure(figsize=(8, 6))
    plt.plot(menuo, incoming_date_by_month_male, marker='o', linestyle='-', label='Vyrai', color='blue')
    plt.plot(menuo, incoming_date_by_month_female, marker='o', linestyle='-', label='Moterys', color='red')
    plt.title('Šių metų apgyvendinimo statistika pagal mėnesius ir lytis')
    plt.xlabel('Mėnuo')
    plt.ylabel('Užsieneičių skaičius')

    for i, j in zip(menuo, incoming_date_by_month_male):
        plt.annotate(f'{j}', (i, j), textcoords="offset points", xytext=(0, 10), ha='center')
    for i, j in zip(menuo, incoming_date_by_month_female):
        plt.annotate(f'{j}', (i, j), textcoords="offset points", xytext=(0, 10), ha='center')

    info_apie_uzsieniecius1 = f'Vyrai (mėlyna)'
    plt.figtext(0.5, 0.01, info_apie_uzsieniecius1, fontsize=10, ha='center', color='blue')
    info_apie_uzsieniecius2 = f'Moterys (raudona)'
    plt.figtext(0.6, 0.01, info_apie_uzsieniecius2, fontsize=10, ha='left', color='red')

    grafikas_filepath4 = 'project_app/uploads/grafikas3.png'
    plt.savefig(grafikas_filepath4)

    return grafikas_filepath4

def draw_line_by_lytis():
    metai, incoming_date_male, incoming_date_female, incoming_date = get_info_about_incoming()

    plt.figure(figsize=(8, 6))
    plt.plot(metai, incoming_date_male, marker='o', linestyle='-', label='Vyrai', color='blue')
    plt.plot(metai, incoming_date_female, marker='o', linestyle='-', label='Moterys', color='red')
    plt.title('Apgyvendinimo statistika pagal metus ir lytis')
    plt.xlabel('Metai')
    plt.ylabel('Užsieneičių skaičius')

    for i, j in zip(metai, incoming_date_male):
        plt.annotate(f'{j}', (i, j), textcoords="offset points", xytext=(0, 10), ha='center')
    for i, j in zip(metai, incoming_date_female):
        plt.annotate(f'{j}', (i, j), textcoords="offset points", xytext=(0, 10), ha='center')

    info_apie_uzsieniecius1 = f'Vyrai (mėlyna)'
    plt.figtext(0.5, 0.01, info_apie_uzsieniecius1, fontsize=10, ha='center', color='blue')
    info_apie_uzsieniecius2 = f'Moterys (raudona)'
    plt.figtext(0.6, 0.01, info_apie_uzsieniecius2, fontsize=10, ha='left', color='red')

    grafikas_filepath1 = 'project_app/uploads/grafikas1.png'
    plt.savefig(grafikas_filepath1)

    return grafikas_filepath1

def generate_pdf(doc):
    pdf_filename = "id_card.pdf"
    doc.save(pdf_filename)
    return pdf_filename

@app.route('/about')
def vizualizacija():
    grafikas = draw_line()
    grafikas_lytis = draw_line_by_lytis()
    grafikas_menuo = draw_line_by_month()
    grafikas_menuo_wm = draw_line_by_month_fm()
    return render_template('public/about.html', grafikas=grafikas, grafikas_lytis=grafikas_lytis, grafikas_menuo=grafikas_menuo, grafikas_menuo_wm=grafikas_menuo_wm)


@app.route("/")
@login_required
def index():
    files = Gyventojas.query.all()
    full_articles = Sklaida.query.order_by(Sklaida.datos.desc()).all()
    return render_template("public/index.html", full_articles=full_articles)


@app.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/duomenys", methods=['GET', 'POST'])
@login_required
def duomenys():
    if request.method == "POST":
        bylos_id1 = request.form['bylos_id']
        statusas1 = request.form['pasirinkimas']
        gim_data1 = request.form['birdday']
        lytis1 = request.form['pasirinkimas2']
        vpavarde1 = request.form['vpavarde']
        pr_data1 = request.form['income']
        kas_pristate1 = request.form['is_kur']
        religija1 = request.form['religija']
        kalba1 = request.form['kalba']
        maitinimas1 = request.form['pasirinkimas3']
        kur_isvyko1 = request.form['isvyko']
        papildomai1 = request.form['tekstas']
        filename = None
        if 'nuotrauka' in request.files:

            file = request.files['nuotrauka']
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if len(bylos_id1) >= 7:
            flash('Duomenys išsaugoti', category='success')
        else:
            flash('Išsaugoti nepavyko', category='error')

        naujas_irasas = Gyventojas(bylos_id=bylos_id1, statusas=statusas1, gim_data=gim_data1, lytis=lytis1,
                                   vpavarde=vpavarde1, pr_data=pr_data1, kas_pristate=kas_pristate1, religija=religija1,
                                   kalba=kalba1, maitinimas=maitinimas1, kur_isvyko=kur_isvyko1, papildomai=papildomai1,
                                   nuotrauka=filename)
        db.session.add(naujas_irasas)
        db.session.commit()

    return render_template("admin/duomenys.html")


@app.route("/ataskaitos")
def ataskaitos():
    return render_template("public/ataskaitos.html")


@app.route("/last_id")
def last_id():
    return render_template("last_id.html")


@app.route("/land_code", methods=['GET', 'POST'])
def land_code():
    listas = []
    sarasas = Salys.query.all()
    sarasas1 = Gyventojas.query.all()
    for el in sarasas:
        a = el.salies_id
        b = a + '00000'
        for x in sarasas1:
            c = x.bylos_id[:7]
            if c.startswith(a) and (c > b):
                b = c
            else:
                continue
        listas.append((el.salies_pav, el.salies_id, b, el.country_name))

    return render_template("public/land_code.html", sarasas=listas)


@app.route("/info_all", methods=['GET', 'POST'])
def info_all():
    who = []
    sarasas = Salys.query.all()
    # atrenkame kiek yra gyventojų pagal šalis
    for el in sarasas:
        x = Gyventojas.query.filter(Gyventojas.bylos_id.like(f'{el.salies_id}%'), Gyventojas.statusas == "Aktyvi").all()
        if x:
            who.append([el.salies_pav, len(x)])
    who = sorted(who, key=lambda y: y[1], reverse=True)
    a = 0
    b = len(who) // 2
    for el in who:
        a += int(el[1])
    # atrenkame kiek yra gyventojų pagal lytis ir šeimas
    seima = Gyventojas.query.filter(Gyventojas.bylos_id.endswith('_1'), Gyventojas.statusas.like('Aktyvi')).count()
    viso = Gyventojas.query.filter(Gyventojas.statusas.like('Aktyvi')).count()
    vyras = Gyventojas.query.filter(Gyventojas.lytis.like('Vyras'), Gyventojas.statusas.like('Aktyvi')).count()
    moteris = Gyventojas.query.filter(Gyventojas.lytis.like('Moteris'), Gyventojas.statusas.like('Aktyvi')).count()
    x = str(int(Gyventojas.query.filter(Gyventojas.statusas.like('Aktyvi')).count()/5))
    y = str(int(Gyventojas.query.filter(Gyventojas.lytis.like('Vyras'), Gyventojas.statusas.like('Aktyvi')).count()/Gyventojas.query.filter(Gyventojas.statusas.like('Aktyvi')).count()*100))
    z = str(100-int(y))
    print(y, z)
    return render_template("public/info_all.html", who=who, a=a, b=b, seima=seima, vyras=vyras, moteris=moteris, viso=viso, x=x, y=y, z=z)


@app.route("/detained_persons")
def detained_persons():
    return render_template("detained_persons.html")


@app.route("/alt_teritory")
def alt_teritory():
    return render_template("alt_teritory.html")


@app.route("/free_to_go")
def free_to_go():
    return render_template("free_to_go.html")


@app.route("/statistika")
def statistika():
    return render_template("statistika.html")


@app.route("/id_korteles")
def id_korteles():
    return render_template("id_korteles.html")


@app.route("/pazymos")
def pazymos():
    return render_template("pazymos.html")


@app.route('/details/<string:bylos_id>')
def details(bylos_id):
    gyventojas = Gyventojas.query.filter_by(bylos_id=bylos_id).first()
    return render_template('public/rezultatas_id.html', gyventojas=gyventojas)

@app.route('/id_info', methods=['GET', 'POST'])
def id_info():
    bylos_id =request.form.get('zodis')
    gyventojas = Gyventojas.query.filter_by(bylos_id=bylos_id).first()
    return render_template('public/id_info.html', gyventojas=gyventojas)

@app.errorhandler(404)
def klaida_404(klaida):
    return render_template('public/404page.html'), 404


@app.route("/rezultatas", methods=['GET', 'POST'])
def paieska():
    zodis = request.form.get('zodis')
    rezultatai = Gyventojas.query.filter(
        (Gyventojas.bylos_id.like(f"""%{zodis}%""")) |
        (Gyventojas.statusas.like(f'%{zodis}%')) |
        (Gyventojas.gim_data.like(f'%{zodis}%')) |
        (Gyventojas.lytis.like(f'%{zodis}%')) |
        (Gyventojas.vpavarde.like(f'%{zodis}%')) |
        (Gyventojas.pr_data.like(f'%{zodis}%')) |
        (Gyventojas.kas_pristate.like(f'%{zodis}%')) |
        (Gyventojas.religija.like(f'%{zodis}%')) |
        (Gyventojas.kalba.like(f'%{zodis}%')) |
        (Gyventojas.maitinimas.like(f'%{zodis}%')) |
        (Gyventojas.kur_isvyko.like(f'%{zodis}%')) |
        (Gyventojas.papildomai.like(f'%{zodis}%')) |
        (Gyventojas.nuotrauka.like(f'%{zodis}%'))
    ).all()
    kiekis = len(rezultatai)
    return render_template("public/rezultatas.html", rezultatai=rezultatai, zodis=zodis, kiekis=kiekis)


@app.route("/add_article", methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        tittle = request.form['tittle']
        author = request.form['author']
        tekstas = request.form['tekstas']

        articles = Sklaida(tittle=tittle, author=author, tekstas=tekstas)
        try:
            db.session.add(articles)
            db.session.commit()
            return redirect('/')
        except:
            return 'Klaida keliant'
    else:
        return render_template("public/add_article.html")


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    passw = request.form.get('password')

    if login and passw:
        user = User.query.filter_by(user_name=login).first()

        if user and check_password_hash(user.user_passw, passw):
            login_user(user)

            next_page = request.args.get('next')
            redirect(next_page)

        else:
            flash("Duomenys suvesti neteisingai")
    else:
        flash('Prašome užpildyti prisijungimo vardą ir slaptažodžio duomenis')

    return render_template('public/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    login1 = request.form.get('login')
    passw1 = request.form.get('password')
    passw2 = request.form.get('password2')
    vardas1 = request.form.get('vardas')
    pavarde1 = request.form.get('pavarde')
    skyrius1 = request.form.get('skyrius')
    if request.method == 'POST':
        if not (login1 or passw1 or passw2):
            flash('Prašome užpildyti visus laukus')
        elif passw1 != passw2:
            flash('Slaptažodžiai nesutampa')
        else:
            hash_pwd = generate_password_hash(passw1)
            new_user = User(user_name=login1, user_passw=hash_pwd, vardas=vardas1, pavarde=pavarde1, skyrius=skyrius1)
            db.session.add(new_user)
            db.session.commit()
            flash('Vartotojas užregistruotas')
            return redirect(url_for('register_page'))
    return render_template("admin/register.html")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_signit(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response


@app.route('/id_card', methods=['GET', 'POST'])
def id_card():
    if request.method == 'POST':
        doc = DocxTemplate('project_app/uploads/card_id.docx')
        bylos_id =request.form.get('bylos_id')
        nuotrauka2 = Code128(request.form.get('bylos_id'), writer=ImageWriter())
        nuotrauka2.save("project_app/uploads/id_code")
        sarasas = Gyventojas.query.filter_by(bylos_id=bylos_id).first()
        vpavarde = sarasas.vpavarde
        gim_data = sarasas.gim_data
        maitinimas = sarasas.maitinimas


        if request.form['pasirinkimas'] == '1':
            pasirinkimas = InlineImage(doc, f"project_app/uploads/1.jpg")
        elif request.form['pasirinkimas'] == '2':
            pasirinkimas = InlineImage(doc, f"project_app/uploads/2.jpg")
        else:
            pasirinkimas = InlineImage(doc, f"project_app/uploads/3.jpg")


        if sarasas.nuotrauka:
            context = {'bylos_id': f'{bylos_id}', 'vpavarde': f'{vpavarde}', 'maitinimas': f'{maitinimas}', 'gim_data': f'{gim_data}',
                       'pasirinkimas': pasirinkimas, 'nuotrauka': InlineImage(doc, f"project_app/uploads/{sarasas.nuotrauka}", width=Mm(40)), 'nuotrauka1': InlineImage(doc, f"project_app/uploads/id_code.png", width=Mm(70))}
        elif sarasas.lytis == 'Vyras':
            context = {'bylos_id': f'{bylos_id}', 'vpavarde': f'{vpavarde}', 'gim_data': f'{gim_data}',
                       'pasirinkimas': pasirinkimas, 'maitinimas': f'{maitinimas}', 'nuotrauka': InlineImage(doc, f"project_app/uploads/male.jpg", width=Mm(40)), 'nuotrauka1': InlineImage(doc, f"project_app/uploads/id_code.jpg", width=Mm(70))}
        else:
            context = {'bylos_id': f'{bylos_id}', 'vpavarde': f'{vpavarde}', 'gim_data': f'{gim_data}',
                       'pasirinkimas': pasirinkimas, 'maitinimas': f'{maitinimas}', 'nuotrauka': InlineImage(doc, f"project_app/uploads/female.jpg", width=Mm(40)), 'nuotrauka1': InlineImage(doc, f"project_app/uploads/id_code.jpg", width=Mm(70))}

        doc.render(context)
        doc.save('project_app/uploads/aaa.docx')
        file_path = current_app.root_path + '/uploads/aaa.docx'
        return send_file(file_path, as_attachment=False)

    is_admin = check_admin_status()  # Define a function to check admin status

    if is_admin:
        return render_template('admin/card_id.html')
    else:
        return render_template('public/card_id.html')


@app.route('/pazyma', methods=['GET', 'POST'])
def pazyma():
    if request.method == 'POST':
        doc1 = DocxTemplate('project_app/uploads/pazyma.docx')
        bylos_id =request.form.get('bylos_id')
        sarasas2 = Gyventojas.query.filter_by(bylos_id=bylos_id).first()
        vpavarde = sarasas2.vpavarde
        gim_data = sarasas2.gim_data
        pr_data = sarasas2.pr_data
        kam = request.form.get('kam')

        context2 = {'bylos_id': f'{bylos_id}', 'vpavarde': f'{vpavarde}', 'gim_data': f'{gim_data}',
                       'pr_data': pr_data, 'data': str(datetime.now().strftime('%Y-%m-%d')), 'kam': kam}

        doc1.render(context2)
        doc1.save('project_app/uploads/pazyma_id.docx')
        file_path = current_app.root_path + '/uploads/pazyma_id.docx'
        return send_file(file_path, as_attachment=False)

    return render_template('public/pazyma.html')
