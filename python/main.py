from flask import Flask, render_template

app = Flask(__name__, template_folder='../web', static_folder='../web/static')

HOST = 'localhost'
PORT = 8080
DEBUG = True

print('실행')

@app.route("/")
def home():
    return render_template("main.html")
if __name__=='__main__':
    app.run(host=HOST,port=PORT,threaded=DEBUG)