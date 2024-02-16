<<<<<<< HEAD
from CeeVee_Online import create_app, db, bcrypt
from CeeVee_Online.users.forms import User, Role
app = create_app()
=======
from flask import Flask, render_template, url_for, flash, redirect
from forms import SignUpForm, SignInForm

app = Flask(__name__)

# SECRET_KEY
app.config['SECRET_KEY'] = 'dev'


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/categories")
def categories():
    return render_template('categories.html', title='Categories')


@app.route("/signup", methods=('GET', 'POST'))
def sign_up():
    """Signup view function. Handles signup form validations
    Return: signup view
    """
    form = SignUpForm()

    if form.validate_on_submit():
        # checks if all fields are validated when submitted
        flash(f'Account Created, Success!!', 'success')
        return redirect(url_for('home'))

    return render_template('signup.html', title='SignUp', form=form)


@app.route("/login", methods=('GET', 'POST'))
def login():
    form = SignInForm()

    # checks if all fields are validated when submitted
    if form.validate_on_submit():
        """Temp data to stimulate login success, change later with actual data from db
         """
        if form.email.data == 'admin@fake.com' and form.password.data == '123456':
            flash(f'Logged In successfully!!', 'success')
            return redirect(url_for('home'))

        else:
            flash(f'Login failed, check credentials', 'danger')
    return render_template('login.html', title='SignIn', form=form)
>>>>>>> cfe74432dc7e2187812755b98c673b4b5df693f4


if __name__ == "__main__":
    # db.create_all()
    # db.session.commit()
    app.app_context().push()
    db.session.commit()
    app.run(debug=True, host='0.0.0.0', port=5000)
