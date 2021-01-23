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

    id = cursor.fetchone()[0]

    cursor.close()

    return id


def create_family(connection, user_id):
    cursor = connection.cursor()

    sql = "INSERT INTO families (owner_id) VALUES (%s) RETURNING id"
    val = (user_id,)

    sql_update = "UPDATE users SET family_id = %s WHERE id = %s"

    try:
        cursor.execute(sql, val)

        family_id = cursor.fetchone()[0]
        val_update = (family_id, user_id)

        cursor.execute(sql_update, val_update)

        connection.commit()
    except:
        connection.rollback()
        raise Exception('Insert family failed.')

    cursor.close()


def delete_family(connection, user_id):
    cursor = connection.cursor()

    sql = "SELECT id FROM families WHERE owner_id = %s"
    val = (user_id,)

    sql_update = "UPDATE users SET family_id = NULL WHERE family_id = %s"

    sql_delete = "DELETE FROM families WHERE id = %s"

    try:
        cursor.execute(sql, val)

        family_id = cursor.fetchone()[0]

        val_update = (family_id,)
        cursor.execute(sql_update, val_update)

        val_delete = (family_id,)
        cursor.execute(sql_delete, val_delete)

        connection.commit()
    except:
        connection.rollback()
        raise Exception('Delete family failed.')

    cursor.close()


def create_family_invitation(connection, user_id, email, invitation_token):
    cursor = connection.cursor()

    sql_select_family_id = "SELECT id FROM families WHERE owner_id = %s"
    val_select_family_id = (user_id,)

    sql_select_user_id = "SELECT id FROM users WHERE email = %s"
    val_select_user_id = (email,)

    sql_insert = "INSERT INTO family_invitations (family_id, user_id, token) VALUES (%s, %s, %s)"

    try:
        cursor.execute(sql_select_family_id, val_select_family_id)
        family_id = cursor.fetchone()[0]

        cursor.execute(sql_select_user_id, val_select_user_id)
        user_id = cursor.fetchone()[0]

        val_insert = (family_id, user_id, invitation_token)
        cursor.execute(sql_insert, val_insert)

        connection.commit()
    except:
        connection.rollback()
        raise Exception('Create family invitations failed.')

    cursor.close()


def join_family(connection, user_id, token):
    cursor = connection.cursor()

    sql = "SELECT id, family_id FROM family_invitations WHERE user_id = %s AND token = %s"
    val = (user_id, token)

    sql_update = "UPDATE users SET family_id = %s WHERE id = %s"
    sql_delete = "DELETE FROM family_invitations WHERE id = %s"

    try:
        cursor.execute(sql, val)
        id, family_id = cursor.fetchone()

        val = (family_id, user_id)
        cursor.execute(sql_update, val)

        val = (id,)
        cursor.execute(sql_delete, val)

        connection.commit()
    except:
        connection.rollback()
        raise Exception('Join family failed.')

    cursor.close()


def leave_family(connection, user_id):
    cursor = connection.cursor()

    sql = "SELECT COUNT(*) FROM families WHERE owner_id = %s"
    val = (user_id,)

    sql_update = "UPDATE users SET family_id = NULL WHERE id = %s"

    try:
        cursor.execute(sql, val)

        is_owner = cursor.fetchone()[0] > 0

        if is_owner:
            raise Exception()

        val_update = (user_id,)
        cursor.execute(sql_update, val_update)

        connection.commit()
    except:
        connection.rollback()
        raise Exception('Leave family failed.')

    cursor.close()


def get_locations(connection, user_id):
    cursor = connection.cursor()

    sql = "SELECT id, name, lat, lng FROM locations WHERE user_id = %s"
    val = (user_id,)

    sql_select_family_id = "SELECT family_id FROM users WHERE id = %s"
    val_select_family_id = (user_id,)

    sql_family = "SELECT l.id, l.name, l.lat, l.lng, l.user_id, u.nickname FROM locations l JOIN users u ON l.user_id = u.id WHERE u.family_id = %s"

    try:
        cursor.execute(sql, val)

        own_locations = []
        family_locations = []

        for location in cursor.fetchall():
            own_locations.append({
                'id': location[0],
                'name': location[1],
                'lat': location[2],
                'lng': location[3]
            })

        cursor.execute(sql_select_family_id, val_select_family_id)
        res = cursor.fetchone()

        if res != None:
            family_id = res[0]
            val_family = (family_id,)
            cursor.execute(sql_family, val_family)

            for location in cursor.fetchall():
                if location[4] != user_id:
                    family_locations.append({
                        'id': location[0],
                        'name': location[1],
                        'lat': location[2],
                        'lng': location[3],
                        'user_id': location[4],
                        'user_nickname': location[5],
                    })

    except:

        connection.rollback()
        raise Exception('Leave family failed.')

    cursor.close()

    return {
        "own": own_locations,
        "family": family_locations

    }


def delete_location(connection, user_id, location_id):
    cursor = connection.cursor()

    sql = "DELETE FROM locations WHERE id = %s AND user_id = %s"
    val = (location_id, user_id)

    try:
        cursor.execute(sql, val)

        connection.commit()
    except:
        connection.rollback()
        raise Exception('Delete location failed.')

    cursor.close()


def get_family_details(connection, user_id):
    cursor = connection.cursor()

    res = dict()
    sql_family_id = "SELECT family_id FROM users WHERE id = %s"
    sql_is_owner = "SELECT COUNT(*) FROM families WHERE id = %s AND owner_id = %s"
    sql_members = "SELECT id, nickname FROM users WHERE family_id = %s AND id != %s"

    try:
        val_family_id = (user_id,)
        cursor.execute(sql_family_id, val_family_id)

        family_id = cursor.fetchone()[0]

        if family_id != None:
            val_is_owner = (family_id, user_id)
            cursor.execute(sql_is_owner, val_is_owner)
            is_owner = cursor.fetchone()[0] > 0
            res['is_owner'] = is_owner

            val_members = (family_id, user_id)
            cursor.execute(sql_members, val_members)
            members = []

            for member in cursor.fetchall():
                members.append({
                    'id': member[0],
                    'nickname': member[1]
                })

            res['members'] = members

        res['family_id'] = family_id

    except:
        raise Exception('Incorrect token.')

    cursor.close()

    return res
