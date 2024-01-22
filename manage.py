from flask import Flask
from flask.cli import FlaskGroup
from sched.app import app

#app = Flask(__name__)
cli = FlaskGroup(app)

@cli.command("runserver")
def runserver():
    """Run the development server."""
    app.run(debug=True)

if __name__ == '__main__':
    cli()
