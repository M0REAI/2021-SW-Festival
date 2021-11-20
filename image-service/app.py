from flask import Flask, jsonify
from  flask_cors import CORS
 
class App:
    app = Flask(__name__)
    CORS(app, expose_headers=["Content-Disposition"])
    def __init__(self,views):
        # self.initialize_config()
        self.initialize_views(views)

    # https://flask.palletsprojects.com/en/2.0.x/errorhandling/ 
    # at the application level
    # not the blueprint level
    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404 

    @app.errorhandler(403)
    def resource_not_found(e):
        return jsonify(error=str(e)), 403 
    
    @app.errorhandler(400)
    def resource_not_found(e):
        return jsonify(error=str(e)), 400
        
    # def initialize_config(self):
        # https://stackoverflow.com/questions/41543951/how-to-change-downloading-name-in-flask
        # CORS(self.app, expose_headers=["Content-Disposition"])
    
    def initialize_views(self,views):
        for view in views:
            self.app.register_blueprint(view.router)
        
    def run(self):
        self.app.run(host='0.0.0.0', port='5000', debug=True)

    





    