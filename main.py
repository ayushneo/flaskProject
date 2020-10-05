import pymysql
from flask import jsonify, request
from app import app
from db_config import mysql

@app.route('/')
def hello_world():
     return jsonify('HEllo World')

@app.route('/add', methods=['POST'])
def add_student():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
       data= request.json
       s_roll=data['s_roll']
       s_name=data['full_name']
       s_class=data['class']
       s_marks=data['marks']
       if s_roll and s_name and s_class and s_marks and request.method == 'POST':
           sql= "INSERT INTO T_Student(s_roll, full_name, class, marks) VALUES (%s,%s,%s,%s)"
           data=(s_roll,s_name,s_class,s_marks)
           cursor.execute(sql,data)
           conn.commit()
           resp=jsonify('Student added successfully!')
           resp.status_code=200
           return resp
       else:
           return 'error'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/students')
def students():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        conn=mysql.connect()
        cursor=conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM T_Student")
        rows=cursor.fetchall()
        resp=jsonify(rows)
        resp.status_code=200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update',methods=['PUT'])
def update_student():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _json = request.json
        _id = _json['s_roll']
        _name = _json['full_name']
        _class = _json['class']
        _marks = _json['marks']
        if _id and _name and _class and _marks and request.method=='PUT':
            sql= "UPDATE T_Student SET full_name=%s , class=%s,marks= %s WHERE s_roll=%s"
            data = (_name, _class, _marks,_id)
            cursor.execute(sql,data)
            conn.commit()
            resp=jsonify("Update Successful")
            resp.status_code=200
            return resp
        else:
            er = jsonify("error")
            return er

    finally:
        cursor.close()
        conn.close()

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute("DELETE FROM T_Student WHERE s_roll=%s", (id,))
        conn.commit()
        resp=jsonify('Student deleted ')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()




if __name__ == "__main__":
    app.run(debug=True)











