from flask import Flask, render_template, request, redirect, url_for, session
import pyotp
import qrcode
import io
import base64
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "clave_secreta"  # 🔹 Clave de seguridad para sesiones

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Base de datos simulada
users = {"admin": {"password": "1234", "secret": None}}

# Modelo de usuario para Flask-Login
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

# Formulario de inicio de sesión
class LoginForm(FlaskForm):
    username = StringField("Usuario")
    password = PasswordField("Contraseña")
    submit = SubmitField("Iniciar sesión")

# Formulario de autenticación 2FA
class OTPForm(FlaskForm):
    otp = StringField("Código de autenticación")
    submit = SubmitField("Verificar")

@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username in users and users[username]["password"] == password:
            session["username"] = username
            if users[username]["secret"] is None:
                return redirect(url_for("setup_2fa"))
            return redirect(url_for("verify_otp"))

    return render_template("login.html", form=form)

@app.route("/setup_2fa")
def setup_2fa():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    secret = pyotp.random_base32()
    users[username]["secret"] = secret
    totp = pyotp.TOTP(secret)
    qr_url = totp.provisioning_uri(name=username, issuer_name="TuApp")

    # Generar código QR
    qr = qrcode.make(qr_url)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_b64 = base64.b64encode(buffer.getvalue()).decode()

    return render_template("setup_2fa.html", qr_code=qr_b64, secret=secret)

@app.route("/verify_otp", methods=["GET", "POST"])
def verify_otp():
    if "username" not in session:
        return redirect(url_for("login"))

    form = OTPForm()
    if form.validate_on_submit():
        username = session["username"]
        user_secret = users[username]["secret"]
        totp = pyotp.TOTP(user_secret)

        if totp.verify(form.otp.data):
            login_user(User(username))
            return redirect(url_for("dashboard"))

    return render_template("verify_otp.html", form=form)

@app.route("/dashboard")
@login_required
def dashboard():
    return f"Bienvenido {current_user.id}! <a href='/logout'>Cerrar sesión</a>"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
