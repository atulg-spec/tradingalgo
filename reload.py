import time
import os

os.system('clear')
os.system('sudo systemctl status algo')
time.sleep(2)
os.system('python3 create.py')
time.sleep(1)
os.system('sudo systemctl restart algo')
time.sleep(5)
os.system('sudo systemctl restart nginx')
os.system('sudo systemctl status algo')



