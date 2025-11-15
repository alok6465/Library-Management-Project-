from flask import Flask
from config import Config
from app.extensions import db, migrate, login

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'auth.student_login'
    login.login_message = 'Please log in to access this page.'
    login.login_message_category = 'info'
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.models import User
    
    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app