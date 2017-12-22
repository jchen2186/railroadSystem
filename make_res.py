import mysql.connector as mariadb


mariadb_connection = mariadb.connect(user='root', password='beer', database='f17336pteam6')
cursor = mariadb_connection.cursor()

# cursor.execute("select fare_type from fare_types where 1")
# for types in cursor:
#     print("Type: %s " % types)

cursor.execute("select passenger_email from passengers where 1")
emails = []
for mail in cursor:
    # print("mail: %s" % mail)
    emails += mail

print(emails)
def makereservation(email, station_from, station_to, date, type):
    # Checking Email
    if(email in emails):
        cursor.execute("Select passenger_lname, passenger_fname from passengers where passenger_email = %s", (email,))
        for lname, fname in cursor:
            pass_lname = lname
            pass_fname = fname
        print("Welcome back %s %s!"% (fname, lname))
    else:
        print("You're not in the system.")
        fname = input("First Name: ")
        lname = input("Last Name: ")
        try:
            cursor.execute("insert into passengers (passenger_fname, passenger_lname, passenger_email) VALUES (%s, %s, %s)", (fname, lname, email))
        except mariadb.Error as error:
            print("Error: %s" % error)
        mariadb_connection.commit()
        print("Your Passenger ID is %s" % cursor.lastrowid)
        mariadb_connection.close()
    # Checking Availability of Segments on certain date
    check_avail(station_from, station_to, date)
    # Check Fare
    total_fare = check_fare(station_from, station_to)
    # Check Type
    cursor.execute("Select fare_rate from fare_types where fare_type = %s", (type.lower(),))
    for curs in cursor:
        rate = float(curs[0])
    print("The ticket would cost approximately %s" % (total_fare * rate))

def check_avail(station_from, station_to, date):
    # TODO: make a check function here
    if(True): # if available on the date
        print("From %s to %s is available on %s on the train TODO:Train Number Here" % (station_from, station_to, date))
    else: # unavailable on the date
        print("Unavailable on this Date")


def check_fare(station_from, station_to):
    # TODO: Check the fare and return value
    print("TODO: Check Fare")
    return 1

print("~Reservation~")
inp_email = input("Email: ")
inp_from = input("Source Station(1-25): ")
inp_to = input("Destination(1-25): ")
inp_date = input("Date of Trip (YYYY-MM-DD): ")
print("Fare Types\n- Adult\n- Child\n- Senior\n- Military\n- Pets\n")
inp_type = input("What type of ticket are you buying today? ")
makereservation(inp_email, inp_from, inp_to, inp_date, inp_type)