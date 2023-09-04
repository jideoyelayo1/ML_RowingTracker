from flask import Flask,session,redirect,url_for,request,render_template
import pyrebase
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split 



app = Flask(__name__)

config = { """
INSERT CONFIG DETAILS
""" }

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app.secret_key = 'secretkey'

improvement_percentage = 2.5
improvement_coeff = 1 + improvement_percentage/100


@app.route('/',methods=['GET','POST'])
def index():  
    if'user' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            session['user'] = email
            return redirect('/')
        except:
            return "Failed to login"
        
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user_with_email_and_password(email,password)

            return redirect('/')
        except Exception as err:
            if "EMAIL_EXISTS" in str(err):
                return "EMAIL EXISTS"
            return "Failed to create account"
    return render_template('signup.html')

@app.route('/reset',methods=['GET','POST'])
def reset():
    if request.method == 'POST':
        email = request.form['email']
        try:
            auth.send_password_reset_email(email)
            return redirect('/')
        except:
            return "Failed to reset password"
    return render_template('forgot.html')

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/add-split',methods=['GET','POST'])
def add_split():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        distance = request.form['distance']

        data = {
            "User":session['user'], 
            "date":date,
            "time":time,
            "distance":distance
        }
        try:
            db.child("splits").push(data)
            return redirect('/add-split')
        except Exception as e:
            print(e)
            return "Failed to add split"
    
    return render_template('addsplit.html')

@app.route('/splits',methods=['GET'])
def splits():
    try:
        user_email = session['user'] 
        
        all_splits_response = db.child("splits").get()
        all_splits_data = all_splits_response.val()

        user_splits = []  
        

        for split_id, split_data in all_splits_data.items():
            if split_data.get('User') == user_email:  
                user_splits.append({
                    'id': split_id,
                    'date': split_data['date'],
                    'distance': split_data['distance'],
                    'time': split_data['time']
                })
        if user_splits == []:
            return render_template('nosplits.html')
    except:
        return render_template('nosplits.html')

    return render_template('allsplits.html',splits=user_splits)

@app.route('/edit-split/<entry_id>', methods=['GET', 'POST'])
def edit_split(entry_id):
    if request.method == 'GET':

        split_data = db.child("splits").child(entry_id).get().val()


        return render_template('edit_split.html', entry_id=entry_id, date=split_data['date'], distance=split_data['distance'], time=split_data['time'])
    
    elif request.method == 'POST':

        date = request.form['date']
        time = request.form['time']
        distance = request.form['distance']


        db.child("splits").child(entry_id).update({"date": date, "time": time, "distance": distance})

        return redirect('/splits')


@app.route('/delete-split/<entry_id>', methods=['GET'])
def delete_split(entry_id):
    try:
        db.child("splits").child(entry_id).remove()
        return redirect('/splits')
    except Exception as e:
        print(e)
        return str(e)




@app.route('/view-graphs',methods=['GET','POST'])
def view_splits():
    try:
        user_email = session['user']  
        all_splits_response = db.child("splits").get()
        all_splits_data = all_splits_response.val()

        user_splits = []  

        for split_id, split_data in all_splits_data.items():
            if split_data.get('User') == user_email:  
                user_splits.append({
                    'id': split_id,
                    'date': split_data['date'],
                    'distance': split_data['distance'],
                    'time': split_data['time']
                })
        if user_splits == []:
            return render_template('nosplits.html')
    except:
        return render_template('nosplits.html')
    

    return render_template('allgraphs.html',splits=user_splits)



