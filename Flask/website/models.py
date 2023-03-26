# All the imports needed for this page
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_session import Session


# Checking our users IDs using Json 
class User(UserMixin):
    def __init__(self, user_json):
        self.user_json = user_json

    # Overriding get_id is required if you don't have the id property
    # Check the source code for UserMixin for details
    def get_id(self):
        object_id = self.user_json.get('_id')
        return str(object_id)