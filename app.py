from flask import Flask, request, make_response, jsonify, abort
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import csv

app = Flask(__name__)
mysql = MySQL(app)
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'db1'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.route('/fetch/balance', methods=['GET'])
def get_balance():
    email = request.args.get('email')
    if not email:
        abort(404)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT amount FROM wallet WHERE email='{}'".format(email))
    row_count = cursor.rowcount
    if row_count == 0:
        abort(404)
    else:
        data = cursor.fetchall()
    return jsonify({'amount': data})

@app.route('/update/balance', methods=['POST', 'PUT'])
def update_balance():
    f = request.files['file']
    file_path = '/tmp/' + secure_filename(f.filename)
    f.save(file_path)
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            for row in reader:
                # The file I downloaded has unicode characters before email
                email = row.get("\ufeffEMAIL", "")
                amount = row.get("AMOUNT (Rs)", "")
                cursor.execute("SELECT amount FROM wallet WHERE email='{}'".format(email))
                row_count = cursor.rowcount
                if row_count == 0:
                    sql_statement = "INSERT INTO wallet(email ,amount) VALUES ('{}',{})".format(email, amount)
                else:
                    sql_statement = "UPDATE wallet SET amount = amount + {} WHERE email='{}'".format(amount, email)

                cursor.execute(sql_statement)

        conn.commit()
        cursor.close()
        return jsonify({'success': 'saved'})
    except Exception:
        abort(400)



if __name__ == '__main__':
    app.run(debug=True)