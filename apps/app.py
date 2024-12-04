from flask import Flask

def create_app():    
    app = Flask(__name__)

    from apps.display import views as display_views
    app.register_blueprint(display_views.display, url_prefix="/display")    
    
    from apps.sound import views as sound_views
    app.register_blueprint(sound_views.sound, url_prefix="/sound")    
    
    return app