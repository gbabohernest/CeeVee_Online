from CeeVee_Online import create_app, db

app = create_app()


if __name__ == "__main__":
    app.app_context().push()
    db.create_all()
    db.session.commit()
    app.run(debug=True, host='0.0.0.0', port=5001)
