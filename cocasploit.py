#!/usr/bin/python
import os
import sys, traceback

# check for root
if not os.geteuid() == 0:
    sys.exit("""!! Run as root !!""")

# msg to display when quitting
byemsg = "\nbye!"

def main():
    try:
        # setup network interface and gateway
        def config():
            global up_iface
            up_iface = os.popen("route | awk '/Iface/{getline; print $8}'").read()
            print("Found active network interface: " + up_iface)
            up_iface = up_iface.replace("\n","")
            valid = {"yes": True, "y": True, "YES": True, "Y": True, "no": False, "n": False, "NO": False, "N": False}
            while True:
                choice = input("Use " + up_iface + " [Y/n]: ")
                print(choice)
                if choice == "":
                    choice = "y"
                if choice in valid:
                    use_interface = valid[choice]
                    break
                else:
                    print("Wrong input, answer with y or n")
            if not use_interface:
                up_iface = input("Interface to use: ")
            
            global gateway
            gateway = os.popen("ip route show | grep -i 'default via' | awk '{print $3}'").read()
            gateway = gateway.replace("\n","")

            # get local network
            global n_ssid
            n_ssid = os.popen('iwgetid -r').read() # name
            n_ssid = n_ssid.replace("\n","")
            global n_bssid
            n_bssid = os.popen("ip addr | grep 'state UP' -A1 | tail -n1 | awk '{print $2}' | cut -f1 -d'/'").read() # mac
            n_bssid = n_bssid.replace("\n","")
            global n_ip
            n_ip = os.popen("hostname -I | cut -f1 -d' '").read() # local ip address
            n_ip = n_ip.replace("\n","")
            global n_hostname
            n_hostname = os.popen('hostname').read() # hostname 
            n_hostname = n_hostname.replace("\n","")

            print(" [*] Network interface: " + up_iface)
            print(" [*] Gateway: " + gateway + "\n")
            
            print(" [-] Network (SSID): " + str(n_ssid))
            print(" [-] BSSID: " + n_bssid)
            print(" [-] IP Address: " + str(n_ip))
            print(" [-] Hostname: " + str(n_hostname))

        config()
    
    except KeyboardInterrupt:
        print ("\n" + byemsg)
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

if __name__ == "__main__":
    main()