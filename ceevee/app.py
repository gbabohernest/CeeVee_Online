from flask import render_template, url_for, flash, redirect, request
from ceevee import create_app
from ceevee.config import Config

app = create_app(config_class=Config)

@app.route("/signup", methods=['GET', 'POST', 'PUT', 'DELETE'])
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

if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0', debug=True)
