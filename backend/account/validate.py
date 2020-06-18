from django.contrib.auth import get_user_model
import re
userModel=get_user_model()

class validationErr(RuntimeError):
    def __init__(self,text):
        self.msg=text

def usernameValidation(username,regFlag=False):
    #Check conflict.
    if regFlag:
        if userModel.objects.filter(username=username).exists():
            raise validationErr('Username has been used.')
    #Check length and content.
    if len(username)>=30:
        raise validationErr('Username shouldn\'t be longer than 30.')
    if not re.search(u'^[_a-zA-Z0-9]+$',username):
        raise validationErr('Illegal symbol in username.')
