import connection


@connection.connection_handler
def register(cursor, username, password):
    cursor.execute("""
                    INSERT INTO users (username, password)
                    VALUES (%(username)s, %(password)s);
                   """,
                   {'password': password,
                    'username': username})


@connection.connection_handler
def check_username(cursor, username):
    cursor.execute("""
                    SELECT username FROM users
                    WHERE  username = %(username)s;
                   """, {'username': username})
    data = cursor.fetchall()
    return data


@connection.connection_handler
def get_hash_by_username(cursor, username):
    cursor.execute("""
                    SELECT password FROM users
                    WHERE username = %(username)s;
                   """,
                   {'username': username})
    data = cursor.fetchone()
    return data


@connection.connection_handler
def get_id_by_username(cursor, username):
    cursor.execute("""
                    SELECT id FROM users
                    WHERE username = %(username)s;
                   """,
                   {'username': username})
    data = cursor.fetchone()
    return data


@connection.connection_handler
def update_vote_table(cursor, user_id, planet_name):
    cursor.execute("""
                     INSERT INTO planet_votes (user_id, planet_name)
                     VALUES (%(user_id)s, %(planet_name)s)
                   """,
                   {'user_id': user_id,
                    'planet_name': planet_name})


@connection.connection_handler
def get_vote_statistics(cursor):
    cursor.execute("""
                    SELECT planet_name, COUNT(planet_name) FROM planet_votes
                    GROUP BY planet_name;
                   """,)
    data = cursor.fetchall()
    return data
