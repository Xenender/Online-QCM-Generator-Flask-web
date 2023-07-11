from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
   return 'coucou'

@app.route("/login")
def login():
   return "c'est le login"

if __name__ == '__main__':
   app.run(debug = True)

app.run(host='0.0.0.0', port=8888)