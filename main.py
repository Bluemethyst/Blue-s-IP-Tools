import requests, time, sqlite3, colorama, socket
from datetime import datetime
from prettytable import PrettyTable

colorama.init(autoreset=True)

intro_text = """
______ _            _       ___________   _____           _     
| ___ \ |          ( )     |_   _| ___ \ |_   _|         | |    
| |_/ / |_   _  ___|/ ___    | | | |_/ /   | | ___   ___ | |___ 
| ___ \ | | | |/ _ \ / __|   | | |  __/    | |/ _ \ / _ \| / __|
| |_/ / | |_| |  __/ \__ \  _| |_| |       | | (_) | (_) | \__ \ 
\____/|_|\__,_|\___| |___/  \___/\_|       \_/\___/ \___/|_|___/

"""

def get_ip_address(): # for checking users ip at startup
    r = requests.get('https://api.ipify.org?format=json')
    data = r.json()
    return data['ip']

def convert_unix_to_normal(unix_time):
    # Convert the Unix time to a datetime object
    normal_time = datetime.fromtimestamp(int(unix_time))
    return normal_time

def help_menu(): # print the help menu
        print('\u001b[38;5;202m' + f"-------------------HELP MENU-------------------")
        print('\u001b[38;5;249m' + f"--help:            this menu")
        print('\u001b[38;5;249m' + f"--removeip <ip>:   removes input IP from database,")
        print('\u001b[38;5;249m' + f"                   use --removeip all to clear database")
        print('\u001b[38;5;249m' + f"--db:              view the full database")
        print('\u001b[38;5;249m' + f"--quit:            exit the program")
        print('\u001b[38;5;202m' + f"-----------------------------------------------")
        print('\u001b[38;5;240m' + f"Report any issues at https://github.com/Bluemethyst")
        
        
def get_ip_address_from_url(domain):
    input_url = domain.split('://')[-1].split('/')[0]
    ip_address = socket.gethostbyname(input_url)
    ip_lookup(ip_address)


def display_db():
    conn = sqlite3.connect('ip_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ip_data")
    rows = c.fetchall()
    print('\u001b[38;5;202m'+f"--------------------DATABASE--------------------")
        # Define the table
    table = PrettyTable(["IP", "Country", "Region", "City", "Zipcode", "Continent", "Timezone", "Proxy", "Latitude", "Longitude", "Request Time"])

    # Add rows
    for row in rows:
        table.add_row(row)
    print(table)
    print('\u001b[38;5;202m'+f"------------------------------------------------")
    conn.close()
        
def removeip(ip): # remove ip from database
    conn = sqlite3.connect('ip_data.db')
    c = conn.cursor()

    if ip.lower() == 'all':
        c.execute("DELETE FROM ip_data")
        print('\u001b[38;5;124m' + f'All data removed from database')
    else:
        c.execute("DELETE FROM ip_data WHERE ip = ?", (ip,))
        print('\u001b[38;5;124m' + f"IP {ip} and all related data removed from database")

    conn.commit()
    conn.close()
    

def ip_lookup(ip): # start the ip lookup process
    start_time = time.time() # timer to see how long lookup took
    r = requests.get(f'https://freeipapi.com/api/json/{ip}')
    r2 = requests.get(f"http://worldtimeapi.org/api/ip/{ip}")
    end_time = time.time()
    data = r.json()
    time_data = r2.json()
    elapsed_time = end_time - start_time
    latitude = data['latitude']
    longitude = data['longitude']
    if data['ipVersion'] != '':
        print('\u001b[38;5;33m' + "IP Info: "+'\u001b[38;5;195m'+f"IPV{data['ipVersion']}, {data['ipAddress']}") # print out all the data and ask if you would like to save the the database
        print('\u001b[38;5;69m' + "Country: "+'\u001b[38;5;195m'+f"{data['countryName']}, {data['countryCode']}")
        print('\u001b[38;5;105m' + "Region/City/Zipcode: "+'\u001b[38;5;195m'+f"{data['regionName']}, {data['cityName']}, {data['zipCode']}")
        print('\u001b[38;5;141m' + "Coninent: "+'\u001b[38;5;195m'+f"{data['continent']}, {data['continentCode']}")
        print('\u001b[38;5;177m' + "Timezone: "+'\u001b[38;5;195m'+f"{data['timeZone']}")
        print('\u001b[38;5;177m' + "Local time: "+'\u001b[38;5;195m'+f"{convert_unix_to_normal(time_data['unixtime'])}")
        print('\u001b[38;5;213m' + "Using Proxy? "+'\u001b[38;5;195m'+f"{data['isProxy']}")
        print('\u001b[38;5;212m' + "Lat/Long: "+'\u001b[38;5;195m'+f"{latitude}, {longitude}")
        print('\u001b[38;5;211m' + "View on Google Maps: "+'\u001b[38;5;195m'+f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}")
        print('\u001b[38;5;240m' + f"Request took {round(elapsed_time, 2)} seconds to complete")
        add_to_db = input('\u001b[38;5;249m' +'Would you like to add this to the database? y/n ')
        if add_to_db.lower() == 'y':    # user chose to save to db
                conn = sqlite3.connect('ip_data.db')
                c = conn.cursor()
                c.execute('''
                CREATE TABLE IF NOT EXISTS ip_data (
                    ip TEXT,
                    country TEXT,
                    region TEXT,
                    city TEXT,
                    zipcode TEXT,
                    continent TEXT,
                    timezone TEXT,
                    proxy TEXT,
                    lat REAL,
                    long REAL,
                    request_time REAL
                    )
                ''')
                c.execute("SELECT ip FROM ip_data WHERE ip = ?", (data['ipAddress'],))
                if c.fetchone() is None: # checking to make sure we dont end up with duplicate db entries
                    print('\u001b[38;5;34m'+f'IP added')
                    c.execute('''
                        INSERT INTO ip_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (data['ipAddress'], data['countryName'], data['regionName'], data['cityName'], data['zipCode'], data['continent'], data['timeZone'], data['isProxy'], latitude, longitude, elapsed_time))
                else:
                    print('\u001b[38;5;210m'+f'IP already in database, skipping')
                conn.commit()
                conn.close()
    
    else:
        print('\u001b[38;5;245m'+'Not a valid IP or command')

print(intro_text)
print(f"Displaying your IP...")

ip_lookup(get_ip_address())
while True: # main loop
    first_input = input('\u001b[38;5;195m'+"Enter the IP you'd like to find results for or use --help to see commands: ")
    if first_input.lower() == '--help': # checking for command usage
        help_menu()
    elif first_input.lower().startswith('https://'):
        get_ip_address_from_url(first_input)
    elif first_input.lower().startswith('--removeip'):
        _, ip_to_remove = first_input.split()
        removeip(ip_to_remove)
    elif first_input.lower() == '--quit':
        quit()
    elif first_input.lower() == '--db':
        display_db()
    else:
        ip_lookup(first_input)