@app.route('/total-distance-vs-date')
def total_distance_vs_date():
    try:
        user_email = session['user']
        all_splits_response = db.child("splits").get()
        all_splits_data = all_splits_response.val()

        user_splits = []

        for split_id, split_data in all_splits_data.items():
            if split_data.get('User') == user_email:
                user_splits.append({
                    'id': split_id,
                    'date': split_data['date'],
                    'distance': split_data['distance'],
                    'time': split_data['time']
                })

        if user_splits == []:
            return render_template('nosplits.html')
    except:
        return render_template('nosplits.html')


    for split in user_splits:
        split['distance'] = int(split['distance'])


    user_splits.sort(key=lambda x: x['date'])


    dates = [split['date'] for split in user_splits]
    total_distances = [split['distance'] for split in user_splits]


    plt.figure(figsize=(10, 6))
    plt.plot(dates, total_distances, marker='o', linestyle='-')
    plt.title('Total Distance vs. Date')
    plt.xlabel('Date')
    plt.ylabel('Total Distance (meters)')
    plt.xticks(rotation=45)
    plt.grid(True)



    plt.savefig('static/total_distance_vs_date.png') 


    return render_template('total_distance_vs_date.html', plot_image='static/total_distance_vs_date.png')





@app.route('/average-speed-vs-date')
def average_speed_vs_date():
    try:
        user_email = session['user']
        all_splits_response = db.child("splits").get()
        all_splits_data = all_splits_response.val()

        user_splits = []

        for split_id, split_data in all_splits_data.items():
            if split_data.get('User') == user_email:
                user_splits.append({
                    'id': split_id,
                    'date': split_data['date'],
                    'distance': split_data['distance'],
                    'time': split_data['time']
                })
        
        if user_splits == []:
            return render_template('nosplits.html')
    except:
        return render_template('nosplits.html')


    date_vs_average_speed = {}
    for split in user_splits:
        date = split['date']
        distance = split['distance']
        time = split['time']
       

        time_parts = time.split(':')
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        total_minutes = hours * 60 + minutes
        

        speed = int(distance) / (total_minutes * 60)
        
        if date in date_vs_average_speed:
            date_vs_average_speed[date].append(speed)
        else:
            date_vs_average_speed[date] = [speed]


    dates = []
    average_speeds = []
    for date, speeds in date_vs_average_speed.items():
        dates.append(date)
        average_speeds.append(sum(speeds) / len(speeds))


    plt.figure(figsize=(10, 6))
    plt.plot(dates, average_speeds, marker='o', linestyle='-')
    plt.title('Average Speed vs. Date')
    plt.xlabel('Date')
    plt.ylabel('Average Speed (m/s)')
    plt.xticks(rotation=45)
    plt.grid(True)



    plt.savefig('static/average_speed_vs_date.png')  


    return render_template('average_speed_vs_date.html', plot_image='static/average_speed_vs_date.png')






@app.route('/average-split-time-vs-date')
def average_split_time_vs_date():
    try:
        user_email = session['user']
        all_splits_response = db.child("splits").get()
        all_splits_data = all_splits_response.val()

        user_splits = []

        for split_id, split_data in all_splits_data.items():
            if split_data.get('User') == user_email:
                user_splits.append({
                    'id': split_id,
                    'date': split_data['date'],
                    'distance': split_data['distance'],
                    'time': split_data['time']
                })
        
        if not user_splits:
            return render_template('nosplits.html')
    except:
        return render_template('nosplits.html')


    date_vs_average_split_time = {}
    date_vs_count = {}
    
    for split in user_splits:
        date = split['date']
        time_str = split['time']
        

        try:
            time_parts = time_str.split(':')
            if len(time_parts) != 2:
                raise ValueError("Invalid time format")
            

            total_minutes = int(time_parts[0]) * 60 + int(time_parts[1])
            
            if date in date_vs_average_split_time:
                date_vs_average_split_time[date] += total_minutes
                date_vs_count[date] += 1
            else:
                date_vs_average_split_time[date] = total_minutes
                date_vs_count[date] = 1
        except ValueError as e:

            print(f"Error processing time: {e}")


    dates = sorted(list(date_vs_average_split_time.keys()))  
    average_split_times = []
    
    for date in dates:
        total_time = date_vs_average_split_time[date]
        count = date_vs_count[date]
        
        if count == 0:
            average_minutes = 0  
        else:
            average_minutes = total_time / count
        
        average_split_times.append(int(average_minutes)) 
        


    plt.figure(figsize=(10, 6))
    plt.plot(dates, average_split_times, marker='o', linestyle='-')
    plt.title('Average Split Time vs. Date')
    plt.xlabel('Date')
    plt.ylabel('Average Split Time (Minutes)') 
    plt.xticks(rotation=45)
    plt.grid(True)


    plt.savefig('static/average_split_time_vs_date.png')  


    return render_template('average_split_time_vs_date.html', plot_image='static/average_split_time_vs_date.png')




