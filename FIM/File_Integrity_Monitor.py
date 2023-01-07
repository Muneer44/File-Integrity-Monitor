from datetime import datetime
import hashlib
import os
import time
import smtplib


class FIM():
    def __init__(self, path, baseline_name, duration, ignore_files_list, receive_email, username, pwd):
        self.path = path
        self.baseline_name = baseline_name
        self.duration = duration
        self.ignore_list = ignore_files_list
        self.files_list, self.folders_list = self.list_files()

        self.receive_email = receive_email
        self.username = username
        self.pwd = pwd

    def options(self):
        print("\nChoose an option:\n  \
            A] Create new baseline\n  \
            B] Monitor files with existing baseline")
        if os.path.isfile("Report.txt"):
            print("              C] Erase Report file")
            print("              X] Exit")
            return input("\nEnter 'A' , 'B' or 'C': ")
        else:
            print("              X] Exit")
            return input("\nEnter 'A' or 'B': ")

    def list_files(self):
        # List all files in 'path' dir
        files = os.listdir(self.path)
        files_list = []
        folders_list = []
        for f in files:
            if os.path.isfile(self.path + f):
                files_list.append(f)
            elif os.path.isdir(self.path + f):
                folders_list.append(f)

        return files_list, folders_list

    def sha256sum(self, filename):
        # Skip hashing of 'ignore_list' files
        if self.ignore_list:
            for i in self.ignore_list:
                if filename == i:
                    return "ignore file"

        # Calculate hash
        h = hashlib.sha256()
        b = bytearray(128*1024)
        mv = memoryview(b)
        try:
            with open(self.path + filename, 'rb', buffering=0) as f:
                while n := f.readinto(mv):
                    h.update(mv[:n])
            return h.hexdigest()
        except PermissionError as error:
            self.write_errors(error)
            pass

    def get_date_time(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y | %H:%M:%S")

    def write_baseline_file(self, filename, file_hash):
        with open(self.baseline_name, 'a') as baseline_file:
            if os.stat(self.baseline_name).st_size != 0:
                baseline_file.write("\n")
            baseline_file.write(filename + " | " + file_hash)
            print(f"'{filename}'")

    def read_baseline_file(self):
        with open(self.baseline_name, "r") as baseline_file:
            baseline_content = baseline_file.read()
            baseline_content_line = baseline_content.split("\n")
            return baseline_content, baseline_content_line

    def write_errors(self, error):
        current_date_time = self.get_date_time()
        with open("exceptions.txt", 'a') as exceptions:
            exceptions.write(f"# {current_date_time}\n {error}\n\n")

    def set_index(self, baseline_content_line):
        if len(self.files_list) > len(baseline_content_line):
            return len(self.files_list)
        else:
            return len(baseline_content_line)

    def current_baseline_file(self, each_baseline_list):
        position = each_baseline_list.index("|")
        current_file = ''
        for p in range(position):
            if not current_file:
                current_file = current_file + each_baseline_list[p]
            else:
                current_file = current_file + " " + each_baseline_list[p]
        return current_file

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        # print(len(self.files_list))
        choice = self.options()
        # Create new baseline
        if choice.upper() == "A":
            # Check & remove if baseline already exists
            if os.path.isfile(self.baseline_name):
                os.remove(self.baseline_name)

            # Create new baseline
            if not self.files_list:
                print(f"\n  [!] found no file in '{self.path}' directory")
            else:
                file_count = 0
                for file in self.files_list:
                    file_hash = self.sha256sum(file)

                    # Update 'baseline.txt'
                    if file_hash != "ignore file":
                        file_count += 1
                        self.write_baseline_file(file, file_hash)
                print(
                    f"\n  => Hash of above [{file_count}] files stored in baseline.txt")
            time.sleep(3)
            self.start()

        # Monitor with existing baseline
        elif choice.upper() == "B":
            print(f"\n=> Path: {self.path}")
            print(f"=> Report duration: {self.duration} seconds")
            print(f"=> Email functionality: {self.receive_email}")
            print("\n  *** Monitoring started ***\n")

            # collect data from 'baseline.txt' file
            if os.path.isfile(self.baseline_name):
                baseline_content, baseline_content_line = self.read_baseline_file()
            else:
                print(" [!] Baseline file missing, Create a new baseline!")
                exit()
            # Monitoring loop
            while True:
                report = ''
                index = self.set_index(baseline_content_line)

                # Iterate through each file
                for i in range(index):
                    index = self.set_index(baseline_content_line)
                    current_date_time = self.get_date_time()

                    try:
                        # Detect unknown file
                        try:
                            self.files_list = os.listdir(self.path)
                            if self.files_list[i] not in baseline_content and self.files_list[i] not in self.ignore_list and self.files_list[i] not in self.folders_list:
                                report = report + "\n" + (
                                    f"'{self.files_list[i]}' : unknown file detected")
                        except IndexError:
                            pass

                        # Split Filename and Hash
                        try:
                            each_baseline_list = baseline_content_line[i].split(
                                " ")
                        except IndexError:
                            pass

                        # Fetch current file from baseline
                        current_file_name = self.current_baseline_file(
                            each_baseline_list)

                        # Compute current file hash
                        try:
                            current_file_hash = self.sha256sum(
                                current_file_name)
                        # Detect deleted file
                        except FileNotFoundError:
                            report = report + "\n" + (
                                f"'{current_file_name}' : deleted")
                            continue

                        # Detect file modification
                        if current_file_hash != each_baseline_list[-1]:
                            report = report + "\n" + (
                                f"'{current_file_name}' : modified")
                            continue

                    # log errors in 'exceptions.txt' file
                    except Exception as error:
                        self.write_errors(error)
                        continue

                # Send report
                if report:
                    report = (
                        f"\n----- Report of {current_date_time} -----\n{report}\n\n")

                    # log findings in 'Report.txt' file
                    with open("Report.txt", 'a') as report_file:
                        report_file.write(report)
                    print(report)

                    # Send mail
                    if self.receive_email:
                        try:
                            self.send_mail(self.username, self.pwd, report)

                        # Invaid username/password
                        except smtplib.SMTPAuthenticationError as error:
                            self.write_errors(error)

                    time.sleep(self.duration)

        # Erase existing Report file
        elif choice.upper() == "C":
            # Check & remove report file
            if os.path.isfile("Report.txt"):
                os.remove("Report.txt")
                print("\n  => Report.txt deleted")
            else:
                print("\n  [!] Inavlid input!")
            time.sleep(2)
            self.start()

        # Exit block
        elif choice.upper() == 'X':
            print("\n  => Program Terminated using exit code\n")
            exit()

        # Invalid input block
        else:
            print("  [!] Inavlid input!")
            time.sleep(1)
            self.start()
