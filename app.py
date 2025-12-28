from flask import render_template, url_for, flash, request, redirect
from datetime import date, datetime # Para enviar fecha y transformar string en fecha y guardarla en sqlite
from flask_login import login_required, login_user, logout_user
from modelos import Usuarios, Clientes, Trabajos
from configs import app, login_manager
from forms import LoginForm, RegisterForm
from modelos import bcrypt, db
from flask_bcrypt import check_password_hash

#Rutas Auth de usuarios
@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for('login'))

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = Usuarios.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('lCli'))
            else:
                flash("Correo o contraseña incorrectos", "danger")
        except Exception as e:
            flash(str(e), "danger")
    return render_template("auth.html", form=form, btn_action="Iniciar Sesión")


@app.route("/logout")

@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#Rutas
@app.route('/clientes')
@login_required
def lCli():
    lsCli = db.session.execute(db.select(Clientes).order_by(Clientes.nombre)).scalars().all()
    return render_template('clientes.html', clis = lsCli)

@app.route('/ecli', methods=['POST'])
@login_required
def ecli():
    cl = Clientes.query.filter_by(id=request.form['cliId']).first()
    cl.nombre = request.form['nombre']
    cl.tel = request.form['tel']
    cl.dom = request.form['dom']
    db.session.commit()
    return redirect(url_for('lCli'))

@app.route('/ncli', methods=['POST'])
@login_required
def ncli():        
    nclient = Clientes(nombre=request.form['nombre'], tel=request.form['tel'], dom=request.form['dom'])
    db.session.add(nclient)
    db.session.commit()
    return redirect(url_for('lCli'))

@app.route('/trabajos', methods=['GET','POST'])
@login_required
def trabajos():
    if request.method == 'GET':
        hoy = date.today()
        lsTrabajos = db.session.query(Trabajos, Clientes).join(Clientes, Clientes.id == Trabajos.id_cli).order_by(Trabajos.id.desc()).all() # envío join y en el for levato las 2 entidades por separado
        lsCli = Clientes.query.with_entities(Clientes.id, Clientes.nombre).order_by(Clientes.nombre).all()
        return render_template('trabajos.html', trabajos = lsTrabajos, clientes = lsCli, hoy = hoy)
    if request.method == 'POST':
        nuevo_trabajo = Trabajos(id_cli=request.form['id_cli'], fecha=datetime.strptime(request.form['fecha'], '%Y-%m-%d').date(), tarea=request.form['tarea'], total=request.form['total'])
        db.session.add(nuevo_trabajo)
        db.session.commit()
        return redirect(url_for('trabajos'))

@app.route('/trabajos/<int:id>', methods=['POST','GET'])
@login_required
def dtrabajo(id):
    if request.method == 'POST':
        trabajo = db.session.get(Trabajos, id)
        db.session.delete(trabajo)
        db.session.commit()
        return redirect(url_for('trabajos'))
    if request.method == 'GET':
        hoy = date.today()
        lsTrabajos = db.session.query(Trabajos, Clientes).join(Clientes, Clientes.id == Trabajos.id_cli).where(Trabajos.id_cli == id).order_by(Trabajos.id.desc()).all() # envío join y en el for levato las 2 entidades por separado
        lsCli = Clientes.query.with_entities(Clientes.id, Clientes.nombre).order_by(Clientes.nombre).all()
        return render_template('trabajos.html', trabajos = lsTrabajos, clientes = lsCli, hoy = hoy)

@app.route('/etrabajo', methods=['POST'])
@login_required
def etrabajo():
    tr = Trabajos.query.filter_by(id=request.form['id']).first()
    tr.sol = request.form['sol']
    tr.total = request.form['total']
    db.session.commit()
    return redirect(url_for('trabajos'))

#Ejecuto la app en servidor interno
if __name__ == '__main__':
    app.run(port=5000, debug=True)