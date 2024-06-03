from flask import Flask,render_template,url_for,request,flash,g,redirect,session
from datetime import datetime
from userPass import UserPass
from userFactory import UserFactory
from config import app,app_info
from config import get_db,close_db
import sqlite3
import os
import string
import random
import binascii

        
@app.route('/init_app')
def init_app():
    """
    The init_app function is used to initialize the application.
    It checks if there are any active users in the database, and if not, it creates a new user with admin privileges.
    
    
    :return: A redirect to the index page
    :doc-author: Trelent
    """
    db=get_db()
    sql_statement='select count(*) as cnt from users where is_active and is_admin;'
    cur = db.execute(sql_statement)
    active_admins = cur.fetchone()
    
    if active_admins!=None and active_admins['cnt']>0:
        flash('Aplikacja gotowa do użycia. Znaleziono aktywnych użytkowników!')
        return redirect(url_for('index'))
    else:
        admin_user = UserFactory.create_user("admin","","")
        admin_user.get_random_user_passw()
        sql_statement = 'insert into users (name, password, is_active, is_admin) values (?, ?, True, True)'
        db.execute(sql_statement, [admin_user.user, admin_user.hashed_passwd()])
        db.commit()
        flash('Admin {} z hasłem {} został dodany'.format(admin_user.user, admin_user.password))
        return redirect(url_for('index'))
    

@app.route('/')
def index():
    """
    The index function is the default function that gets called when a user visits
    the root of the website. It renders the index.html template, which contains all
    of our HTML code for displaying content on this page.
    
    :return: A rendered template
    :doc-author: Trelent
    """
    login = UserPass(session.get('user'))
    login.get_user_info()
    return render_template('index.html', active_menu='Strona główa', login=login)
    
@app.route('/login', methods=['GET','POST'])
def login():
    """
    The login function is used to log in a user.
        It takes no arguments and returns nothing.
    
    
    :return: The rendered template login
    :doc-author: Trelent
    """
    login = UserPass(session.get('user'))
    login.get_user_info()

    if request.method=="GET":
        return render_template("login.html", active_menu='login', login=login)
    else:
        if 'user_name' not in request.form:
            user_name = ''
        else:
            user_name = request.form['user_name']
        if 'user_pass' not in request.form:
            user_pass=''
        else:
            user_pass = request.form['user_pass']
            
        login = UserPass(user_name,user_pass)
        login_record = login.login_user()
        
        if login_record!=None:
            session['user']= user_name
            flash('Zalogowano pomyślnie! Witaj {}'.format(user_name))
            return redirect(url_for('index'))
        else:
            flash('Logowanie nie powiodło się. Spróbuj ponownie.')
            return render_template('login.html', active_menu='login',login=login)
    
@app.route('/logout')
def logout():
    """
    The logout function is used to logout the user from the session.
        It checks if there is a 'user' in session, and if so it pops it out of
        the session and flashes a message saying that you have been logged out.
    
    
    :return: A redirect to the login page
    :doc-author: Trelent
    """
    if 'user' in session:
        session.pop('user',None)
        flash('Wylogowano')
    return redirect(url_for('login'))

@app.route('/users')
def users():
    """
    The users function is used to display a list of all users in the database.
    It also checks if the user is logged in as an admin, and if not, redirects them to login page.
    
    :return: A rendered template
    :doc-author: Trelent
    """
    login = UserPass(session.get('user'))
    login.get_user_info()

    if login.is_admin==False:
        flash('Nie jesteś zalogowany na konto administratora. Zaloguj się aby odwiedzić tę stronę!')
        return redirect(url_for('login'))
    else:
        db=get_db()
        sql_command='select * from users;'
        cur=db.execute(sql_command)
        users=cur.fetchall()
        return render_template('users.html', user_list=users, login=login)

@app.route('/user_status_change/<action>/<user_name>')
def user_status_change(action, user_name):
    """
    The user_status_change function is called when the user clicks on a button to change the status of another user.
    The function takes two arguments: action and user_name. The action argument can be either 'active' or 'admin'. 
    If it's active, then we toggle whether that particular user is active or not by adding 1 to their current value mod 2 (which will flip between 0 and 1). 
    If it's admin, then we do the same thing but for their admin status instead.
    
    :param action: Determine if the user is being made active or admin
    :param user_name: Identify the user that is to be changed
    :return: A redirect to the users page
    :doc-author: Trelent
    """
    if not 'user' in session:
        return redirect(url_for('login'))
    login = session['user']
    
    db=get_db()
    
    if action == 'active':
        db.execute('update users set is_active =(is_active + 1) % 2 where name= ? and name <> ?',[user_name,login])
        db.commit()
    elif action =='admin':
        db.execute('update users set is_admin = (is_admin + 1) % 2 where name= ? and name <> ?',[user_name,login])
        db.commit()
    return redirect(url_for('users'))
        

