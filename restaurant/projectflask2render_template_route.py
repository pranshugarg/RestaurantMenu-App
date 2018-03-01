from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databasesetup import Restaurant, Base, MenuItem

app = Flask(__name__)

## create session and connect to the database #####
engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    #rendering template
    return render_template('menu.html',restaurant=restaurant, items = items)


# Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


@app.route('/')
@app.route('/hello/')
def HelloWorld():
  restaurant = session.query(Restaurant).first()
  items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
  #without rendering template
  output = ''
  for item in items:
     output += item.name
     output += item.price
     output += item.description
     output += '</br>'
     output += '</br>'
  return output   

if __name__ == '__main__':
   app.debug = True
   app.run(host = '0.0.0.0' , port = 5000)  