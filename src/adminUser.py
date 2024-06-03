from userPass import UserPass

class AdminUser(UserPass):
    def __init__(self,user,password):
        """
        The __init__ function is called when the class is instantiated.
            It sets up the attributes of an instance of a class.
            In this case, it takes in two arguments: user and password, which are then passed to the parent's __init__ function.
        
        :param self: Represent the instance of the class
        :param user: Create a user object
        :param password: Set the password of the user
        :return: Nothing
        :doc-author: Trelent
        """
        super().__init__(user,password)
        self.is_active=True
        self.is_admin=True
    
        
        