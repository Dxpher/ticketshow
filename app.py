from flask import Flask, render_template, redirect, request, make_response, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import sqlite3

app = Flask(__name__, static_url_path='/static', static_folder='static')

app.secret_key = '12_werdwr_123112_adiaisa'  # Add a secret key for session encryption
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, email,mname):
        self.id = email
        self.name=mname
def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    # Load the user from the database based on user_id
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT * FROM user WHERE useremail=?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        user = User(user_data[0],user_data[1])
        return user
    return None


def get_db_cursor():
    conn = sqlite3.connect('ticket.db')
    cursor = conn.cursor()
    return conn, cursor


@app.route('/', methods=['GET', 'POST'])
def login():
    conn, cursor = get_db_cursor()
    if request.method == 'POST':
        if request.form['submit'] == 'login':
            e_mail = request.form['email']
            pass_word = request.form['password']

            cursor.execute("SELECT * FROM user WHERE useremail=?", (e_mail,))
            query = cursor.fetchone()
            conn.close()
            if not (query):
                return render_template("login.html", message="Wrong email or account does not exist")
            elif (e_mail, pass_word) == (query[0],query[2]):
                user = User(e_mail,query[1])
                login_user(user)
                conn.close()
                session['logged_in'] = True
                session['user_id'] = user.id
                return redirect("/dashboard")
            else:
                return render_template("login.html", message="Wrong email or password! Please try again")
        elif request.form['submit'] == 'signup':
            e_mail = request.form['email']
            user_name = request.form['username']
            pass_word = request.form['password']

            # Check if the account already exists
            cursor.execute("SELECT count(*) FROM user WHERE useremail=?", (e_mail,))
            result = cursor.fetchone()

            if result[0] > 0:
                # Account already exists
                conn.close()
                return render_template('login.html', message='Account already exists')

            else:
                # Insert the new account into the database
                conn.execute("INSERT INTO user VALUES (?, ?, ?)", (e_mail, user_name, pass_word))
                conn.commit()
                conn.close()
                return render_template('login.html', message='Account created you can login now')

    if request.method == 'GET':
        session.pop('logged_in', None)
        return render_template('login.html')
@app.route("/dashboard")
@login_required
def dashboard():
    if not session.get('logged_in'):
        return redirect('/')

    conn, cursor = get_db_cursor()
    user_id = current_user.id
    user_name=current_user.name
    cursor.execute("SELECT e_id,e_name FROM event")  # Modify the SQL query here
    events = cursor.fetchall()
    conn.close()
    response = make_response(render_template("dashboard.html", allevent=events, username=user_name))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('logged_in', None)
    session.pop('user_id', None)
    response = make_response(redirect('/'))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/about')
@login_required
def about():
    if not session.get('logged_in'):
        return redirect('/')
    response = make_response(render_template("about.html", username=current_user.name))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route('/eventdetail')
@login_required
def event_detail():
    if not session.get('logged_in'):
        return redirect('/')
    image_id= request.args.get('image_id_value')
    conn, cursor = get_db_cursor()
    cursor.execute("select * from event where e_id=?",(image_id,))
    event_det=cursor.fetchone()
    org_id=event_det[7]
    cursor.execute("select * from organizer where o_id=?",(org_id,))
    org=cursor.fetchone()
    response = make_response(render_template("event_details.html", event=event_det,orga=org,username=current_user.name))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    conn.close()
    return response

@app.route('/add')
@login_required
def addEVEN():
    if not session.get('logged_in'):
        return redirect('/')
    response = make_response(render_template("Addevent.html",username=current_user.name))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response
@app.route('/tou')
@login_required
def tandc():
    if not session.get('logged_in'):
        return redirect('/')
    response = make_response(render_template("terms.html",username=current_user.name))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response
@app.route('/contact')
@login_required
def contactus():
    if not session.get('logged_in'):
        return redirect('/')
    response = make_response(render_template("contact.html",username=current_user.name))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8888)
    
