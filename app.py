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
        flash(f'Account was created successfully', 'success')
        return redirect(url_for('home'))

    return render_template('signup.html', title='SignUp', form=form)


@app.route("/login")
def login():
    form = SignInForm()
    return render_template('login.html', title='SignIn', form=form)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)