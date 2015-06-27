import cgi
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
import MySQLdb
import os
import jinja2
from google.appengine.ext.webapp import template
from google.appengine.api import app_identity
import cloudstorage as gcs

my_default_retry_params = gcs.RetryParams(initial_delay= 0.2 , max_delay= 5.0,
                                          backoff_factor=2, max_retry_period=15
                                          )
gcs.set_default_retry_params(my_default_retry_params)


JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True,
  extensions=['jinja2.ext.autoescape'])

_INSTANCE_NAME = 'citric-cistern-97118:geoeq'

class MainPage(webapp2.RequestHandler):
    def get(self):
        
        path = os.path.join(os.path.dirname(__file__), 'query.html') 
        self.response.out.write(template.render(path, {}))   
        
        ''' env = os.getenv('SERVER_SOFTWARE')
        if (env and env.startswith('Google App Engine/')):
            db = MySQLdb.connect(
            unix_socket='/cloudsql/citric-cistern-97118:geoeq',
            db= 'project2',
            user='root')
        else:
            db = MySQLdb.connect(
            host='173.194.232.179',
            port=3306,
            db= 'project2',
            user='root')
 
        cursor = db.cursor()
        
        #cursor.execute('SELECT * FROM Whether where mag>2 ')
        whether= [];
        for row in cursor.fetchall():
          whether.append(dict([('Time',cgi.escape(row[0])),
                                 ('Latitude',cgi.escape(row[1])),
                                 ('Longitude',cgi.escape(row[2])),
                                 ('Depth',cgi.escape(row[3])),
                                 ('Magnitude',cgi.escape(row[4])),
                                 ('Magnitude Type',cgi.escape(row[5])),
                                 ('Nst',cgi.escape(row[6])),
                                 ('Gap',cgi.escape(row[7])),
                                 ('Dmin',cgi.escape(row[8])),
                                 ('Rms',cgi.escape(row[9])),
                                 ('Net',cgi.escape(row[10])),
                                 ('Id',cgi.escape(row[11])),
                                 ('Updated',cgi.escape(row[12])),
                                 ('Place',cgi.escape(row[13])),
                                 ('Type',cgi.escape(row[14]))
                                 ]))

        variables = {'whether': whether}
        template = JINJA_ENVIRONMENT.get_template('query.html')
        self.response.write(template.render(variables))
        db.close()'''



class whether(webapp2.RequestHandler):
    def post(self):

        env = os.getenv('SERVER_SOFTWARE')
        if (env and env.startswith('Google App Engine/')):
            db = MySQLdb.connect(
            unix_socket='/cloudsql/citric-cistern-97118:geoeq',
            db = 'project2',
            user='root')
        else:
            db = MySQLdb.connect(
            host='173.194.232.179',
            port=3306,
            db = 'project2',
            user='root')
                
        fmg = self.request.POST.get('fromval')
        tmg = self.request.POST.get('toval')
        bucket_name = 'revanth_2'
        
        self.response.headers['Content-Type'] = 'text/plain'
        bucket = '/' + bucket_name
        
        file_name = bucket +' /all_month.csv'
        self.tmp_filenames_to_clean_up = []

        cursor = db.cursor()
        #cursor.execute('INSERT INTO entries (mag, location) VALUES (%s, %s)', (mag, location))
        query = str('select * from Whether where mag >= '+str(fmg)+ ' and mag < '+str(tmg))
        cursor.execute(query)
        whether= [];
        for row in cursor.fetchall():
            whether.append(dict([('Time',cgi.escape(row[0])),
                                 ('Latitude',cgi.escape(row[1])),
                                 ('Longitude',cgi.escape(row[2])),
                                 ('Depth',cgi.escape(row[3])),
                                 ('Magnitude',cgi.escape(row[4])),
                                 ('Magnitude Type',cgi.escape(row[5])),
                                 ('Nst',cgi.escape(row[6])),
                                 ('Gap',cgi.escape(row[7])),
                                 ('Dmin',cgi.escape(row[8])),
                                 ('Rms',cgi.escape(row[9])),
                                 ('Net',cgi.escape(row[10])),
                                 ('Id',cgi.escape(row[11])),
                                 ('Updated',cgi.escape(row[12])),
                                 ('Place',cgi.escape(row[13])),
                                 ('Type',cgi.escape(row[14]))
                                 ]))

        db.close()
        
        self.redirect("/")

application = webapp2.WSGIApplication([('/', whether ),],
                              debug=True)

def main():
    application = webapp2.WSGIApplication([('/', MainPage),
                                           ('/sign', whether)],
                                          debug=True)
    run_wsgi_app(application)
if __name__ == "__main__":
    main()

