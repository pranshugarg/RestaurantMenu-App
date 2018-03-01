from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

## import CRUD operations as used before ######### 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databasesetup import Restaurant, Base, MenuItem

## create session and connect to the database #####
engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the declaratives can be accessed through a DBSession instance
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

## start of WebServerHandler class #### 
class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/edit"):
                # this splits into array of strings containing ids  separated by '/' 
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type' , 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method = 'POST' enctype = 'multipart/form-data' action = 'restaurant/%s/edit'>" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type='text' placeholder='%s'>" % myRestaurantQuery.name 
                    output += "<input type='submit' value='Rename'>"
                    output += "</form>"
                    output += "</html></body>"          
                    self.wfile.write(output)

            if self.path.endswith("/delete"):
                # this splits into array of strings containing ids  separated by '/' 
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type' , 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1> Do you want to delete % s ?" % myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method = 'POST' enctype = 'multipart/form-data' action = 'restaurant/%s/delete'>" % restaurantIDPath
                    output += "<input type='submit' value='Delete'>"
                    output += "</form>"
                    output += "</html></body>"          
                    self.wfile.write(output)

            if self.path.endswith("/restaurants"):
                # like earlier used in displaymenuitems.py
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<a href = '/restaurants/new'>Make a new Restaurant</a></br></br>"
                
                for restaurant in restaurants:
                 output += restaurant.name
                 output += "</br>" 
                 output += "<a href = '/restaurants/%s/edit'> Edit </a> " % restaurant.id
                 output += "</br>"
                 output += "<a href = '/restaurants/%s/delete'> Delete </a> "  %  restaurant.id
                 output += "</br>"

                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
                # this is to add a restaurant....
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<h1>Make a new  restaurant.</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='newRestaurantName' type='text' placeholder = 'New Restaurant Name'>"
                output += "<input type='submit' value='Create'>" 
                output += "<html><body>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return    

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>Hello!"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2>
                           <input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>&#161Hola! <a href = '/hello' > Back to Hello! </a> "
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return    
        
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
               
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                    
                    #rename
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        ###### Redirect to /restaurants page ######
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
               
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                    
                #delete
                if myRestaurantQuery != []:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    ###### Redirect to /restaurants page ######
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
               
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    
                messagecontent = fields.get('newRestaurantName')

                # Create a new restaurant.
                restaurant1 = Restaurant(name=messagecontent[0])
                session.add(restaurant1)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                ###### Redirect to /restaurants page ######
                self.send_header('Location', '/restaurants')
                self.end_headers()    
          
        except:
            pass

#########  end of WebServerHandler class        #### 
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()