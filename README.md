# Flask Rowing App

This is a Flask web application for tracking rowing splits and analyzing rowing data. You can use this app to log your rowing splits, view your rowing history, and analyze your performance. The app also provides predictive analytics for your average rowing speed based on your historical data.

It has currently been deployed at [https://rowing-tracker.onrender.com/](https://rowing-tracker.onrender.com/)

## Table of Contents

- [Getting Started](#getting-started)
- [Features](#features)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

To get started with this Flask Rowing App, follow these steps:

1. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/jideoyelayo1/RowingTracker.git
   ```

2. Change into the project directory:

   ```shell
   cd flask-rowing-app
   ```

3. Install the required Python packages using pip:

   ```shell
   pip install -r requirements.txt
   ```

4. Set up Firebase for the database. You will need to create a Firebase project and obtain the Firebase configuration details (apiKey, authDomain, projectId, etc.). Update the `config` dictionary in the `app.py` file with your Firebase configuration.

5. Set your Flask secret key. Replace `'secretkey'` in the `app.py` file with your own secret key.

6. Run the Flask application:

   ```shell
   python app.py
   ```

7. Access the app in your web browser by visiting [http://localhost:5000/](http://localhost:5000/).
   or view my deloyed version at [https://rowing-tracker.onrender.com/](https://rowing-tracker.onrender.com/)

## Features

### 1. User Authentication

- Users can sign up for an account, log in, and log out.
- Password reset functionality is available.

### 2. Dashboard

- Users have access to a dashboard that displays their rowing data.

### 3. Logging Rowing Splits

- Users can log their rowing splits, including date, time, and distance.

### 4. Viewing Rowing Splits

- Users can view and edit their rowing splits.
- Splits are displayed in a table format.

### 5. Analyzing Rowing Data

- Users can view graphs that show:
  - Total Distance vs. Date
  - Average Speed vs. Date
  - Average Split Time vs. Date
  - Percentage Change in Average Distance and Speed vs. Session Date
  - Predicted Average Speed vs. Date

### 6. Predictive Analytics

- The app provides predictive analytics for the user's average rowing speed based on their historical data.
- Users can see their predicted average speed and set a target speed for improvement.

## Usage

1. Sign Up:

   - Create an account using your email and password.

2. Log In:

   - Log in using your registered email and password.

3. Log Out:

   - Click the "Log Out" link to log out of your account.

4. Dashboard:

   - Access your personal dashboard to view your rowing data.

5. Log Rowing Splits:

   - Click the "Add Split" link to log a new rowing split.
   - Enter the date, time, and distance for the split.

6. View Rowing Splits:

   - Click the "Splits" link to view and edit your rowing splits.

7. Analyze Rowing Data:

   - Explore the various graphs available in the app for data analysis.

8. Predictive Analytics:
   - Check your predicted average rowing speed and set a target speed for improvement.

## Screenshots

![image](https://github.com/jideoyelayo1/RowingTracker/assets/41443216/e3221661-95f7-4057-9f6d-6b74a0862d23)
![image](https://github.com/jideoyelayo1/RowingTracker/assets/41443216/9bce78ae-5aca-4442-9b79-ae40f4d14e42)
![image](https://github.com/jideoyelayo1/RowingTracker/assets/41443216/c1638a32-df6d-4d9b-ac00-818b9724f76e)



## Contributing

Contributions to this project are welcome. If you would like to contribute, please open an issue or create a pull request with your proposed changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Enjoy tracking your rowing performance with the Flask Rowing App! If you have any questions or feedback, please [contact us](mailto:jideoyelayo1@gmail.com).
