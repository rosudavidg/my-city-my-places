from random import randint, uniform, choice

FILE_NAME_INSERT_USERS = '02-insert-users.sql'
FILE_NAME_INSERT_LOCATIONS = '03-insert-locations.sql'
FILE_NAME_INSERT_FAMILIES = '04-insert-families.sql'

USERS_COUNT_MIN = 10
USERS_COUNT_MAX = 100

# locations per user
LOCATIONS_COUNT_MIN = 1
LOCATIONS_COUNT_MAX = 20

LOCATION_LAT_MIN = -90
LOCATION_LAT_MAX = 90

LOCATION_LNG_MIN = -180
LOCATION_LNG_MAX = 180

FAMILIES_COUNT_MIN = 5
FAMILIES_COUNT_MAX = 15

# 1234 encrypted
DEFAULT_PASSWORD = 'e15eb021b161df9651dc9788d29e4e41b8e9664e71e9f4448055a2220835697553d6fc57a525e6620b7db0ac30b742c001bbe59bf533baf0e2d43f556dbaa9eaf46cae2829f236972cc5dc3364e039cbd055e2e7ae9294a6129e13bef8578edf'


def generate_users():
    users_count = randint(USERS_COUNT_MIN, USERS_COUNT_MAX)

    with open(FILE_NAME_INSERT_USERS, 'w') as f:
        for i in range(1, users_count + 1):
            f.write(
                f'INSERT INTO users (id, email, password, activated, nickname) VALUES ({i}, \'generated_email_{i}@gmail.com\', \'{DEFAULT_PASSWORD}\', TRUE, \'generated_nickname_{i}\');\n')

    return users_count


def generate_locations(users_count):
    with open(FILE_NAME_INSERT_LOCATIONS, 'w') as f:
        for user_id in range(1, users_count + 1):
            locations_count = randint(LOCATIONS_COUNT_MIN, LOCATIONS_COUNT_MAX)

            for i in range(locations_count):
                lat = uniform(LOCATION_LAT_MIN, LOCATION_LAT_MAX)
                lng = uniform(LOCATION_LNG_MIN, LOCATION_LNG_MAX)

                f.write(
                    f'INSERT INTO locations (user_id, name, lat, lng) VALUES ({user_id}, \'generated_name_{user_id}_{i}\', {lat}, {lng});\n')


def generate_families(users_count):
    users_list = [i + 1 for i in range(users_count)]

    families_count = randint(FAMILIES_COUNT_MIN, FAMILIES_COUNT_MAX)

    if families_count > users_count:
        families_count = users_count

    with open(FILE_NAME_INSERT_FAMILIES, 'w') as f:
        for i in range(1, families_count + 1):
            owner_id = choice(users_list)
            users_list.remove(owner_id)

            f.write(
                f'INSERT INTO families (id, owner_id) VALUES ({i}, {owner_id});\n')

        for user_id in users_list:
            family_id = randint(1, families_count + 1)

            if family_id != families_count + 1:
                f.write(
                    f'UPDATE users SET family_id = {family_id} WHERE id = {user_id};\n')


if __name__ == '__main__':
    users_count = generate_users()
    generate_locations(users_count)
    generate_families(users_count)
