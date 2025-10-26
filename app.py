from flask import request,Flask,render_template,url_for,redirect,flash
from data import User
import time
def check_user(user):
    data=User().check_valid_user(user)
    return True if data else False
def check_password(user,password):
    data=User().check_password(user,password)
    if data: return True
    return False

app=Flask(__name__)
app.secret_key = "secret"
@app.route('/')
def home():
    return (render_template('login.html'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')

        if not user or not password:
            flash("Vui lòng nhập đầy đủ thông tin!")
            return redirect(url_for('home'))

        if check_user(user):
            flash("Tên không hợp lệ hoặc đã được đặt!")
            return redirect(url_for('home'))

        if not check_password(user, password):
            flash("Sai mật khẩu!")
            return redirect(url_for('home'))

        flash(f"Chào mừng trở lại, {user}!")
        return redirect(url_for('index'))

    return redirect(url_for('home'))
@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('firstname')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm-password')

        if not username or not password or not name or not confirm:
            flash("Vui lòng nhập đầy đủ thông tin!")
            return redirect(url_for('register'))

        if password != confirm:
            flash("Xác nhận mật khẩu thất bại")
            return redirect(url_for('register'))

        if check_user(username):
            flash("Tên người dùng đã tồn tại!")
            return redirect(url_for('register'))

        # tạo user mới
        User().create_user(user=username, name=name, password=password)
        flash("Đăng ký thành công! Bạn có thể đăng nhập ngay.")
        time.sleep(2)
        return redirect(url_for('login'))

    return render_template("register.html")


@app.route("/index")
def index():
    return render_template('index.html')


if __name__=='__main__':
    app.run(debug=True)