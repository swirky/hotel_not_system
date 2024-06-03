from userPass import UserPass
import pydoc

class StandardUser(UserPass):

    def __init__(self,user,password):
        """
         
        About method return_x
 
 
        :param x: about x
        :return: x
    
        """
        super().__init__(user,password)
        self.is_active=True
        self.is_admin=False
    