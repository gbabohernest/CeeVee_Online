from CeeVee_Online import create_app, db, bcrypt
from CeeVee_Online.users.forms import User, Role
app = create_app()


if __name__ == "__main__":
    # db.create_all()
    # db.session.commit()
    app.app_context().push()
    db.session.commit()
    app.run(debug=True, host='0.0.0.0', port=5001)
