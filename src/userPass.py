import bcrypt
import binascii
import string 
import random
from config import get_db,close_db

class UserPass:
    def __init__(self, user='', password=''):   #wartosc domyslna argumentu password to pusty string dlatego nie jest wymagane podanie go w instancji
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and takes arguments that are passed to it.
        
        
        :param self: Represent the instance of the class
        :param user: Set the value of the user attribute
        :param password: Set the password attribute
        :return: The instance of the class (self)
        :doc-author: Trelent
        """
        self.user=user
        self.password=password 

    def get_user_info(self):
        """
        The get_user_info function is used to get the user information from the database.
            It takes in a username and returns a boolean value for whether or not that user exists, 
            as well as if they are an admin or not.
        
        :param self: Represent the instance of the class
        :return: The user's id, is_valid and is_admin
        :doc-author: Trelent
        """
        db=get_db()
        sql_query='select * from users where name = ?;'
        cur = db.execute(sql_query,[self.user])
        db_user = cur.fetchone()  
          

        if db_user == None:
            self.is_valid = False
            self.is_admin = False  
        elif db_user['is_active']!=1:
            self.is_valid = False
            self.is_admin = False
        else:
            self.is_valid = True
            self.is_admin = db_user['is_admin']
            self.user_id = db_user['id']

    #generowanie losowych nazw user i password 3 znakowych w kodzie ascii
    def get_random_user_passw(self):
        """
        The get_random_user_passw function generates a random username and password.
            The function uses the string module to generate a random lowercase letter for the username, 
            and then concatenates three of these letters together to form the username. 
            
            For generating the password, we use both uppercase and lowercase letters from string module.
        
        :param self: Refer to the current instance of a class
        :return: The user and password as a string
        :doc-author: Trelent
        """
        random_user = ''.join(random.choice(string.ascii_lowercase)for i in range(3))
        self.user = random_user
        
        passw_characters= string.ascii_letters
        random_password = ''.join(random.choice(passw_characters)for i in range(3))
        self.password = random_password
        
    def hashed_passwd(self):
        """
        The hashed_passwd function takes the password from the user and encodes it into a byte string.
        Then, using bcrypt's hashpw function, we generate a salt for our password and then hash it.
        The hashed value is returned to be stored in our database.
        
        :param self: Make the method a bound method, which means that it can be called on an instance of the class
        :return: The hashed password
        :doc-author: Trelent
        """
        passw = self.password.encode('utf-8')
        hashed = bcrypt.hashpw(passw,bcrypt.gensalt(10))
        return hashed
    
    #metody weryfikujące poprawnosc nazwy uzytkownika i haslo
    
    def check_passw(self,checked_passw, stored_passw):
        """
        The check_passw function takes two arguments:
            1. checked_passw - the password that is being checked against the stored password
            2. stored_passw - the hashed and salted version of a user's password, which is retrieved from 
                              our database
        
        :param self: Represent the instance of the class
        :param checked_passw: Store the password that is entered by the user
        :param stored_passw: Store the password that is hashed and salted
        :return: A boolean value
        :doc-author: Trelent
        """
        checked_passw = checked_passw.encode('utf-8')
        if bcrypt.checkpw(checked_passw, stored_passw):
            return True
        else:
            return False
    
    def login_user(self):
        """
        The login_user function is used to authenticate a user.
            It takes the username and password as input, and returns a record of the user if they are authenticated.
            If not, it returns None.
        
        :param self: Refer to the current instance of the class
        :return: The user record if the login is successful
        :doc-author: Trelent
        """
        db=get_db()
        sql_statement=' select id,name,password,is_active,is_admin from users where name=? '
        cur = db.execute(sql_statement,[self.user])
        user_record = cur.fetchone()
        
        if user_record!=None and self.check_passw(self.password,user_record['password']):
            return user_record
        else:
            self.user =None
            self.password=None
            return None
        
    
    

        
        
    
    
        
    
        
    
