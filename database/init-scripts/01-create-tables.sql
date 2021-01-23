CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    family_id INTEGER,
    email VARCHAR (64) NOT NULL UNIQUE,
    password VARCHAR (192) NOT NULL,
    activated BOOLEAN DEFAULT FALSE NOT NULL,
    nickname VARCHAR (64) NOT NULL,
    created_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    name VARCHAR (256) NOT NULL,
    lat FLOAT NOT NULL,
    lng FLOAT NOT NULL,
    UNIQUE (lat, lng, user_id)
);

CREATE TABLE IF NOT EXISTS families (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER REFERENCES users(id) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS activation_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL UNIQUE,
    token VARCHAR (64) NOT NULL
);

CREATE TABLE IF NOT EXISTS family_invitations (
    id SERIAL PRIMARY KEY,
    family_id INTEGER REFERENCES families(id) ON DELETE CASCADE NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    token VARCHAR (64) NOT NULL
);

CREATE TABLE IF NOT EXISTS exports (
    id SERIAL PRIMARY KEY,
    from_user_id INTEGER REFERENCES users(id) NOT NULL,
    to_user_id INTEGER REFERENCES users(id) NOT NULL
);

ALTER TABLE users ADD CONSTRAINT users_family_id_fk FOREIGN KEY (family_id) REFERENCES families (id) MATCH FULL;
