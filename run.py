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

# Load driver
if os.name == 'nt':
  import winsound
  driver = webdriver.Chrome(r'C:\Users\rellik\Documents\GitHub\TescoSlotDetector\chromedriver_win32\chromedriver.exe')
else:
  driver = webdriver.Chrome('/Users/Like/Documents/tesco/chromedriver')

driver.set_window_position(0, 0)
driver.set_window_size(800, 900)

#queue_found = 0
#while True:
#  driver.get(r"C:\Users\rellik\Desktop\Tesco Groceries.html")
#    
#  try:
#    slot_message = driver.find_elements_by_xpath("//*[contains(text(), 'in a queue to shop with us')]")
#    queue_found = 1
#  except:
#    queue_found = 0
#
#  if queue_found == 1:
#    print ("queue found")
#  time.sleep(100000)
  
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
  for i in range(21):
    date = (datetime.now() + timedelta(days=i) ).strftime('%Y-%m-%d')
    url = "https://www.tesco.com/groceries/en-GB/slots/delivery/" + date + "?slotGroup=1"
    driver.get(url);

    time.sleep(1)
    print ("Checking Tesco Slot " + str(date))

    # Check for slot message and break the for loop if didnt find element
    # TODO: Seems sometimes it gets stuck and make no progress further unless hit enter in terminal. Investigate this problem. 
    try:
      slot_message = driver.find_element_by_class_name('slot-list--none-available')
    except:
      out = 1
      break

    # Sleep
    time.sleep(0.5)

  # Found slots or get into a queue
  if out == 1:
    # Test if it is a queue page
    not_in_queue = 0
    try:
      slot_message = driver.find_elements_by_xpath("//*[contains(text(), 'in a queue to shop with us')]")
    except:
      not_in_queue = 1
    
    if not_in_queue == 0:
      client.send_message("Please mannualy refresh the queue page.", title="We are in a Tesco online queue!")
      time.sleep(1800)
    else:
      client.send_message("Check " + date + " slots in broswer, will resume searching in 10 min.", title="Available Tesco Slot Found!")
      print("Slots found in " + date + ".")
      time.sleep(600)

