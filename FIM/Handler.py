import File_Integrity_Monitor

# --- Edit according to your preference ---
path = "./Monitor/"
baseline_name = ".baseline.txt"
duration = 28  # in seconds
ignore_files_list = ["Ignore.txt"]

receive_email = True  # Use True or False
username = "yourmail@gmail.com"
pwd = "your-app-password"
# -----------------------------------------

file_integrity_monitor = File_Integrity_Monitor.FIM(
    path, baseline_name, duration, ignore_files_list, receive_email, username, pwd)
file_integrity_monitor.start()
