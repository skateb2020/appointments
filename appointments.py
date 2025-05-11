'''
My final project for CS50 Python is Appointments with Dr. Strange.
'''
import sys
import re
import datetime
import csv
import os

def main():
    #checks for command-line arguments
    try:
        validate_command_line(sys.argv[1])
    except IndexError:
        sys.exit("Need a valid command.")

    if len(sys.argv) != 2:
        sys.exit("Invalid.")
    #if command line-argument is create_appointment, proceed with getting the information from the user
    elif validate_command_line:

        #asks the user if he wants to create an appointment until he responds with yes of no
        while True:
             #deletes old appointments and stores it in another csv file
            temp_file = delete_data()
            os.replace(temp_file, "appointments.csv")

            make_appointment = appointment(input("Would you like to create an appointment with Dr. Stange? ").strip())
            if make_appointment is False:
                break

        #list of dictionaries that includes personal questions, regex, and a spot for the answers
        information = [
            {"prompt": "What is your first name? ", "regex": r"^[a-z]+$", "answer":""},
            {"prompt": "What is your last name? ", "regex": r"^[a-z]+$", "answer": ""},
            {"prompt": "What is your phone number? ", "regex": r"^\d{3}-?\d{3}-?\d{4}$", "answer": ""},
            {"prompt": "What is your street address? ", "regex": r"^\d{1,5} [a-z \.#]{3,} [a-z\.]{2,}$", "answer": ""},
            {"prompt": "What city do you live in? ", "regex": r"^[a-z ]{3,}$", "answer": ""},
            {"prompt": "What state do you live in? ", "regex": r"^[a-z]{3,13} ?(?:of )?(?:[a-z]{4,9})?$", "answer": ""},
            {"prompt": "What is your zip code? ", "regex": r"^\d{5}$", "answer": ""}
        ]

        #loops through the list and gets answers for every prompt only if the prompt matches the regex (otherwise, reprompts)
        for i in range(len(information)):
            while True:
                answer = input(information[i]["prompt"]).strip()
                answer = validate(answer, information[i]["regex"])
                if answer != False:
                    break
            information[i]["answer"] = answer

        #gets the birthday from user
        while True:
            dob = validate(input("What is your date of birth? ").strip(), r"^[01]?[0-9]/[0-3]?[0-9]/[12][09][0-9][0-9]?$")
            if dob != False:
                dob = birthdate(dob)
                if dob != False:
                    break

        #gets appointment date and time from the user
        app_date = get_date()
        time = get_time()
        existing_appointments(app_date, time)

        add_data(information[0]["answer"], information[1]["answer"], dob, app_date, time, information[2]["answer"], information[3]["answer"], information[4]["answer"], information[5]["answer"], information[6]["answer"])

        #print the user's confimation
        print(f'{information[0]["answer"]} {information[1]["answer"]}, Dr. Strange looks forward to seeing you on {app_date} at {time}. \nPlease ensure that the following information is correct and let the office know if anything is incorrect before {app_date}:\nBirthdate: {dob}\nPhone Number:{information[2]["answer"]}\nAddress: {information[3]["answer"]} {information[4]["answer"]}, {information[5]["answer"]} {information[6]["answer"]}\nDr. Strange looks forward to seeing you soon!')

def validate_command_line(second):
    '''
    Responds with an appropriate message depending on what the user types into the command-line.
    '''
    if second == "-h" or second == "--help":
        sys.exit("Use the command 'create_appointment' to create a new doctor's appointment with Dr. Strange.")
    elif second == "create_appointment":
        return True
    else:
        sys.exit("Need a valid command.")

def appointment(answer):
    '''
    Prompts the user for if he wants to make an appointment until valid input is received.
    '''
    try:
        answer = str(answer).lower()
    except ValueError:
        return True
    if answer == "yes":
        return False
    elif answer == "no":
        sys.exit("Come back when you want to create an appointment.")
    else:
        return True

def validate(input, regex):
    if re.search(regex, input, re.IGNORECASE):
        return input.title()
    else:
        return False

