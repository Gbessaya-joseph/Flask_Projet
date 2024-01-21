from flask import Flask
from flask import Flask, url_for
from flask import abort, jsonify, redirect, render_template, request, url_for 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import OperationalError
from urllib.parse import quote_plus
from models import Base
from forms import AppointmentForm
from models import Appointment
import config




app = Flask(__name__)
utilisateur = 'root'
mot_de_passe = 'Joseph@MySQL'
hote = 'localhost'
nom_de_la_base = 'sheds'

mot_de_passe_encode = quote_plus(mot_de_passe)



#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/lawson/Documents/Projet_Flask/sched/sched.db'
#engine = create_engine(f'mysql://{utilisateur}:{mot_de_passe_encode}@{hote}/{nom_de_la_base}')

#try:
#   engine = create_engine('mysql://root:Joseph@MySQL@localhost/sheds')
#except OperationalError as e:
#    print(f"Erreur lors de la connexion à la base de données : {e}")
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{utilisateur}:{mot_de_passe_encode}@{hote}/{nom_de_la_base}"
#app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://root:Joseph@MySQL@localhost/sheds" #'mysql://root:@localhost/sheds'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress a warning message
#db = SQLAlchemy()
#metadata = MetaData()
db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base.metadata.create_all(engine)
db.Model = Base

#app.config.from_object(config)


# Use Flask-SQLAlchemy for its engine and session
# configuration. Load the extension, giving it the app object,
# and override its default Model class with the pure
# SQLAlchemy declarative Base class.



@app.route('/appointments/')
def appointment_list():
  """Provide HTML listing of all appointments."""
  # Query: Get all Appointment objects, sorted by date.
  appts = (db.session.query(Appointment)
    .order_by(Appointment.start.asc()).all())
  return render_template('index.html', appts=appts)


@app.route('/appointments/<int:appointment_id>/')
def appointment_detail(appointment_id):
    """Fournir une page HTML avec un rendez-vous donné."""
    # Requête : obtenir l'objet Appointment par ID.
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        # Abandonner avec "Non trouvé".
        abort(404)
    return render_template('appointment/detail.html', appt=appt)


@app.route('/appointments/<int:appointment_id>/edit/', methods=['GET', 'POST'])
def appointment_edit(appointment_id):
    """Provide HTML form to edit a given appointment."""
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        abort(404)
    form = AppointmentForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        # Success. Send the user back to the detail view.
        return redirect(url_for('appointment_detail', appointment_id=appt.id))
    return render_template('appointment/edit.html', form=form)


@app.route('/appointments/create/', methods=['GET', 'POST'])
def appointment_create():
  """Provide HTML form to create a new appointment."""
  form = AppointmentForm(request.form)
  if request.method == 'POST' and form.validate():
    appt = Appointment()
    form.populate_obj(appt)
    db.session.add(appt)
    db.session.commit()
    # Success. Send user back to full appointment list.
    return redirect(url_for('appointment_list'))
  # Either first load or validation error at this point.
  return render_template('appointment/edit.html', form=form)




@app.route(
  '/appointments/<int:appointment_id>/delete/',
  methods=['DELETE'])
def appointment_delete(appointment_id):
  """Delete record using HTTP DELETE, respond with JSON."""
  appt = db.session.query(Appointment).get(appointment_id)
  if appt is None:
    # Abort with Not Found, but with simple JSON response.
    response = jsonify({'status': 'Not Found'})
    response.status = 404
    return response
  db.session.delete(appt)
  db.session.commit()
  return jsonify({'status': 'OK'})






@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  with app.app_context():
     db.create_all()
  app.run(debug=True)
