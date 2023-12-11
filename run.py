import requests, time, sqlite3, colorama, socket
import customtkinter as ct
from datetime import datetime
from prettytable import PrettyTable
from PIL import Image

colorama.init(autoreset=True)


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
    if ip.startswith('https://'):
        get_ip_address_from_url(ip)
    else: 
        r = requests.get(f'https://freeipapi.com/api/json/{ip}')
        r2 = requests.get(f"http://worldtimeapi.org/api/ip/{ip}")
        end_time = time.time()
        data = r.json()
        time_data = r2.json()
        elapsed_time = end_time - start_time
        latitude = data['latitude']
        longitude = data['longitude']
        if data['ipVersion'] != '':
            print('\u001b[38;5;33m' + "IP Info: "+'\u001b[38;5;195m'+f"IPV{data['ipVersion']}, {data['ipAddress']}")
            ip_info_tb.configure(state='normal')
            ip_info_tb.delete("0.0", "end")
            ip_info_tb.insert("0.0", f"IPV{data['ipVersion']}, {data['ipAddress']}")
            ip_info_tb.configure(state='disabled')
            print('\u001b[38;5;69m' + "Country: "+'\u001b[38;5;195m'+f"{data['countryName']}, {data['countryCode']}")
            country_tb.configure(state='normal')
            country_tb.delete("0.0", "end")
            country_tb.insert("0.0", f"{data['countryName']}, {data['countryCode']}")
            country_tb.configure(state='disabled')
            print('\u001b[38;5;105m' + "Region/City/Zipcode: "+'\u001b[38;5;195m'+f"{data['regionName']}, {data['cityName']}, {data['zipCode']}")
            location_info_tb.configure(state='normal')
            location_info_tb.delete("0.0", "end")
            location_info_tb.insert("0.0", f"{data['regionName']}, {data['cityName']}, {data['zipCode']}")
            location_info_tb.configure(state='disabled')
            print('\u001b[38;5;141m' + "Coninent: "+'\u001b[38;5;195m'+f"{data['continent']}, {data['continentCode']}")
            continent_tb.configure(state='normal')
            continent_tb.delete("0.0", "end")
            continent_tb.insert("0.0", f"{data['continent']}, {data['continentCode']}")
            continent_tb.configure(state='disabled')
            print('\u001b[38;5;177m' + "Timezone: "+'\u001b[38;5;195m'+f"{data['timeZone']}")
            timezone_tb.configure(state='normal')
            timezone_tb.delete("0.0", "end")
            timezone_tb.insert("0.0", f"{data['timeZone']}")
            timezone_tb.configure(state='disabled')
            print('\u001b[38;5;177m' + "Local time: "+'\u001b[38;5;195m'+f"{convert_unix_to_normal(time_data['unixtime'])}")
            time_tb.configure(state='normal')
            time_tb.delete("0.0", "end")
            time_tb.insert("0.0", f"{convert_unix_to_normal(time_data['unixtime'])}")
            time_tb.configure(state='disabled')
            print('\u001b[38;5;213m' + "Using Proxy? "+'\u001b[38;5;195m'+f"{data['isProxy']}")
            if data['isProxy'] == True:
                proxy_cb.select()
            else:
                proxy_cb.deselect()
            proxy_cb.configure(state='disabled')
            print('\u001b[38;5;212m' + "Lat/Long: "+'\u001b[38;5;195m'+f"{latitude}, {longitude}")
            coords_tb.insert("0.0", f"{latitude}, {longitude}")
            coords_tb.configure(state='disabled')
            print('\u001b[38;5;211m' + "View on Google Maps: "+'\u001b[38;5;195m'+f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}")
            google_maps_tb.insert("0.0", f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}")
            google_maps_tb.configure(state='disabled')
            print('\u001b[38;5;240m' + f"Request took {round(elapsed_time, 2)} seconds to complete")
            request_time_tb.insert("0.0", f"{round(elapsed_time, 2)}")
            request_time_tb.configure(state='disabled')
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
        
def run_lookup():
    ip = ip_input.get()
    ip_lookup(ip)

def main():
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


ct.set_appearance_mode('dark')
ct.set_default_color_theme('dark-blue')

root = ct.CTk()
root.geometry('1280x720')
root.title("Blue's IP Tools")
root.iconbitmap('images/bluesiptools.ico')

