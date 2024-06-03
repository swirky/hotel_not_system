import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  #wymagane aby załadować moduły z folderu src (dynamiczne dodanie katalogu src do sciezki wyszukiwania modułów)
from userPass import UserPass
from userFactory import UserFactory
from adminUser import AdminUser
from standardUser import StandardUser



#test sprawdzający poprawnosc tworzenia instancji klasy userPass
def test_userpass_init():
    """
    The test_userpass_init function tests the UserPass class's __init__ method.
    It does this by creating a new instance of the UserPass class, and then checking that its user and password attributes are set correctly.
    
    :return: The user and password
    :doc-author: Trelent
    """
    userpass = UserPass("user", "password")
    assert userpass.user == "user"
    assert userpass.password == "password"

#test sprawdzający poprawne wygenerowanie losowej nazwy i hasla dla admina
def test_userpass_get_random_user_passw():
    """
    The test_userpass_get_random_user_passw function tests the get_random_user_passw function in the UserPass class.
        The test asserts that both user and password are 3 characters long.
    
    :return: A user and password of length 3
    :doc-author: Trelent
    """
    userpass = UserPass()
    userpass.get_random_user_passw()
    assert len(userpass.user) == 3
    assert len(userpass.password) == 3


def test_userpass_check_passw():
    """
    The test_userpass_check_passw function tests the check_passw function in the UserPass class.
        The test_userpass_check_passw function creates a new instance of the UserPass class, and then hashes
        its password using the hashed_password method. It then checks to see if it can correctly identify that 
        &quot;password&quot; is indeed its password, and that &quot;wrong-password&quot; is not.
    
    :return: True if the password is correct and false if it is wrong
    :doc-author: Trelent
    """
    userpass = UserPass("user", "password")
    hashed_password = userpass.hashed_passwd()
    assert userpass.check_passw("password", hashed_password) == True
    assert userpass.check_passw("wrong_password", hashed_password) == False

def test_adminuser_init():
    """
    The test_adminuser_init function tests the AdminUser class's __init__ method.
    It does this by creating an instance of the AdminUser class and then checking that its attributes are set correctly.
    
    :return: The following:
    :doc-author: Trelent
    """
    admin_user = AdminUser("admin", "admin_password")
    assert admin_user.user == "admin"
    assert admin_user.password == "admin_password"
    assert admin_user.is_active == True
    assert admin_user.is_admin == True


def test_userfactory_create_user():
    """
    The test_userfactory_create_user function tests the UserFactory.create_user function by creating two users, one admin and one standard user.
    
    :return: The user, which is a string that contains the username
    :doc-author: Trelent
    """
    admin_user = UserFactory.create_user("admin", "admin", "admin_password")
    standard_user = UserFactory.create_user("standard", "standard_user", "user_password")

    assert isinstance(admin_user, AdminUser)
    assert isinstance(standard_user, StandardUser)

    assert admin_user.user == "admin"
    assert standard_user.user == "standard_user"

    