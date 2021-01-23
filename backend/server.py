from flask import Flask, request, Response, json
from flask_cors import CORS, cross_origin
import security
import database
import utils
import email_utils

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/status', methods=['GET'])
def status():
    return Response("Server is running!", status=200, mimetype='application/json')


@app.route('/api/users', methods=['POST'])
def create_user():
    db_connection = database.create_database_connection()

    try:
        body = request.get_json()

        if body == None:
            raise Exception('Body is missing.')

        email = utils.get_field(body, 'email')
        password = utils.get_field(body, 'password')
        nickname = utils.get_field(body, 'nickname')

        # Encrypt password
        hashed_password = security.hash_password(password)

        # Insert user into database
        user_id = database.insert_user(
            db_connection, email, hashed_password, nickname)

        #  Generate activation token
        activation_token = utils.generate_activation_token()
        database.insert_activation_token(
            db_connection, user_id, activation_token)

        # Send activation token via email
        email_utils.send_activation_link(email, activation_token)

        return Response('Created.', status=201, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)


@app.route('/api/users/activate/<token>', methods=['GET'])
def activate_user(token):
    db_connection = database.create_database_connection()

    try:
        database.activate_user(db_connection, token)

        return Response('Activated.', status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)


@app.route('/api/login', methods=['POST'])
def login():
    db_connection = database.create_database_connection()

    try:
        body = request.get_json()

        email = utils.get_field(body, 'email')
        password = utils.get_field(body, 'password')

        # Get user's details
        user = database.get_user_by_email(db_connection, email)

        # Check if activated
        if not user['activated']:
            return Response('User is not activated.', status=401, mimetype='application/json')

        # Check password
        if not security.verify_password(user['password'], password):
            return Response('Incorrect password.', status=401, mimetype='application/json')

        # Create jwt token
        data = {
            'id': user['id'],
            'email': user['email'],
            'nickname': user['nickname']
        }

        jwt_token = security.jwt_encode(data)

        data = {
            'token': jwt_token
        }

        return Response(json.dumps(data), status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)


@app.route('/api/locations', methods=['POST'])
def create_location():
    db_connection = database.create_database_connection()

    try:
        user = utils.get_user(request)

        body = request.get_json()

        if body == None:
            raise Exception('Body is missing.')

        name = utils.get_field(body, 'name')
        lat = utils.get_field(body, 'lat')
        lng = utils.get_field(body, 'lng')

        location_id = database.insert_location(
            db_connection, user['id'], name, lat, lng)

        return Response(json.dumps({'id': location_id}), status=201, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)


@app.route('/api/locations', methods=['GET'])
def get_locations():
    db_connection = database.create_database_connection()

    try:
        user = utils.get_user(request)

        res = database.get_locations(db_connection, user['id'])

        return Response(json.dumps(res), status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)


@app.route('/api/locations/<id>', methods=['DELETE'])
def delete_location(id):
    db_connection = database.create_database_connection()

    try:
        user = utils.get_user(request)

        database.delete_location(db_connection, user['id'], id)

        return Response("Deleted.", status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)


@app.route('/api/families', methods=['POST'])
def create_family():
    db_connection = database.create_database_connection()

    try:
        user = utils.get_user(request)

        database.create_family(db_connection, user['id'])

        return Response('Created.', status=201, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)


@app.route('/api/families', methods=['GET'])
def get_family_details():
    db_connection = database.create_database_connection()

    try:
        user = utils.get_user(request)

        res = database.get_family_details(db_connection, user['id'])

        return Response(json.dumps(res), status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)


@app.route('/api/families', methods=['DELETE'])
def delete_family():
    db_connection = database.create_database_connection()

    try:
        user = utils.get_user(request)

        database.delete_family(db_connection, user['id'])

        return Response('Deleted.', status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)


@app.route('/api/families/invitations', methods=['POST'])
def create_family_invitations():
    db_connection = database.create_database_connection()

    try:
        user = utils.get_user(request)
        body = request.get_json()

        if body == None:
            raise Exception('Body is missing.')

        email = utils.get_field(body, 'email')

        # Generate invitation
        invitation_token = utils.generate_activation_token()
        database.create_family_invitation(
            db_connection, user['id'], email, invitation_token)

        # Send invitation
        email_utils.send_family_invitation_link(email, invitation_token)

        return Response('Sent.', status=201, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)


@app.route('/api/families/join/<token>', methods=['GET'])
def join_family(token):
    db_connection = database.create_database_connection()

    try:
        user = utils.get_user(request)

        database.join_family(db_connection, user['id'], token)

        return Response('Ok.', status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)


@app.route('/api/families/leave', methods=['GET'])
def leave_family():
    db_connection = database.create_database_connection()

    try:
        user = utils.get_user(request)

        database.leave_family(db_connection, user['id'])

        return Response('Ok.', status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)


@app.route('/api/exports', methods=['POST'])
def create_export():
    db_connection = database.create_database_connection()

    try:
        user = utils.get_user(request)
        body = request.get_json()

        if body == None:
            raise Exception('Body is missing.')

        email = utils.get_field(body, 'email')

        export_id = database.create_export(db_connection, user['id'], email)

        # Send export
        email_utils.send_export_link(email, export_id)

        return Response('Ok.', status=201, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)


@app.route('/api/exports/<id>', methods=['GET'])
def accept_import(id):
    db_connection = database.create_database_connection()

    try:
        user = utils.get_user(request)

        database.accept_import(db_connection, user['id'], id)

        return Response('Ok.', status=201, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
