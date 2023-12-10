import psycopg2

with psycopg2.connect(dbname="ref_system", user="postgres", password="1234", host="127.0.0.1") as db:
    cursor = db.cursor()
    
    def check_db():
        try:
            cursor.execute("SELECT * FROM users")
            print("Таблица users запущена")

        except:
            db.rollback()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            user_id BIGINT NOT NULL,
                            referrer_id BIGINT,
                            user_balance INT)
                            """
            )
            print("Таблица users создана")
        db.commit()
    
    def get_referrer(user_id):

        cursor.execute('SELECT referrer_id FROM users WHERE user_id = %s', (user_id,))

        return cursor.fetchone()
    

    def add_referrer(referrer_id, user_id):

        cursor.execute(
            "UPDATE users SET referrer_id = %s WHERE user_id = %s",
            (referrer_id, user_id),
        )

        db.commit()

    
    def get_info_user(user_id):
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))

        return cursor.fetchone()
    

    def user_exists(user_id):

        cursor.execute('SELECT user_id FROM users WHERE user_id = %s', (user_id,))

        if not cursor.fetchone():
            return False

        return True
    

    def add_user(user_id, ref_id=None):

        cursor.execute('''INSERT INTO users (
                          user_id,
                          referrer_id,
                          user_balance)
                          VALUES (%s, %s, %s)
                          ''',
                       (user_id, ref_id, 0))

        db.commit()

    
    def change_balance(user_id, amount):
        user_balance = get_balance(user_id)
        user_balance += amount

        cursor.execute(
            "UPDATE users SET user_balance = %s WHERE user_id = %s", (user_balance, user_id)
        )
        db.commit()


    def get_balance(user_id):
        return get_info_user(user_id)[3]