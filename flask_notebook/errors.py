from flask import render_template
from flask_notebook import app


@app.errorhandler(404)
@app.errorhandler(403)
@app.errorhandler(405)
def page_not_found(e):
    return render_template('errors/404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html')

