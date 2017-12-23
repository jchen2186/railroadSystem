import mysql.connector as mariadb
import datetime

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
    res_avail = check_avail(int(station_from), int(station_to), date)
    if(res_avail):
        print("Trains: ", res_avail)
    else:
        print("None available")
        return False
    # Check Fare
    total_fare = check_fare(int(station_from), int(station_to))
    # Check Type
    cursor.execute("Select fare_rate from fare_types where fare_type = %s", (type.lower(),))
    for curs in cursor:
        rate = float(curs[0])
    print("The ticket would cost approximately %s" % (total_fare * rate))

def check_avail(station_from, station_to, res_date):
    # TODO: make a check function here
    trains = []
    segments = []
    if station_from > station_to:
        direction = 1
    else:
        direction = 0
    cursor.execute("Select train_id from trains where train_direction = %s", (direction,))
    for id in cursor:
        trains += id
    print("Trains: ",  trains) # Show trains going in the same direction
    if direction == 0: #0 is station_from to station_to
        for i in range(station_from, station_to):
            cursor.execute("Select segment_id from segments where seg_n_end = %s and seg_s_end = %s", (i, i+1,))
            for j in cursor:
                segments += j
    else:   #1 is station_to to station_from
        for i in range(station_to, station_from):
            cursor.execute("Select segment_id from segments where seg_n_end = %s and seg_s_end = %s", (i, i+1,))
            for j in cursor:
                segments += j

    print("Segments: ", segments)

    for z in cursor:
        print(z)
    avail_list = {}
    for t_id in trains:
        avail_list[t_id] = True
        for seg_id in segments:
            cursor.execute("select freeseat from seats_free where train_id = %s AND segment_id = %s AND seat_free_date = %s ",
                                                                                            (t_id, seg_id, res_date,))
            for capacity in cursor:
                if capacity == 0:
                    avail_list[t_id] = False

    print(avail_list)
    return avail_list

def check_fare(station_from, station_to):
    # TODO: Check the fare and return value
    print("TODO: Check Fare")
    return 1

print("~Reservation~")
inp_email = input("Email: ")
inp_from = input("Source Station(1-25): ")
inp_to = input("Destination(1-25): ")
inp_date = input("Date of Trip (YYYY-MM-DD): ")
print("Fare Types:\t\tAdult\tChild\tSenior\tMilitary\tPets\n")
inp_type = input("What type of ticket are you buying today? ")
makereservation(inp_email, inp_from, inp_to, inp_date, inp_type)