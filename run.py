# Tesco Booker v1.0
# Download chromedriver for script to function 

import time
import sys
import os
from datetime import datetime
from datetime import timedelta
from selenium import webdriver  # need to be installed
from pushover import Client     # need to be installed

# Send notification to phone using pushover
# This is my personal TOKEN and API, please do not use them for testing
client = Client("uj4ktz2oah8huuc9kk7g6awg6gactw", api_token="abe4opagsun1xdiya5c5fxykyvj2o4") # user-key and token 

start_date = (datetime.now() + timedelta(days=13) ).strftime('%m-%d')
end_date   = (datetime.now() + timedelta(days=21) ).strftime('%m-%d')

client.send_message("Searching slots from " + start_date + " to " + end_date, title="Start to find available Tesco slots!")

# Load driver
if os.name == 'nt':
  import winsound
  driver = webdriver.Chrome(r'C:\Users\rellik\Desktop\Workspace\TescoSlotDetector-master\chromedriver_win32\chromedriver.exe')
else:
  driver = webdriver.Chrome('/Users/Like/Documents/tesco/chromedriver')

driver.set_window_position(0, 0)
driver.set_window_size(800, 900)

# Load url
driver.get("https://secure.tesco.com/account/en-GB/login")
current_url = driver.current_url

# Wait for user to login and add items to basket
while current_url != "https://www.tesco.com/groceries/en-GB/slots/delivery":
    current_url = driver.current_url
    time.sleep(2)

# Loop forever
loop_cnt = 1
while True:

  print ("\nStarting " + str(loop_cnt) + "th Tesco slot searches.")
  out = 0

  # Iterate over days for three weeks
  for i in range(13, 21):
    date = (datetime.now() + timedelta(days=i) ).strftime('%Y-%m-%d')
    url = "https://www.tesco.com/groceries/en-GB/slots/delivery/" + date + "?slotGroup=1"
    driver.get(url);

    time.sleep(1)
    print ("Checking Tesco Slot " + str(date))

    # Check for slot message and break if didnt find element
    # TODO: Seems sometimes it gets stuck and make no progress further. Investigate this problem.
    try:
      slot_message = driver.find_element_by_class_name('slot-list--none-available')
    except:
      out = 1
      break

    # Sleep
    time.sleep(0.5)


  loop_cnt = loop_cnt + 1
  
  if ((loop_cnt % 1000) == 0) and out == 0:
    client.send_message("Completed " + str(loop_cnt) + " searches.", title="Milestone")
    
  # Break out main loop
  if out == 1:
    client.send_message("Slots in " + date + ", resume searching in 1 min.", title="Current in Queue OR available Tesco Slot Found!")
    time.sleep(60)

