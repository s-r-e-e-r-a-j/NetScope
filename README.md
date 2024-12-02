## NetScope
NetScope is a network scanning and monitoring Ethical Hacking tool designed to help users discover and monitor devices in their network. It provides useful information about each device, such as IP addresses, MAC addresses, device manufacturers, and packet sizes. With live monitoring and filtering capabilities, NetScope is perfect for home users, network admins, and IT enthusiasts.

## Features
- **Network Scanning:** Quickly find devices in your network.
- **Device Details:** Get details like IP address, MAC address, manufacturer name, and packet size.
- **Live Monitoring:** Continuously track devices on your network with live updates.
- **Manufacturer Filter:** View devices from a specific manufacturer (e.g., Apple, Samsung).
- **Save Results:** Export scan results to a file for later use.
## Installation
- Python 3.x installed on your system.
- The following Python libraries:
- scapy
- rich
- requests
- os
- argparse
- threading
- ipaddress
- time
### Installation Steps

1. **Clone the repository:**

```bash
git clone https://github.com/s-r-e-e-r-a-j/NetScope.git
```
```bash
cd NetScope
``` 
2.  **Install the required libraries using requirements.txt:**

``` bash
pip3 install -r requirements.txt
```
3. **Install NetScope on your system**
```bash
cd NetScope
 ```
```bash
sudo python3 install.py
 ```
   **Then Enter `y` for install**
   
4. **Make sure to run NetScope as sudo:**

```bash
sudo netscope [command line options]
```

## Options


| Option                  | Description                                                                |
|-------------------------|----------------------------------------------------------------------------|
| `-r`, `--ip-range`      | Specify the target IP range or subnet to scan (e.g., `192.168.1.0/24`).    |
| `-n`, `--interfaces`    | Specify the network interface(s) to use (e.g., `eth0`, `wlan0`).           |
| `-l`, `--live`          | Enable live monitoring to track network devices in real-time.              |
| `-o`, `--output`        | Save scan results to a specified file.                                     |
| `-m`, `--manufacturer`  | Filter devices by manufacturer (e.g., `Apple`, `Samsung`).                 |
| `-i`, `--interval`      | Set the refresh interval for live monitoring (default: 5 seconds).         |



## Example Usage
### Basic Network Scan
Scan all devices within a subnet or IP range:

```bash
sudo netscope -r 192.168.1.0/24 -n eth0
```
### Save Scan Results to a File
Scan a network and save the output to a file:

```bash
sudo netscope -r 192.168.1.0/24 -n eth0 -o results.txt
``` 
### Filter by Manufacturer
Only display devices from a specific manufacturer:

```bash
sudo netscope -r 192.168.1.0/24 -n eth0 -m "Apple"
```
### Enable Live Monitoring
Continuously monitor the network for changes:

```bash
sudo netscope -r 192.168.1.0/24 -n eth0 -l
```
### Live Monitoring with a Custom Interval
Set a custom refresh interval for live monitoring (e.g., 10 seconds):

```bash
sudo netscope -r 192.168.1.0/24 -n eth0 -l -i 10
```
## Output Example
When scanning the network, NetScope displays a table with device details:

```mathematica
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ IP Address    ┃ MAC Address       ┃ Packet Size ┃ Manufacturer     ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ 192.168.1.10  │ 00:1A:2B:3C:4D:5E │ 128         │ Apple            │
│ 192.168.1.15  │ 11:22:33:44:55:66 │ 128         │ Samsung          │
└───────────────┴───────────────────┴─────────────┴──────────────────┘
```

## uninstallation
```bash
cd NetScope
```
```bash
cd NetScope
```
```bash
sudo python3 install.py
```
**Then Enter `n` for uninstall**

## Notes
1.**Run with sudo**: NetScope requires root privileges to access network interfaces. Always run with sudo.

2.**Internet Connection**: The tool uses an online service to identify device manufacturers. Ensure you have an active internet connection.


## License
NetScope is licensed under the MIT License.

## Author
- **Sreeraj**
GitHub: https://github.com/s-r-e-e-r-a-j
