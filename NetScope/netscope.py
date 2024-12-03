#!/usr/bin/env python3

# copyright of Sreeraj,2024
# https://github.com/s-r-e-e-r-a-j

import os
import argparse
from rich.console import Console
from rich.table import Table
from scapy.all import ARP, Ether, srp
import requests
import threading
import time
import ipaddress


class NetScope:
    def __init__(self):
        self.console = Console()
        self.check_sudo()

    def check_sudo(self):
        """Exit if the script is not run as root or with sudo."""
        if os.geteuid() != 0:
            self.console.print("[bold red]Error:[/] This tool requires root privileges. Please run with [bold]sudo[/bold].")
            exit()

    def scan_network(self, ip_range, interface):
        arp_request = ARP(pdst=ip_range)
        ethernet_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
        request_packet = ethernet_frame / arp_request

        try:
            responses = srp(request_packet, timeout=3, verbose=0, iface=interface)[0]
        except OSError as e:
            if "No such device" in str(e):
                self.console.print(f"[bold red]Invalid Interface:[/] The interface '{interface}' does not exist.")
                exit()
            else:
                raise

        devices = []
        for sent, received in responses:
            mac_address = received.hwsrc
            manufacturer_name = self.get_manufacturer_name(mac_address)
            packet_size = len(sent) + len(received)
            devices.append({'ip': received.psrc, 'mac': mac_address, 'manufacturer': manufacturer_name, 'packet_size': packet_size})

        return devices

    def get_manufacturer_name(self, mac):
        try:
            response = requests.get(f"https://api.macvendors.com/{mac}")
            return response.text.strip() if response.status_code == 200 else "Unknown"
        except requests.RequestException:
            return "Unknown"

    def filter_results(self, devices, manufacturer_filter=None):
        return [
            device for device in devices
            if not manufacturer_filter or device['manufacturer'].lower() == manufacturer_filter.lower()
        ]

    def live_scan(self, ip_ranges, network_interfaces, save_file=None, manufacturer_filter=None, interval=5):
        known_devices = []
        while True:
            for ip_range in ip_ranges:
                for interface in network_interfaces:
                    current_devices = self.scan_network(ip_range, interface)

                    new_devices = [device for device in current_devices if device not in known_devices]
                    if new_devices and save_file:
                        self.save_to_file(new_devices, save_file)
                        known_devices.extend(new_devices)

                    filtered_devices = self.filter_results(current_devices, manufacturer_filter)

                    self.console.clear()
                    table = Table(show_header=True, header_style="bold magenta")
                    table.add_column("IP Address", style="bold red")
                    table.add_column("MAC Address", style="bold blue")
                    table.add_column("Packet Size", style="bold green")
                    table.add_column("Manufacturer", style="bold yellow")

                    for device in filtered_devices:
                        table.add_row(device['ip'], device['mac'], str(device['packet_size']), device['manufacturer'])

                    self.console.print(table)
                    time.sleep(interval)

    def save_to_file(self, devices, filepath):
        with open(filepath, 'a') as file:
            for device in devices:
                file.write(f"IP Address: {device['ip']}\n")
                file.write(f"MAC Address: {device['mac']}\n")
                file.write(f"Manufacturer: {device['manufacturer']}\n")
                file.write(f"Packet Size: {device['packet_size']} bytes\n\n")

    def run(self):
        try:
            args = self.parse_arguments()
            ip_ranges = args.ip_range
            interfaces = args.interfaces
            track_live = args.live
            output_path = args.output
            manufacturer_filter = args.manufacturer
            scan_interval = args.interval

            all_devices = []
            for ip_range in ip_ranges:
                for interface in interfaces:
                    all_devices.extend(self.scan_network(ip_range, interface))

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("IP Address", style="bold red")
            table.add_column("MAC Address", style="bold blue")
            table.add_column("Packet Size", style="bold green")
            table.add_column("Manufacturer", style="bold yellow")

            filtered_devices = self.filter_results(all_devices, manufacturer_filter)

            for device in filtered_devices:
                table.add_row(device['ip'], device['mac'], str(device['packet_size']), device['manufacturer'])

            self.console.print(table)

            if output_path:
                self.save_to_file(filtered_devices, output_path)
                self.console.print(f"\n[bold green]Results saved to {output_path}")

            if track_live:
                live_thread = threading.Thread(target=self.live_scan,
                                               args=(ip_ranges, interfaces, output_path, manufacturer_filter, scan_interval))
                live_thread.daemon = True
                live_thread.start()

                while live_thread.is_alive():
                    time.sleep(1)

        except KeyboardInterrupt:
            self.console.print("\n[bold red]User interrupted. Exiting...")

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="NetScope: A tool for network scanning and monitoring.")
        parser.add_argument("-r", "--ip-range", help="Target IP range or subnet (e.g., 192.168.1.0/24)", nargs='+', required=True)
        parser.add_argument("-n", "--interfaces", help="Network interface(s) to use (e.g., eth0, wlan0)", nargs='+', required=True)
        parser.add_argument("-l", "--live", action="store_true", help="Enable live monitoring of devices.")
        parser.add_argument("-o", "--output", help="File to save the results.")
        parser.add_argument("-m", "--manufacturer", help="Filter results by manufacturer name (e.g., Apple).")
        parser.add_argument("-i", "--interval", type=int, default=5, help="Refresh interval for live monitoring (default: 5 seconds).")
        return parser.parse_args()


if __name__ == "__main__":
    netscope = NetScope()
    netscope.run()
