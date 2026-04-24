from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from app.routes.auth import auth_bp
    from app.routes.articles import articles_bp
    from app.routes.categories import categories_bp
    from app.routes.tags import tags_bp
    from app.routes.upload import upload_bp
    from app.routes.site import site_bp
    from app.routes.account import account_bp
    from app.routes.media import media_bp
    from app.routes.ai import ai_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(articles_bp, url_prefix="/api/articles")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(tags_bp, url_prefix="/api/tags")
    app.register_blueprint(upload_bp, url_prefix="/api/upload")
    app.register_blueprint(site_bp, url_prefix="/api/site")
    app.register_blueprint(account_bp, url_prefix="/api/account")
    app.register_blueprint(media_bp, url_prefix="/api/media")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")

    with app.app_context():
        db.create_all()
        _init_admin(app)

    return app

def _init_admin(app):
    from app.models.user import User
    from config import Config
    if not User.query.first():
        admin = User(username=Config.ADMIN_USERNAME)
        admin.set_password(Config.ADMIN_PASSWORD)
        db.session.add(admin)
        db.session.commit()
