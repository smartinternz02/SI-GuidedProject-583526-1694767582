from flask import Flask, request, render_template, Request, session
import ibm_db
app = Flask(__name__)
app.secret_key="hai123"
conn=ibm_db.connect("DATABASE=bludb; HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;UID=jdx61184;PWD=FblcU5yVwTtkIC1I;SECURITY=SSL;SSLCERTIFICATE=DigiCertGlobalRootCA.crt",'','')
           
print(conn)
print(ibm_db.active(conn))



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        global uname
        uname = request.form['username']
        pword = request.form['password']
        print(uname, pword)
        sql = "SELECT * FROM REGISTER1 WHERE UNAME = ? AND PASSWORD = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.bind_param(stmt,2,pword)
        ibm_db.execute(stmt)
        out = ibm_db.fetch_assoc(stmt)
        print(out)
        if out != False:
            session['username'] = uname
            session['email'] = out['EMAIL']
            
            if out['ROLE'] == "Admin":
                return render_template("adminprofile.html", adname = out['NAME'], ademail = out['EMAIL'] )
            elif out['ROLE'] == "Student":
                return render_template("studentprofile.html",sname = out['NAME'], semail = out['EMAIL'])
            else: 
                return render_template("facultyprofile.html",fname = out['NAME'], femail = out['EMAIL'])
        else: 
            msg = "Invalid Credentials"
            return render_template("login.html",message1= msg)
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def regsiter():
    if request.method == "POST":
        name = request.form['NAME']
        email = request.form['EMAIL']
        uname = request.form['UNAME']
        password = request.form['PASSWORD']
        role = request.form['role']
        print(name,email,uname,password, role)
        sql = "SELECT * FROM REGISTER1 WHERE UNAME=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.execute(stmt)
        out = ibm_db.fetch_assoc(stmt)
        print(out)
        if out != False:
            msg = "Already Registered"
            return render_template("register.html",msg = msg)
        else:
            sql = "INSERT INTO REGISTER1 VALUES(?,?,?,?,?)"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, name)
            ibm_db.bind_param(stmt, 2,email)
            ibm_db.bind_param(stmt, 3, uname)
            ibm_db.bind_param(stmt, 4, password)
            ibm_db.bind_param(stmt, 5, role)
            ibm_db.execute(stmt)
            msg = "Registered"
            return render_template("register.html", msg =msg)

    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)