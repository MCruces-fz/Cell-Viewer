from utils.const import *
import os

print("remember to update the directory DATA_DIR to your desired place")
user = input("Type your Trucha user: ")
os.system(f"scp -r {user}@fptrucha.usc.es:/home/labcaf/People/Pablo.Cabanelas/soft/png {DATA_DIR}/../. ")
