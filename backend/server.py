from flask import Flask, request, Response, json
import security
import database
import utils
import email_utils

app = Flask(__name__)


@app.route('/status', methods=['GET'])
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

        database.insert_location(db_connection, user['id'], name, lat, lng)

        return Response('Created.', status=201, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=400, mimetype='application/json')
    finally:
        database.close_connection(db_connection)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
