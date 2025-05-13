from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
import os

# 初始化扩展
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()

def create_app(test_config=None):
    # 创建并配置应用
    app = Flask(__name__, instance_relative_config=True)
    
    # 配置数据库和安全密钥
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(app.instance_path, "medquality.db")}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # 非测试环境下加载实例配置
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 测试环境下加载传入的配置
        app.config.from_mapping(test_config)

    # 确保实例文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    csrf.init_app(app)
    migrate.init_app(app, db)

    # 注册蓝图
    from app.controllers.auth import auth_bp
    from app.controllers.dashboard import dashboard_bp
    from app.controllers.indicators import indicators_bp
    from app.controllers.reports import reports_bp
    from app.controllers.api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(indicators_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(api_bp)

    # 注册一个简单的首页路由
    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))

    # 添加错误处理页面
    from app.controllers import errors
    app.register_error_handler(404, errors.page_not_found)
    app.register_error_handler(500, errors.internal_server_error)

    # 初始化命令
    from app.commands import init_db_command
    app.cli.add_command(init_db_command)

    return app 