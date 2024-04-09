from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .demo import GA4RealTimeReport  # Update the import statement

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.route('/analytics')
    def analytics():
        try:
            # Fetch analytics data using GA4RealTimeReport from demo.py
            ga4_realtime = GA4RealTimeReport(property_id='434126696')
            response = ga4_realtime.query_report(['country', 'deviceCategory', 'minutesAgo', 'appVersion'], ['activeUsers'], 10, True)
            headers = response['headers']
            rows = response['rows']
            
            return render_template('analytic.html', headers=headers, rows=rows)
        except Exception as e:
            # Print any error messages to the console for debugging
            print(f"An error occurred: {str(e)}")
            # Render a generic error page or redirect to the home page
            return render_template('error.html', error=str(e))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