@app.route('/average-distance-and-speed-vs-date')
def average_distance_and_speed_vs_date():
    try:
        user_email = session['user']
        all_splits_response = db.child("splits").get()
        all_splits_data = all_splits_response.val()

        user_splits = []

        for split_id, split_data in all_splits_data.items():
            if split_data.get('User') == user_email:
                user_splits.append({
                    'id': split_id,
                    'date': split_data['date'],
                    'distance': split_data['distance'],
                    'time': split_data['time']
                })
        
        if not user_splits:
            return render_template('nosplits.html')
    except:
        return render_template('nosplits.html')


    user_splits.sort(key=lambda x: x['date'])


    sessions = [] 
    current_session_date = None
    current_session_distance = 0
    current_session_speed = 0
    
    for split in user_splits:
        date = split['date']
        distance = int(split['distance'])
        time_str = split['time']
        

        try:
            time_parts = time_str.split(':')
            if len(time_parts) != 2:
                raise ValueError("Invalid time format")
            

            total_minutes = int(time_parts[0]) * 60 + int(time_parts[1])
            

            speed = distance / (total_minutes / 60)
            
            if date != current_session_date:
                if current_session_date is not None:
                    sessions.append({
                        'date': current_session_date,
                        'distance': current_session_distance,
                        'speed': current_session_speed
                    })
                current_session_date = date
                current_session_distance = distance
                current_session_speed = speed
            else:
                current_session_distance += distance
                current_session_speed += speed
        except ValueError as e:

            print(f"Error processing time: {e}")
    

    if len(sessions) < 2:
        return render_template('notenoughsessions.html')

    session_dates = [session['date'] for session in sessions]
    session_distances = [session['distance'] for session in sessions]
    session_speeds = [session['speed'] for session in sessions]

    percentage_change_distance = [0]  
    percentage_change_speed = [0] 

    for i in range(1, len(sessions)):
        percentage_change_distance.append(((session_distances[i] - session_distances[i - 1]) / session_distances[i - 1]) * 100)
        percentage_change_speed.append(((session_speeds[i] - session_speeds[i - 1]) / session_speeds[i - 1]) * 100)


    plt.figure(figsize=(10, 6))
    plt.plot(session_dates, percentage_change_distance, marker='o', linestyle='-', label='Percentage Change in Distance')
    plt.plot(session_dates, percentage_change_speed, marker='o', linestyle='-', label='Percentage Change in Speed')
    plt.title('Percentage Change in Average Distance and Speed vs. Session Date')
    plt.xlabel('Session Date')
    plt.ylabel('Percentage Change (%)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend() 


    plt.savefig('static/percentage_change_distance_and_speed_vs_date.png')  


    return render_template('percentage_change_distance_and_speed_vs_date.html', plot_image='static/percentage_change_distance_and_speed_vs_date.png')


@app.route('/predict_speed')
def predict_speed():
    try:
        rmse,current_speed = ml_average_speed_vs_date(session['user'])

        if rmse == None or current_speed == None:
            return render_template('needmoresessions.html')
        str_rmse = str(rmse*100)[:5]
        str_current_speed = str(current_speed)[:5]
        str_target = str(current_speed*improvement_coeff)[:5]
    except Exception as e:
        print(e)
        return render_template('needmoresessions.html')
    return render_template('predict_speed.html',rmse=str_rmse,speed=str_current_speed,target=str_target,percent_push = improvement_percentage)






def ml_average_speed_vs_date(user_email):
    try:
        all_splits_response = db.child("splits").get()
        all_splits_data = all_splits_response.val()

        user_splits = []

        for split_id, split_data in all_splits_data.items():
            if split_data.get('User') == user_email:
                user_splits.append({
                    'id': split_id,
                    'date': split_data['date'],
                    'distance': split_data['distance'],
                    'time': split_data['time']
                })

        if not user_splits:
            return None, None
    except:
        return None, None
    
    
    dates, average_speeds = get_speed_and_data(user_splits)

    df = pd.DataFrame({'Date': dates, 'AverageSpeed': average_speeds})
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    df['Date'] = df['Date'].apply(lambda x: x.timestamp())
    
    df.sort_values(by='Date', inplace=True)
    
    X = df[['Date']] 
    y = df['AverageSpeed']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    current_date = datetime.now().timestamp()
    
    current_speed = model.predict([[current_date]])[0]
    
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)


    return rmse, current_speed