def birthdate(date):
    '''
    Returns False if the date is before 1901 or in the future.
    Otherwise, returns date.
    '''
    try:
        birthday = datetime.datetime.strptime(date, '%m/%d/%Y')
    except ValueError:
        return False
    else:
        too_old = datetime.datetime.strptime("12/31/1900", '%m/%d/%Y')
        today = datetime.datetime.today()
        if too_old >= birthday or birthday > today:
            return False
        else:
            return date

def appointment_date(date):
    '''
    Checks if a given day has passed, is on a weekday, or is in the future.
    '''
    try:
        appointed_day = datetime.datetime.strptime(date, '%m/%d/%Y')
    except ValueError:
        sys.exit("Error")
    else:
        if appointed_day <= datetime.datetime.today():
            return "Appointment date has already passed."
        elif appointed_day.isoweekday() > 5:
            return "Needs to be on a weekday."
        else:
            return date

def get_date():
    '''
    Gets the day the user wants to make the appointment.
    '''
    while True:
        date = validate(input("On what day would you like to schedule your appointment? ").strip(), r"^[01]?[0-9]/[0-3]?[0-9]/[12][09][0-9][0-9]?$")
        if date != False:
            date = appointment_date(date)
            if "/" in date:
                return date
            else:
                print(date)
    pass

def get_time():
    '''
    Gets the time the user wants to make the appointment.
    '''
    while True:
        time = validate(input("What time would you like to schedule your appointment? ").strip(), r"^1?[012349] [ap]\.?m\.?$")
        if time != False:
            time = time_validator(time)
            if time != False:
                return time

def existing_appointments(date, time):
    '''
    Reads the csv file and adds the rows apppointment_date and appointment_time to a dictionary.
    If the arguments date and time are both already in the dictionary, reruns functions get_date(), get_time(), and existing_appointments().
    '''

    appointments = []

    with open("appointments.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            appointments.append({"appointment_date": row["appointment_date"], "appointment_time": row["appointment_time"]})

        for app in appointments:
            if app["appointment_date"] == date and app["appointment_time"] == time:
                print("Appointment already taken.")
                app_date = get_date()
                app_time = get_time()
                existing_appointments(app_date, app_time)

def time_validator(time):
    '''
    Checks if a given time is in the list of valid times.
    Valid times: 9 am, 10 am, 11 am, 1 pm, 2 pm, 3 pm, 4 pm
    '''
    try:
        hour, meridian = time.split(" ")
        meridian = meridian.replace(".", "")
    except ValueError:
        sys.exit("Invalid")
    else:
        if meridian.lower() == "am":
            morning = ["9", "10", "11"]
            if hour in morning:
                return time.lower().replace(".", "")
            else:
                return False
        elif meridian.lower() == "pm":
            afternoon = ["1", "2", "3", "4"]
            if hour in afternoon:
                return time.lower().replace(".", "")
            else:
                return False
        else:
            sys.exit("Invalid")

def add_data(first, last, dob, date, time, phone, street, city, state, zip):
    '''
    Opens the csv file appointments.csv and writes all the arguments of this function to a row in the form of a dictionary.
    '''
    with open("appointments.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["first_name", "last_name", "dob", "appointment_date", "appointment_time", "phone_number", "street_address", "city", "state", "zip"])
        writer.writerow({"first_name": first, "last_name": last, "dob": dob, "appointment_date": date, "appointment_time": time, "phone_number": phone, "street_address": street, "city": city, "state": state, "zip": zip})

def delete_data():
    '''
    If the date of the appointment has passed, stores the appointment in past_appointments.csv and deletes it from appointments.csv
    '''
    temp_file = "temp.csv"
    fieldnames=["first_name", "last_name", "dob", "appointment_date", "appointment_time", "phone_number", "street_address", "city", "state", "zip"]

    with open("appointments.csv", "r", newline="") as curr_file, open("past_appointments.csv", "a", newline="") as deletedfile, open(temp_file, "w", newline="") as tempfile:
        reader = csv.DictReader(curr_file)
        deleted_writer = csv.DictWriter(deletedfile, fieldnames)
        writer = csv.DictWriter(tempfile, fieldnames)

        writer.writeheader()

        today = datetime.datetime.today()

        for row in reader:
            date = datetime.datetime.strptime(row["appointment_date"], "%m/%d/%Y")
            if date < today:
                deleted_writer.writerow(row)
            else:
                writer.writerow(row)

    return temp_file




if __name__ == "__main__":
    main()