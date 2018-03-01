from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from databasesetup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

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

items = session.query(MenuItem).all()
for item in items:
     print item.name

