import os
import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = "bdamilola00@gmail.com"
PASSWORD = os.environ.get('PASSWORD')
API_URL = os.environ.get("API_URL")
API_URL_1 = os.environ.get("API_URL_1")

MY_LAT = float(os.environ.get("MY_LAT"))
MY_LONG = float(os.environ.get("MY_LONG"))

def is_iss_overhead():
    """ This check is the iss is close to my location"""

    response = requests.get(url=API_URL)
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # My position is within +5 or -5 degree of the iss position
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def night_time():
    """ This checks if it's nighttime at my location"""
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(url=API_URL_1, params=parameters, verify=False)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and night_time():
        with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg="Subject:ISS IS HERE\n\nLook up, the ISS is passing."
                                )

