from flask import Flask, request, send_from_directory,jsonify
import socket
from requests import get
from flask_cors import CORS,cross_origin
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from PIL import Image
import datetime
import pymongo

app = Flask(__name__, static_url_path='/static')
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Define the root route
@app.route('/', methods=["GET"])
@cross_origin()
def home():
    return "Hello, World!"

# @app.route('/explorer/<username>/<path>',methods=["GET","POST"])
# @cross_origin()
# def explorer(username,path):
#     myclient = pymongo.MongoClient("mongodb+srv://ronilcoder999:wfO4LmraAjvrqDMG@mailtrack.chu56.mongodb.net/?retryWrites=true&w=majority&appName=Mailtrack")
#     mydb = myclient["Mailtrack"]
#     mycol = mydb["Emailtrack"]

#     mycol.find_one_and_update({'filename':path}, {'$push': {'opened': str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))}}, upsert = True)
    
#     ip = get('https://api.ipify.org').text
#     print ('My public IP address is:', ip)
#     print("Path Name:", path,"\nUserName:", username)
#     return send_from_directory('static', f"{username}/{path}")


# @app.route('/dashdata',methods=["GET","POST"])
# @cross_origin()
# def dashdata():
#     myclient = pymongo.MongoClient("mongodb+srv://ronilcoder999:wfO4LmraAjvrqDMG@mailtrack.chu56.mongodb.net/?retryWrites=true&w=majority&appName=Mailtrack")
#     mydb = myclient["Mailtrack"]
#     mycol = mydb["Emailtrack"]
    
#     if request.method=="POST":
#         print(request.json,"Dash Board Request")
#         x = mycol.find({"sender":request.json["email"]})
#         li=[]
#         dicti = {}
#         for ele in x:
#             print(ele["sender"],ele["receiver"],ele["opened"])
#             dicti["sender"]=ele["sender"]
#             dicti["receiver"]=ele["receiver"]
#             dicti["opened"]=ele["opened"]
#             li.append({"sender":ele["sender"],"receiver":ele["receiver"],"opened":ele["opened"]})
#             dicti={}
#         return jsonify ({"res":li})

#     return jsonify({1:1})



# @app.route('/sendemail', methods=["POST"]) 
# @cross_origin()   
# def sendemail():
#     if request.method == "POST":
#         sender_email = request.json["useremail"]
#         receiver_email = request.json["recemail"]
#         password = request.json["userpass"]  # Use App Password here

#         message = MIMEMultipart("alternative")
#         message["Subject"] = request.json["subject"]
#         message["From"] = sender_email
#         message["To"] = receiver_email

#         # Ensure directory exists
#         user_directory = f"static/{sender_email}"
#         if not os.path.isdir(user_directory):
#             os.makedirs(user_directory)
        
#         # Create and save image
#         image = Image.new('RGB', (10, 10))
#         filename = f"{sender_email}_{receiver_email}_{datetime.datetime.now().strftime('%Y-%m-%d+%H-%M-%S')}.jpg"
#         image.save(os.path.join(user_directory, filename))
        
#         # Email content
#         text = request.json["mailcontent"]
#         html = f"""\
#         <html>
#           <body>
#             <p>
#                <img src="http://localhost:5000/explorer/{sender_email}/{filename}"></img>
#             </p>
#           </body>
#         </html>
#         """
        
#         # Email parts
#         part1 = MIMEText(text, "plain")
#         part2 = MIMEText(html, "html")
#         message.attach(part1)
#         message.attach(part2)

#         # Send email
#         context = ssl.create_default_context()
#         try:
#             with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#                 server.login(sender_email, password)  # Use App Password
#                 server.sendmail(sender_email, receiver_email, message.as_string())
#             print(request.json)
            
#             # MongoDB logging
#             myclient = pymongo.MongoClient("mongodb+srv://ronilcoder999:wfO4LmraAjvrqDMG@mailtrack.chu56.mongodb.net/?retryWrites=true&w=majority&appName=Mailtrack")
#             mydb = myclient["Mailtrack"]
#             mycol = mydb["Emailtrack"]
#             mydict = {"sender": sender_email, "receiver": receiver_email, "filename": filename, "opened": []}
#             x = mycol.insert_one(mydict)
            
#             return jsonify({1: 1})
#         except smtplib.SMTPAuthenticationError as e:
#             print(f"Authentication error: {e}")
#             return jsonify({"error": "Authentication failed"}), 500
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return jsonify({"error": str(e)}), 500

#     return jsonify({1: 1})


if __name__ == "__main__":
    app.run(debug=True)