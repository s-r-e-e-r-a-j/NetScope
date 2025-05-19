#!/usr/bin/env python3

# copyright © Sreeraj, 2024
# https://github.com/s-r-e-e-r-a-j

import os
import argparse
import time
import requests
import threading
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
from rich.console import Console
from rich.table import Table

__c = Console()

def __sudo_guard():
    if os.geteuid() != 0:
        __c.print("[bold red]Permission Denied:[/] Run as [bold]root[/bold] or with [bold]sudo[/bold].")
        exit()

def __resolve_mac(mac):
    try:
        r = requests.get(f"https://api.macvendors.com/{mac}")
        return r.text.strip() if r.status_code == 200 else "Unknown"
    except:
        return "Unknown"

def __query_lan(ipmask, nic):
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ipmask)
    try:
        resp, _ = srp(packet, iface=nic, timeout=3, verbose=0)
    except OSError as e:
        if "No such device" in str(e):
            __c.print(f"[bold red]Invalid Interface:[/] '{nic}' does not exist.")
            exit()
        else:
            raise

    found = []
    for _, res in resp:
        mac = res.hwsrc
        vendor = __resolve_mac(mac)
        found.append({
            "ip": res.psrc,
            "mac": mac,
            "manu": vendor,
            "size": len(_) + len(res)
        })
    return found

def __refine(devs, filt=None):
    return [d for d in devs if not filt or d['manu'].lower() == filt.lower()]

def __save(devs, path):
    with open(path, 'a') as out:
        for d in devs:
            out.write(f"IP Address: {d['ip']}\n")
            out.write(f"MAC Address: {d['mac']}\n")
            out.write(f"Manufacturer: {d['manu']}\n")
            out.write(f"Packet Size: {d['size']} bytes\n\n")

def __banner(devs):
    tab = Table(show_header=True, header_style="bold cyan")  # Changed header color
    tab.add_column("IP Address", style="bold magenta")       # New color
    tab.add_column("MAC Address", style="bold white")        # New color
    tab.add_column("Packet Size", style="bold green")        # Retained for contrast
    tab.add_column("Manufacturer", style="bold blue")        # New color

    for d in devs:
        tab.add_row(d['ip'], d['mac'], str(d['size']), d['manu'])
    __c.print(tab)

def __track(ipblocks, ifcs, path=None, vendor=None, pace=5):
    prev = []
    while True:
        for net in ipblocks:
            for i in ifcs:
                now = __query_lan(net, i)
                unseen = [x for x in now if x not in prev]
                if unseen and path:
                    __save(unseen, path)
                    prev.extend(unseen)
                screen = __refine(now, vendor)
                __c.clear()
                __banner(screen)
                time.sleep(pace)

def __launch():
    a = __get_args()
    nets = a.ip_range
    devs = a.interfaces
    out = a.output
    man = a.manufacturer
    wait = a.interval

    inventory = []
    for net in nets:
        for d in devs:
            inventory += __query_lan(net, d)

    relevant = __refine(inventory, man)
    __banner(relevant)

    if out:
        __save(relevant, out)
        __c.print(f"\n[bold green]Saved to:[/] {out}")

    if a.live:
        live = threading.Thread(target=__track, args=(nets, devs, out, man, wait))
        live.daemon = True
        live.start()
        try:
            while live.is_alive():
                time.sleep(1)
        except KeyboardInterrupt:
            __c.print("\n[bold red]Cancelled by user.[/]")
            exit()

def __get_args():
    p = argparse.ArgumentParser(description="Network Info Scanner")
    p.add_argument("-r", "--ip-range", nargs='+', required=True, help="CIDR range(s) to scan.")
    p.add_argument("-n", "--interfaces", nargs='+', required=True, help="Interface(s) like eth0/wlan0.")
    p.add_argument("-l", "--live", action="store_true", help="Enable real-time monitoring.")
    p.add_argument("-o", "--output", help="File path to store output.")
    p.add_argument("-m", "--manufacturer", help="Filter by manufacturer name.")
    p.add_argument("-i", "--interval", type=int, default=5, help="Interval in seconds for live scan.")
    return p.parse_args()


if __name__ == "__main__":
    __sudo_guard()
    __launch()
