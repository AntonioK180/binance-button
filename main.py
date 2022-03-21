from pickle import NONE
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt
import matplotlib as mpt
import numpy as np
import datetime as dt

options = Options()
options.headless = True

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

driver.get("https://www.binance.me/en/activity/bitcoin-button-game")

accept_cookies = driver.find_element_by_id("onetrust-accept-btn-handler")
accept_cookies.click()

time.sleep(0.5)

data_rows = driver.find_elements_by_class_name("css-th68ec")
timer_value = driver.find_elements_by_class_name("css-w39bvu")

times_clicked = None
sum_clicked = []
times_clicked_per_tick = []
timestamps = []
smallest_number_on_counter = 6000

for row in data_rows:
	if row.text != "--":
		times_clicked_element = row
		break

while len(sum_clicked) < 3500:
	times_clicked = times_clicked_element.text.replace(',', '')

	times_clicked = int(times_clicked)
	if len(sum_clicked) == 0:
		sum_clicked.append(times_clicked)
		timestamps.append(round(time.time(), 2))
	elif (sum_clicked[-1] != times_clicked):
		times_clicked_per_tick.append(times_clicked - sum_clicked[-1])
		sum_clicked.append(times_clicked)
		timestamps.append(round(time.time(), 2))

	smallest_number_on_counter_temp = ""
	for digit in timer_value:
		smallest_number_on_counter_temp += digit.text
	
	if int(smallest_number_on_counter_temp) < int(smallest_number_on_counter):
		smallest_number_on_counter = smallest_number_on_counter_temp
	
	print(smallest_number_on_counter_temp)
	time.sleep(6)


driver.close()

sum_clicked.pop(0)
timestamps.pop(0)
times_clicked_per_tick[0] = times_clicked_per_tick[-1]

print(sum_clicked)
print(len(timestamps))
print(times_clicked_per_tick)

dates=[dt.datetime.fromtimestamp(ts) for ts in timestamps]

fig, ax = plt.subplots()
ax.plot(np.array(dates), np.array(times_clicked_per_tick))
ax.get_yaxis().set_major_formatter(mpt.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

plt.ylim(0, 75)
plt.show()

print("Smallest number: " + str(smallest_number_on_counter))

#SMallest number: 42:50