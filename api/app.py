from flask import Flask, request
from flask_ngrok import run_with_ngrok 
from sendToMongoDB import push_to_mongo

app = Flask(__name__)
run_with_ngrok(app)

@app.route('/')
def index():
    return 'Welcome to Smart ECG Monitoring System!'

# Route to collect user's email
@app.route('/email', methods=['GET', 'POST'])
def user_email():
    global user_email 
    user_email = request.json
    print(user_email)
    return user_email

# Route to collect json object containing user's ECG Data
@app.route('/data', methods=['GET', 'POST'])
def collect_data():
    data = request.json
    print(data)
    push_to_mongo(data, user_email)
    return {'data': data}

if __name__ == "__main__": 
  app.run()