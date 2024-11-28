from __init__ import create_app, db

def run():
    app = create_app('DevelopmentConfig')

    with app.app_context():
        #db.drop_all()
        db.create_all()

    return app

if __name__ == '__main__':
    app = run()
    app.run(debug=True)
