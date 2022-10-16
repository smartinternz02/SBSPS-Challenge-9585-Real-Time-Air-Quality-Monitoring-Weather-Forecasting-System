from flask import Flask, request, jsonify, render_template
import requests
import json

API_KEY = "JV480I6W3vOoxEFx9RqBtzEmI5_EQDA5hT7zID7fUAke"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data ={"apikey":API_KEY, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"})
mltoken = token_response.json()["access_token"]
print("mltoken",mltoken)

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


######       Testing the API       ###########

# payload_scoring = {"input_data":[{"field": [["PM2.5","PM10","NO","NO2","NOX","NH3","CO","SO2","TOL"]],
#                                   "values":[[2.0, 1.5, 1.5, 3.3, 0.2, 1.5, 2.0, 0.25, 1.3]]}]}

# response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/541fbf3b-0170-4317-93bb-4a8d66c097d2/predictions?version=2022-10-14', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})

# print("Scoring response")
# prediction = response_scoring.json()
# print("AQI value is: ",prediction['predictions'][0]['values'][0][0]) 




########     Creating The Flask App    ##########

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    
    pm25 = request.form["pm2.5"]
    pm10 = request.form["pm10"]
    no = request.form["no"]
    no2 = request.form["no2"]
    nox = request.form["nox"]
    nh3 = request.form["nh3"]
    co = request.form["co"]
    so2 = request.form["so2"]
    tol = request.form["tol"]

    
    t = [[float(pm25),float(pm10),float(no),float(no2),float(nox),float(nh3),float(co),float(so2),float(tol)]]
    print(t)

    payload_scoring = {"input_data":[{"field": [["PM2.5","PM10","NO","NO2","NOX","NH3","CO","SO2","TOL"]],
                                      "values":t}]}
    
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/541fbf3b-0170-4317-93bb-4a8d66c097d2/predictions?version=2022-10-14', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})

    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)
    ans = str(predictions['predictions'][0]['values'][0][0])
    return render_template('index.html', prediction_text= ans)

if __name__ == '__main__':
    app.run(debug = True)

