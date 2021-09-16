import subprocess
import random
import optparse

def get_arguments():
    myparse = optparse.OptionParser()
    myparse.add_option("-i", "--interface", dest="iface")
    myparse.add_option("-o", "--option", dest="tool_option")
    return myparse.parse_args()[0]

def mac_create():
    hex_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    double_hex_chars = ["0", "2", "4", "6", "8", "a", "c", "e"]
    mac_address = [random.choice(hex_chars) + random.choice(double_hex_chars)]
    for i in range(5):
        octet = ""
        for i in "ab":
            octet += random.choice(hex_chars)
        mac_address.append(octet)

    return ":".join(mac_address)

def restore_permaddr(iface):
    change_control = subprocess.check_output(["ip", "link", "show", iface], text=True)
    infoLine = change_control.splitlines()[1].strip()
    if ("permaddr" in infoLine):
        perm_address = infoLine.split(" permaddr ")[1]
        subprocess.run(["ifconfig", iface, "down"], capture_output=True)
        subprocess.run(["ifconfig", iface, "hw", "ether", perm_address], capture_output=True)
        subprocess.run(["ifconfig", iface, "up"], capture_output=True)
        print("\nPermanent Mac:", perm_address)
        print("[*]->> Your Mac address has been restored to permanent state! <<-[*]\n")
    else:
        your_mac = infoLine.split()[1]
        print("\nCurrent Mac:", your_mac)
        print("[*]->> It's the same mac! <<-[*]\n")

def random_mac(iface):
    iface_info = subprocess.check_output(["ip", "link", "show", iface], text=True)
    old_mac = iface_info.splitlines()[1].strip().split()[1]
    new_mac = mac_create()

    subprocess.run(["ifconfig", iface, "down"], capture_output=True)
    subprocess.run(["ifconfig", iface, "hw", "ether", new_mac], capture_output=True)
    subprocess.run(["ifconfig", iface, "up"], capture_output=True)

    iface_info = subprocess.check_output(["ip", "link", "show", iface], text=True)
    current_mac = iface_info.splitlines()[1].strip().split()[1]
    perm_address = iface_info.splitlines()[1].strip().split()[-1]

    if (current_mac == new_mac):
        print(f"""
        ----------------------------------
            Old Mac:   {old_mac}
            Permanent Mac: {perm_address}
            New Mac:       {new_mac}
        -----------------------------------
        [*]->> The mac address is changed! <<-[*]
        """)

    else:
        print("\n[!]->> The mac address has not changed! <<-[!]\n")


def nic_addr_changer(iface):
    iface_info = subprocess.check_output(["ip", "link", "show", iface], text=True)
    old_mac = iface_info.splitlines()[1].strip().split()[1]
    new_nic_mac = mac_create()[-8:]
    if (old_mac[-8:] != new_nic_mac):
        new_mac = old_mac[:8] + ":" + new_nic_mac
        subprocess.run(["ifconfig", iface, "down"], capture_output=True)
        subprocess.run(["ifconfig", iface, "hw", "ether", new_mac], capture_output=True)
        subprocess.run(["ifconfig", iface, "up"], capture_output=True)

        iface_info = subprocess.check_output(["ip", "link", "show", iface], text=True)
        current_mac = iface_info.splitlines()[1].strip().split()[1]

        if (current_mac == new_mac):
            perm_address = iface_info.splitlines()[1].strip().split()[-1]
            print(f"""
            ----------------------------------
            Old Mac:   {old_mac}
            Permanent Mac: {perm_address}
            New Mac:       {new_mac}
            -----------------------------------
        [*]->> The mac address is changed! <<-[*]
            """)

    else:
        print("\n[!]->> The mac address NIC has not changed! <<-[!]\n")


