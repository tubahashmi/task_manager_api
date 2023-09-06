from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from apiserver.api.models.roles import Role

db_uri = "mysql://admin:admin@localhost/taskmanagerdb"

# Create a SQLAlchemy engine and session
engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
session = Session()

import pdb;pdb.set_trace()
# Create 'admin' role
admin_role = Role(name='admin')
session.add(admin_role)

# Create 'user' role
user_role = Role(name='user')
session.add(user_role)

# Commit the changes
session.commit()

# Close the session
session.close()

print("Roles 'admin' and 'user' have been added to the roles table.")
