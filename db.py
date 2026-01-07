import psycopg2

conn = psycopg2.connect(host="localhost",
                        port="5432",
                        database="postgres",
                        user="dungbb",
                        password="123456")

curr = conn.cursor()

conn.set_session(autocommit=True)

curr.execute("select * from users")

print(curr.fetchall())

