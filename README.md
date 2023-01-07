# File-Integrity-Monitor

> ### _This script is capable of recursively surveiling files in the specified path._


## Description
Ever worried about your critical information being tweaked by malicious actor and you happen to use the manipulated data?. This FIM script is exactly designed to keep you safe and informed about such malicious manipulation attacks.

FIM is commonly used in the Cardholder Data Environment (CDE). It is a handy tool for blue-teamers to be informed about all data manipulation attacks.

## Capabilities:
- Recognize File modification
- File deletion detection
- Unknown file detection
- Ignore certain files
- Report the findings over e-mail
- Log the findings in `Report` text file
- Cross platform capability


## Demonstration
https://user-images.githubusercontent.com/31078414/211162996-cc69ef37-69d0-4e72-bb72-634752d94d0d.mp4

## This repository contains:
- **Handler.py :** To change the preferences and start the script
- **File_Integrity_Monitor.py :** Main BG script file
- **Monitor Folder:** Default folder to monitor


_This application is tested and tried on Python 3.10.7 and works on more than one computer architecture/ OS._

## Installation process
*Assuming you're using Windows OS,*
- *Download this repository,* 
- *Update the arguments accordingly in `Handler.py` file* 
- *And execute the `Handler.py` file.*

```
C:\Users\user> python3 "FIM/Handler.py" 
```
- On execution of this script, it will create the following files in the FIM directory:
  - `.baseline.txt` : Contains hashes of monitoring files
  - `Report.txt` : Log of all the detections
  
## Recommended
- Change the `Path` from default directory
- Change the `Baseline_name`
- Enable `receive_email`
  - *Note: Gmail requires you to use "App password" on your applications instead of your actual "email password".*
    ![App_pwd](https://user-images.githubusercontent.com/31078414/201460604-6f080b47-a39c-4dae-8a11-06d21bd5d24b.gif)

## Disclaimer
The use of code contained in this repository, either in part or in its totality,
for engaging targets without prior mutual consent is illegal. **It is
the end user's responsibility to obey all applicable local, state and
federal laws.**