@app.route('/edit_user/<user_name>', methods=['GET', 'POST'])
def edit_user(user_name):
    """
    The edit_user function allows you to edit a user's information.
        
    
    :param user_name: Identify which user to edit
    :return: 'not implemented'
    :doc-author: Trelent
    """
    return 'not implemented'


@app.route('/user_delete/<user_name>', methods=['POST'])
def delete_user(user_name):
    """
    The delete_user function deletes a user from the database.
        Args:
            user_name (str): The name of the user to be deleted.
    
    
    :param user_name: Pass the name of the user to be deleted
    :return: A redirect to the users page
    :doc-author: Trelent
    """
    if request.method=='POST':
        
        if not 'user' in session:
            return redirect(url_for(login))
        login = session['user']
        
        db=get_db()
        sql_zapytanie='DELETE from users where name=?;'
        if user_name!=login:
            db.execute(sql_zapytanie,[user_name])
            db.commit()
        else:
            flash('Nie można usunąć konta na którym jesteś aktualnie zalogowany!')
            return redirect(url_for('users'))
        
        flash('Usunieto uzytkownika {}!'.format(user_name))
        return redirect(url_for('users'))

        
@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    """
    The new_user function is responsible for creating a new user.
    It first checks if the user is logged in as an admin, and if not, redirects them to the login page.
    If they are logged in as an admin, it then checks whether or not there was a POST request made to this function.  If so, it creates a new User object using the UserFactory class and inserts that into our database.
    
    :return: A redirect to the users function
    :doc-author: Trelent
    """
    login = UserPass(session.get('user'))
    login.get_user_info()

    if not login.is_admin:
        flash('Nie jesteś zalogowany na konto administratora. Zaloguj się aby odwiedzić tę stronę!')
        return redirect(url_for('login'))
    
    db=get_db()
    message = None 
    user = {}  #tablica do przechowywania danych z formularza
    
    if request.method =='GET':
        return render_template('new_user.html', active_menu='users', user=user, login=login)
    else:
        user['user_name'] ="" if not 'user_name' in request.form else request.form['user_name']
        user['user_password']= "" if not 'user_password' in request.form else request.form['user_password']
        user['user_type']= "" if not 'user_type' in request.form else request.form['user_type']
    
    sql_query='select count(*) as cnt from users where name=?;'
    cur = db.execute(sql_query,[user['user_name']])
    record = cur.fetchone()
    is_user_name_unique = (record['cnt']==0)

    if user['user_name']=="":
        message='Nie podano nazwy użytkownika!'
    elif user['user_password']=="":
        message='Nie podano hasła!'
    elif not is_user_name_unique:
        message="Konto z tą nazwą użytkownika już istnieje!"
    elif user['user_type']=="":
        message="Nie podano typu użytkownika (standard lub admin)"
        
    if not message:
        new_user = UserFactory.create_user(user['user_type'],user['user_name'], user['user_password'])
        
        sql_statement='insert into users (name,password,is_active,is_admin) values (?,?,?,?)'
        db.execute(sql_statement,[new_user.user,new_user.hashed_passwd(), new_user.is_active,new_user.is_admin])
        db.commit()
        flash('User {} has been created'.format(user['user_name']))
        return redirect(url_for('users'))
    else:
        flash('Correct error: {}'.format(message))
        return render_template('new_user.html', active_menu='users', user=user)
        
        
@app.route('/form', methods=['GET', 'POST'])
def form():
    """
    The form function is responsible for handling the form.html template,
    which allows users to submit a notification about a problem in their room.
    The function checks if the user is logged in and if not, redirects them to 
    the login page with an appropriate flash message. If they are logged in, 
    it renders the form template and waits for POST requests from it.
    
    :return: A redirect to the form_content function
    :doc-author: Trelent
    """
    login = UserPass(session.get('user'))
    login.get_user_info()
    
    if not login.is_valid:
        flash('Nie jesteś zalogowany na konto użytkownika. Zaloguj się aby odwiedzić tę stronę!')
        return redirect(url_for('login'))
    else:    
        if request.method == 'GET':
            return render_template('form.html', login=login)
        else:
            numer_pokoju = request.form.get('numer_pokoju', '')
            nazwisko_zlgaszajacego = request.form.get('nazwa_goscia', '')
            priorytet = request.form.get('priorytet', '')
            notatka = request.form.get('skarga', '')
            
            flash('Zgłoszenie zostało wysłane poprawnie!')
            
            db = get_db()
            sql_command = 'INSERT INTO notifications (room_number, guest_name, notification, priority, user_id) VALUES (?, ?, ?, ?, ?)'
            db.execute(sql_command, [numer_pokoju, nazwisko_zlgaszajacego, notatka, priorytet, login.user_id])
            db.commit()
            
            return redirect(url_for('form_content', 
                                    priorytet=priorytet, 
                                    skarga=notatka, 
                                    numer_pokoju=numer_pokoju, 
                                    nazw_zglaszajacego=nazwisko_zlgaszajacego))

