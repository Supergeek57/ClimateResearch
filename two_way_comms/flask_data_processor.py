from flask import Flask, request, jsonify
import pandas as pd
import os
from twilio.rest import Client

# Load the pre-trained ML model
# model = joblib.load('ml_model.pkl')

app = Flask(__name__)

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(account_sid, auth_token)

# Endpoint to receive survey data and make predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get the incoming data from Qualtrics webhook
    data = request.json
    print(data)

    # Parse survey responses into a DataFrame
    # survey_data = {
    #     'QID1': data['questions']['QID1'],
    #     'QID2': data['questions']['QID2'],
    # }
    # df = pd.DataFrame([survey_data])  # Convert to DataFrame
    # df.head()

    # Make prediction using model

@app.route('/send-sms', methods=['POST'])
def send_sms():
    try:
        to_number = request.json.get('to')
        survey_link = request.json.get('survey_link', 'https://universityofalabama.az1.qualtrics.com/jfe/form/SV_6gnRQdY0zIUMtUO')
        
        # Sending the SMS via Twilio
        message = client.messages.create(
            body=f'Please take our survey: {survey_link}',
            from_=twilio_number,
            to=to_number
        )
        
        return jsonify({'status': 'success', 'message_sid': message.sid}), 200
    
    except Exception as e:
        return jsonify({'status': 'failed', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)