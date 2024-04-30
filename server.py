from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.books import Books
from forms.user import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.login import LoginForm
from forms.search import SearchForm
from data.parser import search
from data.player import play

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/history')
@login_required
def history():
    db_sess = db_session.create_session()
    books = db_sess.query(Books).filter(Books.user == current_user)
    return render_template('history.html', books=books)


@app.route('/book/<book>', methods=['GET', 'POST'])
def show_book(book):
    return render_template(f'{book}.html')


@app.route("/", methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    srch = SearchForm()
    if srch.validate_on_submit():
        search_msg = srch.name.data
        files = search(search_msg)
        play(files, search_msg)

        flag = True
        for bk in db_sess.query(Books).filter(Books.user == current_user):
            if bk.title == search_msg:
                flag = False

        if flag:
            bk = Books()
            bk.title = search_msg
            bk.user_id = int(current_user.id)
            db_sess.add(bk)
            db_sess.commit()

        return redirect(f'/book/{search_msg}')
    return render_template("index.html", form=srch)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/blogs.db")

    app.run()


if __name__ == '__main__':
    main()
