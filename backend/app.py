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
import bcrypt

app = Flask(__name__, static_url_path='/static')
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=["GET"])
@cross_origin()
def home():
    return "Hello, World!"


  # To securely hash passwords

@app.route('/register', methods=["POST"])
@cross_origin()
def register():
    """
    Endpoint to register a new user.
    Request Body: { "name": "string", "email": "string", "password": "string" }
    """
    myclient = pymongo.MongoClient("mongodb+srv://ronilcoder999:wfO4LmraAjvrqDMG@mailtrack.chu56.mongodb.net/?retryWrites=true&w=majority&appName=Mailtrack") 
    mydb = myclient["Mailtrack"]
    users_col = mydb["Users"]

    if request.method == "POST":
        data = request.json
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        # Check if email already exists
        if users_col.find_one({"email": email}):
            return jsonify({"error": "Email already registered"}), 409  # Conflict

        # Hash the password for security
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Save user details to database
        user = {"name": name, "email": email, "password": hashed_password.decode('utf-8')}
        users_col.insert_one(user)

        return jsonify({"message": "User registered successfully!"}), 201

    return jsonify({"error": "Invalid request method"}), 405


@app.route('/login', methods=["POST"])
@cross_origin()
def login():
    """
    Endpoint to log in an existing user.
    Request Body: { "email": "string", "password": "string" }
    """
    myclient = pymongo.MongoClient("mongodb+srv://ronilcoder999:wfO4LmraAjvrqDMG@mailtrack.chu56.mongodb.net/?retryWrites=true&w=majority&appName=Mailtrack") 
    mydb = myclient["Mailtrack"]
    users_col = mydb["Users"]

    if request.method == "POST":
        data = request.json
        email = data.get("email")
        password = data.get("password")

        # Find user by email
        user = users_col.find_one({"email": email})
        if not user:
            return jsonify({"error": "User not found"}), 404  # Not Found

        # Validate the password
        if bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            return jsonify({"message": "Login successful!"}), 200

        return jsonify({"error": "Invalid credentials"}), 401  # Unauthorized

    return jsonify({"error": "Invalid request method"}), 405


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

            # Ensure opened is properly formatted as an array
            opened_list = ele.get("opened", [])
            if isinstance(opened_list, str):
                # Convert a single string of concatenated dates to a list
                opened_list = [opened_list[i:i+19] for i in range(0, len(opened_list), 19)]

            li.append({
                "sender": ele["sender"], 
                "receiver": ele["receiver"], 
                "opened": opened_list  # Always return an array
            })
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
        
        # Corrected HTML with properly formatted CSS
        html = f"""\
        <html>
        
        <body>
            {text}<br>
            
            <img src="{img_url}" width="1" height="1" style="display:none;" alt="tracker" />
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
