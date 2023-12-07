import psycopg2
from config import db_params
import datetime
from decimal import Decimal

# Create connection to database
def connect_database():
    conn = psycopg2.connect(**db_params)
    return conn

# Method that displays the login menu
def login_menu(conn):
    client_id = -1
    while client_id == -1:
        choice = input("Enter '1' to login or '0' to register a new account: ")
        
        if choice == '1':
            client_id = client_login(conn)
        elif choice == '0':
            register_new_client(conn)
        else:
            print("Invalid choice. Please enter '1' to login or '0' to register.")
    return client_id

# Method that logs in the client (returns client_id or -1)
def client_login(conn):
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    try:
        cur = conn.cursor()
        cur.execute("SELECT client_id FROM client WHERE email = %s AND password = %s", (email, password))
        client = cur.fetchone()
        cur.close()

        if client:
            print("Login successful!")
            return client[0]
        else:
            print("Login failed. Incorrect email or password.")
            return -1
    except Exception as e:
        conn.rollback()
        print("An error occurred during login:", e)
        return -1

# Method that registers a new client
def register_new_client(conn):
    first_name = input("First name: ")
    last_name = input("Last name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO client (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", 
                    (first_name, last_name, email, password))
        conn.commit()
        cur.close()
        
        print("Registration successful.")
    except Exception as e:
        conn.rollback()
        print("An error occurred during registration:", e)

