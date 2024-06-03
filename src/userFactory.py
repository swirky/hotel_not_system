from adminUser import AdminUser
from standardUser import StandardUser

class UserFactory:
    @staticmethod
    def create_user(usertype,user,password):
        """
        The create_user function creates a user object of the specified type.
            
        
        :param usertype: Determine which type of user to create
        :param user: Pass the username to the constructor of adminuser or standarduser
        :param password: Set the password of the user
        :return: An object of type adminuser or standarduser
        :doc-author: Trelent
        """
        if usertype=="admin":
            return AdminUser(user,password)
        elif usertype=="standard":
            return StandardUser(user,password)
        else:
            raise ValueError("Nieznany typ użytkownika")
        