def oui_addr_changer(iface):
    iface_info = subprocess.check_output(["ip", "link", "show", iface], text=True)
    old_mac = iface_info.splitlines()[1].strip().split()[1]
    new_vendor_mac = mac_create()[:8]
    if (old_mac[:8] != new_vendor_mac):
        new_mac = new_vendor_mac + ":" + old_mac[9:]
        subprocess.run(["ifconfig", iface, "down"], capture_output=True)
        subprocess.run(["ifconfig", iface, "hw", "ether", new_mac], capture_output=True)
        subprocess.run(["ifconfig", iface, "up"], capture_output=True)

        iface_info = subprocess.check_output(["ip", "link", "show", iface], text=True)
        current_mac = iface_info.splitlines()[1].strip().split()[1]

        if (current_mac == new_mac):
            perm_address = iface_info.splitlines()[1].strip().split()[-1]
            print(f"""
            ----------------------------------
            Old Mac:   {old_mac}
            Permanent Mac: {perm_address}
            New Mac:       {new_mac}
            -----------------------------------
        [*]->> The mac address is changed! <<-[*]
            """)
    else:
        print("\n[!]->> The mac address NIC has not changed! <<-[!]\n")

def special_mac(iface):
    user_input_mac = input("Enter a valid mac address: ").strip().split(":")
    if (len(user_input_mac) == 6):
        hex_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
        double_hex_chars = ["0", "2", "4", "6", "8", "a", "c", "e"]
        o1 = user_input_mac[0]
        if (len(o1) == 2) and (o1[0] in hex_chars) and (o1[1] in double_hex_chars):
            for i in user_input_mac[1:]:
                i = i.lower()
                if (len(i) != 2) or (i[0] not in hex_chars) or (i[1] not in hex_chars):
                    print("\n[!]->> Invalid mac address <<-[!]\n")
                    break
            else:
                sp_mac = ":".join(user_input_mac)
                iface_info = subprocess.check_output(["ip", "link", "show", iface], text=True)
                old_mac = iface_info.splitlines()[1].strip().split()[1]

                subprocess.run(["ifconfig", iface, "down"], capture_output=True)
                subprocess.run(["ifconfig", iface, "hw", "ether", sp_mac], capture_output=True)
                subprocess.run(["ifconfig", iface, "up"], capture_output=True)

                iface_info = subprocess.check_output(["ip", "link", "show", iface], text=True)
                current_mac = iface_info.splitlines()[1].strip().split()[1]
                if (current_mac == sp_mac):
                    perm_address = iface_info.splitlines()[1].strip().split()[-1]
                    print(f"""
                    ----------------------------------
                    Old Mac:       {old_mac}
                    Permanent Mac: {perm_address}
                    New Mac:       {sp_mac}
                    -----------------------------------
                [*]->> The mac address is changed! <<-[*]
                    """)

                else:
                    print("\n[!]->> The mac address has not changed! <<-[!]\n")
        else:
            print("\n[!]->> Invalid mac address <<-[!]\n")

    else:
        print("\n[!]->> Invalid mac address <<-[!]\n")

def help_menu():
    print("""
                                HELP MENU
    --------------------------------------------------------------------------
    Use: python3 mac_changer.py -i <iface> -o <option(1,2,3,4,5)>
    Ex: python3 mac_changer.py -i wlan0 -o 2

    -i    --interface       Enter a interface
    -o    --tool_option     Enter a option, options = 1,2,3,4,5 one of them

    -o 1  ----> retore permanent mac
    -o 2  ----> random mac
    -o 3  ----> new nic address
    -o 4  ----> new oui address
    -o 5  ----> special mac address
    -o 6  ----> help menu

    ---------------------------------------------------------------------------""")

arguments = get_arguments()
iface = arguments.iface
tool_option = arguments.tool_option

if (tool_option == "6"):
    help_menu()

elif (iface != None) and (tool_option != None):

    control_iface = subprocess.run(["ip", "link", "show", iface], capture_output=True)
    if (control_iface.returncode == 0):
        option_funcs = {
            "1": restore_permaddr,
            "2": random_mac,
            "3": nic_addr_changer,
            "4": oui_addr_changer,
            "5": special_mac
        }

        if (tool_option in option_funcs):
            option_funcs[tool_option](iface)

        else:
            print("\n[!]->> Invalid Option <<-[!]\n")

    else:
        print("\n[!]->> Interface not found!! <<-[!]\n")

else:
    help_menu()