frame = ct.CTkFrame(master=root)
frame.pack(pady=10, padx=10, fill='both', expand=True)

logo_img = ct.CTkImage(dark_image=Image.open('images/bluesiptools1.png'), size=(128,128))

logo_label = ct.CTkLabel(master=frame, text="", image=logo_img)
logo_label.pack(pady=12, padx=10, fill='both')

ip_input = ct.CTkEntry(master=frame, placeholder_text="Enter IP", height=40)
ip_input.pack(pady=12, padx=10, fill='both')

run_button = ct.CTkButton(master=frame, command=run_lookup, text="Run Lookup")
run_button.pack(pady=12, padx=10)

output_frame = ct.CTkFrame(master=frame)
output_frame.pack(pady=10, padx=10, fill='both', expand=True)

ip_info_label = ct.CTkLabel(master=output_frame, text='IP Info: ', anchor='w')
ip_info_label.grid(row=0, column=0, sticky='w',pady=10, padx=10)
ip_info_tb = ct.CTkTextbox(master=output_frame, height=30, width=500)
ip_info_tb.grid(row=0, column=2, sticky='w',pady=10, padx=10)

country_label = ct.CTkLabel(master=output_frame, text='Country: ', anchor='w')
country_label.grid(row=1, column=0, sticky='w',pady=10, padx=10)
country_tb = ct.CTkTextbox(master=output_frame, height=30, width=500)
country_tb.grid(row=1, column=2, sticky='w',pady=10, padx=10)

location_info_label = ct.CTkLabel(master=output_frame, text='Region/City/Zipcode:', anchor='w')
location_info_label.grid(row=2, column=0, sticky='w',pady=10, padx=10)
location_info_tb = ct.CTkTextbox(master=output_frame, height=30, width=500)
location_info_tb.grid(row=2, column=2, sticky='w',pady=10, padx=10)

continent_label = ct.CTkLabel(master=output_frame, text='Continent:', anchor='w')
continent_label.grid(row=3, column=0, sticky='w',pady=10, padx=10)
continent_tb = ct.CTkTextbox(master=output_frame, height=30, width=500)
continent_tb.grid(row=3, column=2, sticky='w',pady=10, padx=10)

timezone_label = ct.CTkLabel(master=output_frame, text='Timezone:', anchor='w')
timezone_label.grid(row=4, column=0, sticky='w',pady=10, padx=10)
timezone_tb = ct.CTkTextbox(master=output_frame, height=30, width=500)
timezone_tb.grid(row=4, column=2, sticky='w',pady=10, padx=10)

time_label = ct.CTkLabel(master=output_frame, text='Local Time:', anchor='w')
time_label.grid(row=5, column=0, sticky='w',pady=10, padx=10)
time_tb = ct.CTkTextbox(master=output_frame, height=30, width=500)
time_tb.grid(row=5, column=2, sticky='w',pady=10, padx=10)

proxy_label = ct.CTkLabel(master=output_frame, text='Using Proxy?', anchor='w')
proxy_label.grid(row=6, column=0, sticky='w',pady=10, padx=10)
proxy_cb = ct.CTkCheckBox(master=output_frame, height=30, text="")
proxy_cb.grid(row=6, column=2, sticky='w',pady=10, padx=95)
proxy_cb.configure(state="disabled")

coords_label = ct.CTkLabel(master=output_frame, text='Lat/Long:', anchor='w')
coords_label.grid(row=7, column=0, sticky='w',pady=10, padx=10)
coords_tb = ct.CTkTextbox(master=output_frame, height=30, width=500)
coords_tb.grid(row=7, column=2, sticky='w',pady=10, padx=10)

google_maps_label = ct.CTkLabel(master=output_frame, text='View on Google Maps:', anchor='w')
google_maps_label.grid(row=8, column=0, sticky='w',pady=10, padx=10)
google_maps_tb = ct.CTkTextbox(master=output_frame, height=30, width=500)
google_maps_tb.grid(row=8, column=2, sticky='w',pady=10, padx=10)

request_time_label = ct.CTkLabel(master=output_frame, text='Request Length:', anchor='w')
request_time_label.grid(row=9, column=0, sticky='w',pady=10, padx=10)
request_time_tb = ct.CTkTextbox(master=output_frame, height=30, width=500)
request_time_tb.grid(row=9, column=2, sticky='w',pady=10, padx=10)


root.mainloop()

#if __name__ =='__main__':
#    main()