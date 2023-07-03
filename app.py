from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors   #This is used fetch details from the database and connect the database

app=Flask(__name__) #Start the program from name
app.config['MYSQL_HOST']="127.0.0.1"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="Btsjk1997!"
app.config['MYSQL_DB']="bigbasket_flask"

mysql=MySQL(app)

@app.route('/',methods=['GET','POST'])
def main_page():
    return render_template('main_page.html')
@app.route('/bill')
def bill():
    bill_number=10000
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('Select * from cart')
    details=cursor.fetchall()
    for i in details:
        bill_id=bill_number
        b_product=i['pro_name']
        quantity=i['quantity']
        cursor.execute('Select fv_price from fruit_vegetables,cart where cart.pro_name=fruit_vegetables.fv_name ')
        price=cursor.fetchone()['fv_price']
        cost=price*quantity
        cursor.execute('Insert into bill values (%s,%s,%s,%s)',(bill_id,b_product,quantity,cost))
        mysql.connection.commit()

    cursor.execute("SELECT * from bill where BId=%s",(bill_number,))
    bill_details=cursor.fetchall()
    cursor.execute('SELECT sum(cost) as total FROM bill where BId=%s',(bill_number,))
    total=cursor.fetchone()['total']


    cursor.execute('TRUNCATE table cart')
    bill_number+=1
    mysql.connection.commit()
    return render_template('bill.html',details=bill_details,total=total)





@app.route('/cart')
def cart():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('Select * from cart')
    details=cursor.fetchall()
    return render_template('cart.html',details=details)


@app.route('/all_page',methods=['POST','GET'])
def all_page():
    if request.method=='POST':
        details=request.form
        quantity=details["quantity"]
        name=details["name"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('Select * from Fruit_vegetables where fv_name=%s',(name,))  #Keep all the items in one table
        account=cursor.fetchone()
        cursor.execute('insert into cart values (%s,%s)',(name,quantity))
        mysql.connection.commit()
        return render_template('all_page.html')

    return render_template('all_page.html')
@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        details=request.form
        username=details["username"]
        email=details["email"]
        password=details["password"]
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('insert into signup_db values(%s,%s,%s)',(username,email,password))
        mysql.connection.commit()
        return redirect('/')
    return render_template('signup_page.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        details=request.form
        username=details['username']
        password=details['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('TRUNCATE TABLE bill')
        cursor.execute('Select * from signup_db where username=%s and password=%s',(username,password))
        account=cursor.fetchone()
        if account:
            return redirect(url_for('all_page'))



    return render_template('login_page.html')



if __name__ == "__main__":
    app.run(debug=True)
