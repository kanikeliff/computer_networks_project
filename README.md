```
  _   _      _                      _    
 | \ | | ___| |___      _____  _ __| | __
 |  \| |/ _ \ __\ \ /\ / / _ \| '__| |/ /
 | |\  |  __/ |_ \ V  V / (_) | |  |   < 
 |_| \_|\___|\__| \_/\_/ \___/|_|  |_|\_\
                                          
  ____            _           _   #1
 |  _ \ _ __ ___ (_) ___  ___| |_ 
 | |_) | '__/ _ \| |/ _ \/ __| __|
 |  __/| | | (_) | |  __/ (__| |_ 
 |_|   |_|  \___// |\___|\___|\__|
               |__/               
```

# Computer Networks Project #1
### Robust Client–Server Communication and JSON Processing

---

## Project Structure

```
computer_networks_project/
├── client.py                 # main client application
├── original.json             # input file with personal info
├── modified_available.json   # server response (available scenario)
├── modified_unavailable.json # no response (unavailable scenario)
├── client_available.log      # log file (available scenario)
├── client_unavailable.log    # log file (unavailable scenario)
└── README.md
```

---

## Description

A Python client that sends a JSON file to a remote server, receives a modified version back, and compares the two files. The client handles connection errors, retries automatically, and logs all activity.

---

## How to Run

**1. Install dependencies**
```bash
pip install requests
```

**2. Run the client**
```bash
python client.py
```

The client will:
- Read `original.json`
- Send it to the server via POST request
- Save the server response as `modified.json`
- Compare the two files and print the differences
- Retry every 60 seconds if the server is unavailable

---

## Server Availability

The server only accepts requests between **09:00 and 18:00**.  
Outside these hours the client will keep retrying automatically until it succeeds.

---

## Files

| File | Description |
|------|-------------|
| `client.py` | Main Python client |
| `original.json` | Personal info sent to server |
| `modified_available.json` | Server response (success scenario) |
| `modified_unavailable.json` | Empty — no response outside hours |
| `client_available.log` | Log showing successful interaction |
| `client_unavailable.log` | Log showing retries and failures |

---

## Author
Elif Kanık
