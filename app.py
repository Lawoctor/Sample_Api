from flask import Flask, jsonify
import pyodbc

app = Flask(__name__)

server = 'sql.bsite.net\\MSSQL2016' 
database = 'lawoctor_test'
username = 'lawoctor_test'
password = 'lawoctor'
driver = 'SQL Server'
 
def get_db_connection():
    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};'
            f'UID={username};PWD={password}'
        )
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None

@app.route('/')
def home():
    return ('This is for testing API\'s. Currently we have /users')

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM ")  
    cursor.execute("SELECT * FROM sampletest")  
    # users = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    columns = [column[0] for column in cursor.description]  # Get column names dynamically

    # Dynamically build a list of dictionaries based on the columns
    users = [dict(zip(columns, row)) for row in cursor.fetchall()]
   
    cursor.close()
    conn.close()
    return jsonify(users)


if __name__ == '__main__':
    app.run(debug=True)