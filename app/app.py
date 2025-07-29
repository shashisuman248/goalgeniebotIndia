from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
user_sessions = {}

@app.route('/whatsapp', methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').strip().lower()
    sender = request.values.get('From', '')

    resp = MessagingResponse()
    msg = resp.message()
    session = user_sessions.get(sender, {'step': 0})

    if session['step'] == 0:
        msg.body("🙏 Namaste! Yeh GoalGenieBot powered by Sip Wealth hai.\nAapka investment goal kya hai?")
        session['step'] = 1
    elif session['step'] == 1:
        session['goal'] = incoming_msg
        msg.body("Har mahine kitni SIP karna chahte hain? (₹)")
        session['step'] = 2
    elif session['step'] == 2:
        session['sip'] = incoming_msg
        msg.body("Kitne saal ke liye invest karna chahte hain?")
        session['step'] = 3
    elif session['step'] == 3:
        session['tenure'] = incoming_msg
        msg.body("Risk profile kya hai? (Low / Medium / High)")
        session['step'] = 4
    elif session['step'] == 4:
        session['risk'] = incoming_msg
        msg.body(f"✅ Summary:\nGoal: {session['goal']}\nSIP: ₹{session['sip']} for {session['tenure']} years\nRisk: {session['risk']}\n\n📊 Recommendation: Axis Growth Opportunities Fund (Demo)\n\nPDF report jaldi milega 🙏")
        session['step'] = 0

    user_sessions[sender] = session
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
