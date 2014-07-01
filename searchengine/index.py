from flask import Flask
from sphinx import *

app = Flask(__name__)

@app.route('/')
def MainPage():
    return render_template('index.html',error = error) 

@app.rout('/search')
def SearchPageRedirect():
    return redirect(url_for('/'))

@app.route('/search',methods=['POST'])
def SearchPage():
    return redner_template('search.html',error = error)

if __name__ == '__main__':
    app.run()

