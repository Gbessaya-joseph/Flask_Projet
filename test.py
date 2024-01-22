from flask import Flask, url_for

app = Flask(__name__)

@app.route('/appointments/')
def appointment_list():
    return 'Liste de tous les rendez-vous que nous avons.'

@app.route('/appointments/<int:appointment_id>/')
def appointment_detail(appointment_id):
    return 'Détail du rendez-vous #{}.'.format(appointment_id)

@app.route('/appointments/<int:appointment_id>/edit/', methods=['GET', 'POST'])
def appointment_edit(appointment_id):
    return 'Formulaire pour éditer le rendez-vous #{}.'.format(appointment_id)

@app.route('/appointments/create/', methods=['GET', 'POST'])
def appointment_create():
    return 'Formulaire pour créer un nouveau rendez-vous.'

@app.route('/appointments/<int:appointment_id>/delete/', methods=['DELETE'])
def appointment_delete(appointment_id):
    raise NotImplementedError('DELETE')

# Démonstration de l'utilisation de url_for
@app.route('/appointments/<int:appointment_id>/')
def appointment_detail_with_url(appointment_id):
    edit_url = url_for('appointment_edit', appointment_id=appointment_id)
    # Retourne la chaîne URL simplement pour la démonstration.
    return f'Détail du rendez-vous #{appointment_id}. URL d\'édition : {edit_url}'

if __name__ == '__main__':
    app.run(debug=True)
