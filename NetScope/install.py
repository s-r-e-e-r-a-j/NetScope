import os
choice = input('[+] to install press (Y) to uninstall press (N) >> ')
run = os.system
if str(choice) =='Y' or str(choice)=='y':

    run('chmod 777 netscope.py')
    run('mkdir /usr/share/netscope')
    run('cp netscope.py /usr/share/netscope/netscope.py')

    cmnd=(' #! /bin/sh \n exec python3 /usr/share/netscope/netscope.py "$@"')
    with open('/usr/bin/netscope','w')as file:
        file.write(cmnd)
    run('chmod +x /usr/bin/netscope & chmod +x /usr/share/netscope/netscope.py')
    print('''\n\ncongratulation NetScope is installed successfully \nfrom now just type \x1b[6;30;42mnetscope\x1b[0m in terminal ''')
if str(choice)=='N' or str(choice)=='n':
    run('rm -r /usr/share/netscope ')
    run('rm /usr/bin/netscope ')
    print('[!] now NetScope  has been removed successfully')
