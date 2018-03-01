from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
      
      #employeeData is python file here.
from employeeData import Employee, Base, Address

                      #it is the name of database you want to populate
engine = create_engine('sqlite:///employeeData.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# address for pranshu   #Employee is a class.
employee1 = Employee(name="Pranshu Garg")

session.add(employee1)
session.commit()


address1 = Address(street="Ayodhya ganj", zip="203207", employee=employee1)

session.add(address1)
session.commit()

# Menu for Deepanshu
employee1 = Employee(name="Deepanshu Garg")

session.add(employee1)
session.commit()


address1 = Address(street="Ayodhya ganj", zip="203207", employee=employee1)

session.add(address1)
session.commit()

# Menu for Khushi

employee1 = Employee(name="Khushi Garg")

session.add(employee1)
session.commit()


address1 = Address(street="Ayodhya ganj", zip="203207", employee=employee1)

session.add(address1)
session.commit()

print "added addresses for employees!"