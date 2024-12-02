## NetScope
NetScope is a network scanning and monitoring tool designed to help users discover and monitor devices in their network. It provides useful information about each device, such as IP addresses, MAC addresses, device manufacturers, and packet sizes. With live monitoring and filtering capabilities, NetScope is perfect for home users, network admins, and IT enthusiasts.

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

1. **Install the required libraries using requirements.txt:**

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
3. **Install the tool on your system**
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

## Options


| Option                  | Description                                                                |
|-------------------------|----------------------------------------------------------------------------|
| `-r`, `--ip-range`      | Specify the target IP range or subnet to scan (e.g., `192.168.1.0/24`).    |
| `-n`, `--interfaces`    | Specify the network interface(s) to use (e.g., `eth0`, `wlan0`).           |
| `-l`, `--live`          | Enable live monitoring to track network devices in real-time.              |
| `-o`, `--output`        | Save scan results to a specified file.                                     |
| `-m`, `--manufacturer`  | Filter devices by manufacturer (e.g., `Apple`, `Samsung`).                 |
| `-i`, `--interval`      | Set the refresh interval for live monitoring (default: 5 seconds).         |
