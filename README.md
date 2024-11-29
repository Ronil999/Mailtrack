# Mail Track
<div align="center">
  <img src="https://i.ibb.co/hWbdctV/mailtracker.png">
</div>

## 📖 Introduction 

- This application tracks the email, let user know whether someone opens the mail and also how many times the email has been opened.
- It works using Pixel tracking method
- Most the work is carried out in the backend. A image is generated for the user and then added in backend folder.
- This link is added in the email message and when user opens the mail a GET request is made. We also track IP address but its of the mail provider and not user.
- Then the data is added to Mongodb and whenever GET request is made current time is appended into the database and we can know when user opens the mail

## ✨ How to Contribute

The frontend part is created using react and to run it we need to run npm i and npm start command
This will open the react app
Now to run the backend which is created using flask we need to simply run python app.py. The backend contains REST APIs which enable our react to communicate with MongoDB database.
Our current goal is to redesign the whole project and remove the form input for sending email and instead enable user to login from their email id and send emails just like we do in All in one mail apps which are pre-installed on our devices.

### Steps to Contribute
- 1. Fork this repo and clone it on your local machine 
- 2. Next create a new branch stating issue number and switch to it
- 3. Make changes and commit changes
- 4. Push to remote

## 💻 Languages and Frameworks
- Python
- Javascript
- React
- Flask
- Auth0
- MongoDB Atlas

## Licenses
[MIT LICENSE](LICENSE)