def get_speed_and_data(user_splits):
    date_vs_average_speed = {}
    for split in user_splits:
        date = split['date']
        distance = split['distance']
        time = split['time']
        time_parts = time.split(':')
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        total_minutes = hours * 60 + minutes
        
        speed = int(distance) / (total_minutes * 60)
        
        if date in date_vs_average_speed:
            date_vs_average_speed[date].append(speed)
        else:
            date_vs_average_speed[date] = [speed]

    dates = []
    average_speeds = []
    for date, speeds in date_vs_average_speed.items():
        dates.append(date)
        average_speeds.append(sum(speeds) / len(speeds))

    return dates,average_speeds





@app.route('/pred-average-speed-vs-date')
def pred_average_speed_vs_date():
    try:
        user_email = session['user']
        all_splits_response = db.child("splits").get()
        all_splits_data = all_splits_response.val()

        user_splits = []

        for split_id, split_data in all_splits_data.items():
            if split_data.get('User') == user_email:
                user_splits.append({
                    'id': split_id,
                    'date': split_data['date'],
                    'distance': split_data['distance'],
                    'time': split_data['time']
                })
        
        if user_splits == []:
            return render_template('nosplits.html')
    except:
        return render_template('nosplits.html')

    date_vs_average_speed = {}
    for split in user_splits:
        date = split['date']
        distance = split['distance']
        time = split['time']
        time_parts = time.split(':')
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        total_minutes = hours * 60 + minutes
        speed = int(distance) / (total_minutes * 60)
        
        if date in date_vs_average_speed:
            date_vs_average_speed[date].append(speed)
        else:
            date_vs_average_speed[date] = [speed]

    dates = []
    average_speeds = []
    for date, speeds in date_vs_average_speed.items():
        dates.append(date)
        average_speeds.append(sum(speeds) / len(speeds))

    df = pd.DataFrame({'Date': dates, 'AverageSpeed': average_speeds})
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    df['Date'] = df['Date'].apply(lambda x: x.timestamp())
    
    df.sort_values(by='Date', inplace=True)
    
    X = df[['Date']]  
    y = df['AverageSpeed']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    predicted_speeds = model.predict(X)
    



    plt.figure(figsize=(10, 6))
    plt.plot(dates, average_speeds, label='Actual', marker='o', linestyle='-')
    plt.plot(dates, predicted_speeds, label='Predicted', marker='x', linestyle='--')
    plt.title('Average Speed vs. Date')
    plt.xlabel('Date')
    plt.ylabel('Average Speed (m/s)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    plt.savefig('static/predicted_average_speed_vs_date.png')

    return render_template('predicted_average_speed_vs_date.html', plot_image='static/predicted_average_speed_vs_date.png')






if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host="0.0.0.0",port=5000,debug=False)
