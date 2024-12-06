from flask import Flask

mastication = {"status": None,
               "count": 0}

def create_app():    
    app = Flask(__name__) 
           
    app.config['mastication'] = mastication

    from apps.display import views as display_views
    app.register_blueprint(display_views.display, url_prefix="/display")    
    
    from apps.sound import views as sound_views
    app.register_blueprint(sound_views.sound, url_prefix="/sound")

    from apps.processing import views as processing_views
    app.register_blueprint(processing_views.processing, url_prefix="/processing")
    
    return app