@app.route('/form_content', methods=['GET'])
def form_content():
    """
    The form_content function is used to render the form_content.html template,
    which contains a form that allows users to submit complaints about their hotel 
    rooms. The function takes in four arguments: priorytet, skarga, numer_pokoju and 
    nazwisko_zlgaszajacego. These are all strings that will be passed into the HTML 
    template as variables.
    
    :return: A rendered template
    :doc-author: Trelent
    """
    login = UserPass(session.get('user'))
    login.get_user_info()
    
    priorytet = request.args.get('priorytet', "")
    notatka = request.args.get('skarga', "")
    numer_pokoju = request.args.get('numer_pokoju', "")
    nazwisko_zlgaszajacego = request.args.get('nazw_zglaszajacego', "")
    
    return render_template('form_content.html', 
                           login=login, 
                           priorytet=priorytet, 
                           skarga=notatka, 
                           numer_pokoju=numer_pokoju, 
                           nazw_zglaszajacego=nazwisko_zlgaszajacego)

@app.route('/notifications', methods=['GET','POST'])
def notifications():
    """
    The notifications function is responsible for displaying all notifications in the database.
    It also checks if the user is logged in and if he has admin rights. If not, it displays only his own notifications.
    
    :return: The notifications
    :doc-author: Trelent
    """
    login = UserPass(session.get('user'))
    login.get_user_info()

    if not login.is_valid:
        flash('Nie jesteś zalogowany na konto użytkownika. Zaloguj się aby odwiedzić tę stronę!')
        return redirect(url_for('login'))
    else:    
        db=get_db()
        if login.is_admin:
            sql_command='SELECT notifications.id, notifications.room_number, notifications.guest_name, notifications.notification, notifications.priority,notifications.user_id, users.name as name FROM notifications JOIN users ON notifications.user_id = users.id;'
            cur=db.execute(sql_command)
        else:
            sql_command='select * from notifications where user_id=?;'
            cur=db.execute(sql_command,[login.user_id])
            
        
        notyfikacje=cur.fetchall()
        return render_template('notifications.html', zgloszenia=notyfikacje, login=login)

@app.route('/delete/<int:notification_id>', methods=['POST'])
def delete_not(notification_id):
    """
    The delete_not function deletes a notification from the database.
        Args:
            notification_id (int): The id of the notification to be deleted.
    
    :param notification_id: Delete the notification with a given id
    :return: The redirect function, which returns a response object
    :doc-author: Trelent
    """
    login = UserPass(session.get('user'))
    login.get_user_info()

    db=get_db()
    sql_zapytanie='DELETE from notifications where id=?;'
    db.execute(sql_zapytanie,[notification_id])
    db.commit()
    flash('Usunięto zgloszenie!')
    return redirect(url_for('notifications'))

@app.route('/edition/<int:notification_id>', methods=['GET','POST'])
def edition(notification_id):
    """
    The edition function is responsible for editing the notification.
    It takes one argument, which is the id of a notification to be edited.
    The function first checks if user is logged in and if not, redirects him to login page. 
    If he's logged in it renders edition template with data from database (notification). 
    When user submits form with new data, this function updates database.
    
    :param notification_id: Identify the notification that is being edited
    :return: The edition
    :doc-author: Trelent
    """
    login = UserPass(session.get('user'))
    login.get_user_info()

    if not login.is_valid:
        flash('Nie jesteś zalogowany na konto użytkownika. Zaloguj się aby odwiedzić tę stronę!')
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            db=get_db()
            sql_zapytanie='select id, room_number, guest_name, notification, priority from notifications where id=?'
            cur=db.execute(sql_zapytanie,[notification_id])
            notyfikacja=cur.fetchone()
            return render_template('edition.html', zgloszenie=notyfikacja, login=login)
        else:
            numer_pokoju=0
            
            if 'numer_pokoju' in request.form:
                numer_pokoju=request.form['numer_pokoju']
                
            nazwisko_zlgaszajacego=""
            if 'nazwa_goscia' in request.form:
                nazwisko_zlgaszajacego=request.form['nazwa_goscia']
                
            
            if 'priorytet' in request.form:
                priorytet=request.form['priorytet']
                
            notatka=""
            if 'skarga' in request.form:
                notatka=request.form['skarga']
                
            db=get_db()
            sql_command = 'update notifications set room_number=?, guest_name=?, notification=? where id=?'
            db.execute(sql_command, [numer_pokoju,nazwisko_zlgaszajacego,notatka,notification_id])
            db.commit()
            return redirect(url_for('notifications'))
            
        
        