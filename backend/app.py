from flask import Flask, request, send_from_directory, jsonify
import socket
from requests import get
from flask_cors import CORS, cross_origin
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from PIL import Image
import datetime
import pymongo

app = Flask(__name__, static_url_path='/static')
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=["GET"])
@cross_origin()
def home():
    return "Hello, World!"

@app.route('/explorer/<username>/<path>', methods=["GET", "POST"])
@cross_origin()
def explorer(username, path):
    myclient = pymongo.MongoClient("mongodb+srv://ronilcoder999:wfO4LmraAjvrqDMG@mailtrack.chu56.mongodb.net/?retryWrites=true&w=majority&appName=Mailtrack")
    mydb = myclient["Mailtrack"]
    mycol = mydb["Emailtrack"]

    # Update database with the time the email was opened
    mycol.find_one_and_update({'filename': path}, {'$push': {'opened': str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))}}, upsert=True)
    
    ip = get('https://api.ipify.org').text
    print('My public IP address is:', ip)
    print("Path Name:", path, "\nUserName:", username)
    return send_from_directory('/tmp', path)  # Serve the image from the /tmp directory

@app.route('/dashdata', methods=["GET", "POST"])
@cross_origin()
def dashdata():
    myclient = pymongo.MongoClient("mongodb+srv://ronilcoder999:wfO4LmraAjvrqDMG@mailtrack.chu56.mongodb.net/?retryWrites=true&w=majority&appName=Mailtrack")
    mydb = myclient["Mailtrack"]
    mycol = mydb["Emailtrack"]
    
    if request.method == "POST":
        print(request.json, "Dash Board Request")
        x = mycol.find({"sender": request.json["email"]})
        li = []
        for ele in x:
            print(ele["sender"], ele["receiver"], ele["opened"])
            li.append({"sender": ele["sender"], "receiver": ele["receiver"], "opened": ele["opened"]})
        return jsonify({"res": li})

    return jsonify({1: 1})


@app.route('/sendemail', methods=["POST"])
@cross_origin()
def sendemail():
    if request.method == "POST":
        sender_email = request.json["useremail"]
        receiver_email = request.json["recemail"]
        password = request.json["userpass"]  # Use App Password here

        message = MIMEMultipart("alternative")
        message["Subject"] = request.json["subject"]
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create and save a 1x1 transparent image temporarily in /tmp directory
        image = Image.new('RGBA', (1, 1), (0, 0, 0, 0))  # Create a transparent image
        filename = f"{sender_email}_{receiver_email}_{datetime.datetime.now().strftime('%Y-%m-%d+%H-%M-%S')}.png"
        temp_path = os.path.join("/tmp", filename)  # Save in /tmp directory
        image.save(temp_path)

        # Email content
        text = request.json["mailcontent"]
        # Use your Flask route for the image URL
        img_url = f"https://mailtrack.vercel.app/explorer/{sender_email}/{filename}"
        html = f"""\
        <html>
        <head>
            <style>
                .double-checkmark {
                position: relative;
                font-size: 200%; 
                color: #4CAF50; 
                }

                .double-checkmark::before {
                content: '\2714'; 
                position: absolute;
                left: -7px; 
                }

                .double-checkmark::after {
                content: '\2714'; 
                position: absolute;
                }
            </style>
        </head>
          <body>
            {text}<br>
            
            <img src="{img_url}" width="1" height="1" style="display:none;" alt="tracker" />
            <span>MailTrack</span></br>
            <span class="double-checkmark"></span>
          </body>
        </html>
        """

        # Email parts
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        # Send email
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)  # Use App Password
                server.sendmail(sender_email, receiver_email, message.as_string())
            print(request.json)
            
            # MongoDB logging
            myclient = pymongo.MongoClient("mongodb+srv://ronilcoder999:wfO4LmraAjvrqDMG@mailtrack.chu56.mongodb.net/?retryWrites=true&w=majority&appName=Mailtrack")
            mydb = myclient["Mailtrack"]
            mycol = mydb["Emailtrack"]
            mydict = {"sender": sender_email, "receiver": receiver_email, "filename": filename, "opened": []}
            x = mycol.insert_one(mydict)
            
            return jsonify({1: 1})
        except smtplib.SMTPAuthenticationError as e:
            print(f"Authentication error: {e}")
            return jsonify({"error": "Authentication failed"}), 500
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({"error": str(e)}), 500

    return jsonify({1: 1})


if __name__ == "__main__":
    app.run(debug=True)
