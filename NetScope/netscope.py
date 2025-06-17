#!/usr/bin/env python3

# copyright © Sreeraj, 2024
# https://github.com/s-r-e-e-r-a-j

import os, argparse, time, threading, requests, ipaddress
from scapy.all import ARP, Ether, srp
from rich.console import Console
from rich.table import Table

__c = Console()

def __args():
    p = argparse.ArgumentParser(description="Scan LAN for connected devices with optional live tracking.")
    p.add_argument("-r", "--ip-range", nargs='+', required=True, help="IP range/subnet(s) to scan (e.g. 192.168.0.0/24)")
    p.add_argument("-n", "--interfaces", nargs='+', required=True, help="Network interface(s) to use (e.g. eth0)")
    p.add_argument("-l", "--live", action="store_true", help="Enable real-time monitoring")
    p.add_argument("-o", "--output", help="Save results to file")
    p.add_argument("-m", "--manufacturer", help="Filter by vendor name")
    p.add_argument("-i", "--interval", type=int, default=5, help="Interval for live scan (default: 5s)")
    return p.parse_args()

def __check_root():
    if os.geteuid() != 0:
        __c.print("[red]Error: Root required. Use sudo.[/red]")
        exit()

def __vendor(mac):
    try:
        r = requests.get(f"https://api.macvendors.com/{mac}", timeout=2)
        return r.text.strip() if r.status_code == 200 else "Unknown"
    except:
        return "Unknown"

def __scan(ipr, iface):
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ipr)
    try:
        res, _ = srp(pkt, iface=iface, timeout=3, verbose=0)
    except OSError as e:
        if "No such device" in str(e): __c.print(f"[red]Interface '{iface}' not found.[/red]"); exit()
        else: raise
    devs = []
    for s, r in res:
        mac, ip = r.hwsrc, r.psrc
        devs.append({"ip": ip, "mac": mac, "vendor": __vendor(mac), "size": len(s)+len(r)})
    return devs

def __table(rows):
    t = Table(show_header=True, header_style="bold cyan")
    t.add_column("IP", style="green")
    t.add_column("MAC", style="blue")
    t.add_column("Size", style="magenta")
    t.add_column("Vendor", style="yellow")
    for d in rows:
        t.add_row(d['ip'], d['mac'], str(d['size']), d['vendor'])
    __c.print(t)

def __filter(lst, vendor=None):
    return [d for d in lst if not vendor or vendor.lower() in d['vendor'].lower()]

def __save(devs, f):
    with open(f, "a") as w:
        for d in devs:
            w.write(f"IP: {d['ip']}\nMAC: {d['mac']}\nVendor: {d['vendor']}\nSize: {d['size']} bytes\n\n")

def __live(iprs, ifs, fout, fvend, interval):
    mem = []
    while True:
        for ipr in iprs:
            for iface in ifs:
                now = __scan(ipr, iface)
                new = [d for d in now if d not in mem]
                if fout and new: __save(new, fout); mem.extend(new)
                final = __filter(now, fvend)
                __c.clear()
                __table(final)
        time.sleep(interval)

def __main():
    __check_root()
    a = __args()
    seen = []
    for i in a.ip_range:
        for n in a.interfaces:
            seen.extend(__scan(i, n))
    result = __filter(seen, a.manufacturer)
    __table(result)
    if a.output: __save(result, a.output); __c.print(f"[green]Saved to {a.output}[/green]")
    if a.live:
        t = threading.Thread(target=__live, args=(a.ip_range, a.interfaces, a.output, a.manufacturer, a.interval))
        t.daemon = True
        t.start()
        try:
            while t.is_alive(): time.sleep(1)
        except KeyboardInterrupt:
            __c.print("\n[red]Interrupted. Exiting...[/red]")

if __name__ == "__main__":
    __main()
