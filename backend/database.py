import psycopg2
from get_docker_secret import get_docker_secret
import os


def create_database_connection():
    connection = psycopg2.connect(user=get_docker_secret(os.environ['DATABASE_USER']),
                                  password=get_docker_secret(
                                      os.environ['DATABASE_PASSWORD']),
                                  host="database",
                                  port="5432",
                                  database=get_docker_secret(os.environ['DATABASE_DB']))
    return connection


def close_connection(connection):
    connection.close()


def insert_user(connection, email, password, nickname):
    cursor = connection.cursor()

    sql = "INSERT INTO users (email, password, nickname) VALUES (%s, %s, %s) RETURNING id"
    val = (email, password, nickname)

    try:
        cursor.execute(sql, val)
        connection.commit()
    except:
        connection.rollback()
        raise Exception('Insert user failed.')

    user_id = cursor.fetchone()[0]

    cursor.close()

    return user_id


def insert_activation_token(connection, user_id, token):
    cursor = connection.cursor()

    sql = "INSERT INTO activation_tokens (user_id, token) VALUES (%s, %s) RETURNING id"
    val = (user_id, token)

    try:
        cursor.execute(sql, val)
        connection.commit()
    except:
        connection.rollback()
        raise Exception('Cannot add activation token.')

    cursor.close()


def get_user_id_by_token(connection, token):
    cursor = connection.cursor()

    sql = "SELECT user_id FROM activation_tokens WHERE token = %s"
    val = (token,)

    try:
        cursor.execute(sql, val)

        return cursor.fetchone()[0]
    except:
        raise Exception('Incorrect token.')

    cursor.close()


def activate_user(connection, token):
    user_id = get_user_id_by_token(connection, token)

    cursor = connection.cursor()

    sql_users = "UPDATE users SET activated = True WHERE id = %s"
    val_users = (user_id,)

    sql_activation_tokens = "DELETE FROM activation_tokens WHERE user_id = %s"
    val_activation_tokens = (user_id,)

    try:
        cursor.execute(sql_users, val_users)
        cursor.execute(sql_activation_tokens, val_activation_tokens)

        connection.commit()

    except:
        connection.rollback()
        raise Exception('Cannot activate user.')

    cursor.close()


def get_user_by_email(connection, email):
    cursor = connection.cursor()

    sql = "SELECT id, family_id, email, password, activated, nickname, created_date FROM users WHERE email = %s"
    val = (email,)

    try:
        cursor.execute(sql, val)
        user = cursor.fetchone()

        return {
            'id': user[0],
            'family_id': user[1],
            'email': user[2],
            'password': user[3],
            'activated': user[4],
            'nickname': user[5],
            'created_date': user[6]
        }

    except:
        raise Exception()

    cursor.close()


def insert_location(connection, user_id, name, lat, lng):
    cursor = connection.cursor()

    sql = "INSERT INTO locations (user_id, name, lat, lng) VALUES (%s, %s, %s, %s) RETURNING id"
    val = (user_id, name, lat, lng)

    try:
        cursor.execute(sql, val)
        connection.commit()
    except:
        connection.rollback()
        raise Exception('Insert location failed.')

    cursor.close()