def generate_match_score(conn, budget, weather_preference, travel_start_date, travel_end_date, destination_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT average_cost, average_weather, best_travel_time FROM destination WHERE destination_id = %s", (destination_id,))
        destination = cur.fetchone()
        cur.close()
        if not destination:
            print("Destination not found.")
            return None
        destination_avg_cost, destination_weather, destination_best_time = destination

        # Compute budget_match
        budget_match = max(0, 1 - abs(float(str(destination_avg_cost)) - budget) / float(str(destination_avg_cost)))
        
        # Compute weather_match
        weather_values = {
            'Freezing': 0,
            'Cold': 1,
            'Cool': 2,
            'Mild': 3,
            'Warm': 4,
            'Hot': 5,
            'Very Hot': 6
        }
        weather_match = max(0, 1 - abs(weather_values[weather_preference] - weather_values[destination_weather]) / len(weather_values))

        # Calculate date_match
        month_to_int = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        best_months = set(month_to_int[month.strip()] for month in destination_best_time.split(','))

        user_months = set()
        current_date = travel_start_date
        while current_date <= travel_end_date:
            user_months.add(current_date.month)
            current_date += datetime.timedelta(days=1)
        
        overlap = user_months.intersection(best_months)
        if user_months:
            date_match = len(overlap) / len(user_months)
        else:
            date_match = 0

        # Combine matches into a final score
        # Example: Weighted sum of matches (adjust weights as needed)
        final_score = (budget_match * 0.4 + weather_match * 0.3 + date_match * 0.3) * 100

        return Decimal(str(final_score))
    except Exception as e:
        print("An error occurred:", e)
        return None

def generate_suggestions(conn, questionnaire_id, budget, weather_preference, travel_start_date, travel_end_date):
    try:
        cur = conn.cursor()

        # Retrieve all necessary information for each destination from the database
        cur.execute("SELECT destination_id, name, average_cost, best_travel_time, average_weather FROM destination")
        destinations = cur.fetchall()

        # Calculate match scores for each destination
        scores = []
        for dest in destinations:
            dest_id, dest_name, avg_cost, best_travel_time, avg_weather = dest
            score = generate_match_score(conn, budget, weather_preference, travel_start_date, travel_end_date, dest_id)
            scores.append((dest, score))  # Store the entire destination record with the score

        # Sort destinations by their match scores, descending
        top_destinations = sorted(scores, key=lambda x: x[1], reverse=True)[:3]

        # Display top 3 destinations with all their details
        print("Top 3 Destination Suggestions:")
        for dest, score in top_destinations:
            dest_id, dest_name, avg_cost, best_travel_time, avg_weather = dest
            rounded_score = round(score)  # Round the score to the nearest integer
            print(f"Destination ID: {dest_id}, Name: {dest_name}, Average Cost: {avg_cost}, "
                  f"Best Travel Time: {best_travel_time}, Average Weather: {avg_weather}, "
                  f"Match Score: {rounded_score}%")  # Display score as a percentage

        # Save suggestions to the database
        for dest, score in top_destinations:
            dest_id = dest[0]  # The first element is the destination_id
            cur.execute("INSERT INTO suggestion (questionnaire_id, destination_id, match_score) VALUES (%s, %s, %s)", 
                        (questionnaire_id, dest_id, score))
        conn.commit()
        cur.close()
    except Exception as e:
        conn.rollback()
        print("An error occurred while generating suggestions:", e)

def fill_questionnaire(conn, client_id):
    # Get the start date
    while True:
        start_date_str = input("Enter the desired start date of your travel (mm-dd-yyyy): ")

        try:
            travel_start_date = datetime.datetime.strptime(start_date_str, '%m-%d-%Y')
            break
        except ValueError:
            print("Invalid date format. Please enter the date in mm-dd-yyyy format.")

    # Get the end date 
    while True:
        end_date_str = input("Enter the desired end date of your travel (mm-dd-yyyy): ")
        try:
            travel_end_date = datetime.datetime.strptime(end_date_str, '%m-%d-%Y')
            if travel_end_date > travel_start_date:
                break
            else:
                print("The end date must be after the start date.")
        except ValueError:
            print("Invalid date format. Please enter the date in mm-dd-yyyy format.")

    # Get the weather preference
    weather_preferences = {
        '1': 'Freezing',
        '2': 'Cold',
        '3': 'Cool',
        '4': 'Mild',
        '5': 'Warm',
        '6': 'Hot',
        '7': 'Very Hot'
    }
    print("Select your weather preference:")
    for key, preference in weather_preferences.items():
        print(f"{key}. {preference}")
    while True:
        choice = input("Enter your choice (1-7): ")
        if choice in weather_preferences:
            weather_preference = weather_preferences[choice]
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")
    
    # Get the budget
    while True:
        try:
            budget = float(input("Enter your budget per day for the whole trip (including flights and accommodation) in $: "))
            if budget >= 0:
                break
            else:
                print("Invalid input. Please enter a positive number for the budget.")
        except ValueError:
            print("Invalid input. Please enter a numerical value.")

    # Add Questionnaire entry to database
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO questionnaire (client_id, budget, weather_preference, travel_start_date, travel_end_date) VALUES (%s, %s, %s, %s, %s)", (client_id, budget, weather_preference, travel_start_date, travel_end_date))
        conn.commit()
        cur.close()
        print("Questionnaire response saved successfully.")

        cur = conn.cursor()
        cur.execute("SELECT MAX(questionnaire_id) FROM questionnaire")
        questionnaire_id = cur.fetchone()[0]
        cur.close()
        
        generate_suggestions(conn, questionnaire_id, budget, weather_preference, travel_start_date, travel_end_date)
    except Exception as e:
        conn.rollback()
        print("An error occurred while saving the questionnaire response:", e)

def saved_recommendations(conn, client_id):
    try:
        cur = conn.cursor()

        # SQL query to retrieve suggestions, questionnaire info, and destination info
        cur.execute("""
            SELECT d.name, d.average_cost, d.average_weather, d.best_travel_time, 
                   q.travel_start_date, q.travel_end_date, s.match_score
            FROM suggestion s
            JOIN questionnaire q ON s.questionnaire_id = q.questionnaire_id
            JOIN destination d ON s.destination_id = d.destination_id
            WHERE q.client_id = %s
            ORDER BY s.match_score DESC
        """, (client_id,))

        suggestions = cur.fetchall()
        cur.close()

        if suggestions:
            print("\nYour Saved Recommendations:")
            for suggestion in suggestions:
                name, avg_cost, avg_weather, best_time, start_date, end_date, score = suggestion
                print(f"Destination: {name}; Average Cost: ${avg_cost}/day; Weather: {avg_weather}; Best Time: {best_time}; "
                      f"Travel Dates: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}; "
                      f"Match Score: {round(score)}%")
        else:
            print("No recommendations saved.")

    except Exception as e:
        print("An error occurred while retrieving recommendations:", e)

# Method that implements the main menu interaction (returns True on exit)
def main_menu(conn, client_id):
    print("\nMain Menu:")
    print("1. Fill Questionnaire to get travel recommendations")
    print("2. See your saved recommendations")
    print("3. Exit App")

    choice = input("\nEnter the number of the desired option: ")

    if choice == '1':
        fill_questionnaire(conn, client_id)
    if choice == '2':
        saved_recommendations(conn, client_id)
    if choice == '3':
        return True  

    return False


# The whole app runs in this method
def main_app():
    try:
        conn = connect_database()

        # Prompt user to login
        client_id = login_menu(conn)

        # Now that user is logged in, display main menu as long as the user didn't exit the app
        exited = False
        while not exited:
            exited = main_menu(conn, client_id)

        conn.close()
    except Exception as e:
        print("An error occurred:", e)

if __name__ == '__main__':
    main_app()