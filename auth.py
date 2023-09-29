import pyrebase

config = { "apiKey": "AIzaSyCasWhb-CbQygQ1Unv9ZDMTmCwA1mJ5yeg",
    "authDomain": "rowingapp-42cab.firebaseapp.com",
    "projectId": "rowingapp-42cab",
    "storageBucket": "rowingapp-42cab.appspcot.com",
    "messagingSenderId": "1005692947250",
    "appId": "1:1005692947250:web:2253af161d23143d1fa52b",
    "measurementId": "G-GCY3766YLS",
    "databaseURL":"" }

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


email = 'test@gmail.com'
password = '123456'

#user = auth.create_user_with_email_and_password(email,password)

#print(user)
user = auth.sign_in_with_email_and_password(email,password) # sign in
info = auth.get_account_info(user['idToken']) # get account info
#print(info)

auth.send_email_verification(user['idToken']) # send verification email

auth.send_password_reset_email(email) # reset password

