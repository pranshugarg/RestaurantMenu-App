from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#employeeData is python file here.
from employeeData import Employee, Base, Address

engine = create_engine('sqlite:///employeeData.db')

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


## to display all menu items.

items = session.query(Address).all()
for item in items:
     print item.street

