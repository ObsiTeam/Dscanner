import json
import os
import ipaddress
from platform import system


def clear():
    if system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def get_settings():
    with open("data/settings.json", "r", encoding="utf-8") as file:
        return json.load(file)


def get_last_session():
    with open("data/tmp/last_session.json", "r", encoding="utf-8") as file:
        return json.load(file)


def save_file(new_thinks, file_path):
    try:
        os.remove(file_path)
    except:
        pass
    with open(file_path, "w") as file:
        file.write(new_thinks)


def get_lang(settings, state=0):
    if state == 1 or settings["language"] is None:
        lang_list = ["EN", "IT", "ES", "NL"]
        while True:
            clear()
            x = int(input('''
    1) English
    2) Italiano
    3) Español
    4) Nederlands
    
    Select your language: '''))
            if 1 <= x <= len(lang_list):
                settings["language"] = lang_list[x - 1]
                save_file(json.dumps(settings), "data/settings.json")
                break

    with open("data/lang/lang_" + settings["language"] + ".json", "r", encoding="utf-8") as file:
        return json.load(file)


def range_calculator(number_of_client, raw_range):
    if raw_range is not None:
        try:
            first_ip = raw_range.split("-")[0]
            last_ip = raw_range.split("-")[1]
            first_ip_int = int(ipaddress.IPv4Address(first_ip))
            last_ip_int = int(ipaddress.IPv4Address(last_ip))

            difference = last_ip_int - first_ip_int
            diff_between_ip = int(difference / number_of_client)
            diff_between_ip_copy = diff_between_ip

            divided_range = [(str(first_ip) + "-" + str(ipaddress.IPv4Address(diff_between_ip + first_ip_int)))]

            for x in range(number_of_client - 1):
                range_string = str(ipaddress.IPv4Address(diff_between_ip + first_ip_int + 1)) + "-"
                diff_between_ip += diff_between_ip_copy
                if x == number_of_client - 2:
                    range_string += last_ip
                else:
                    range_string += str(ipaddress.IPv4Address(diff_between_ip + first_ip_int))
                divided_range.append(range_string)
            return divided_range
        except:
            pass
    return None


def range_parse(raw_address):
    address = None
    if raw_address.count("/") != 0:
        try:
            address_list = list(ipaddress.ip_network(raw_address).hosts())
            address = str(address_list[0]) + "-" + str(address_list[-1])
        except:
            pass
    elif raw_address.count(".") == 6 and raw_address.count("-") == 1:
        address = raw_address
    elif raw_address.count(".") == 3 and (raw_address.count("-") != 0 or raw_address.count("*") != 0):
        address_splitted = raw_address.split(".")
        adr1 = ""
        adr2 = ""
        for x in address_splitted:
            y = [x, x]
            if x.count("-") == 1:
                y = x.split("-")
            if x.count("*") == 1:
                y[0] = "0"
                y[1] = "255"
            if x != address_splitted[-1]:
                y[0] += "."
                y[1] += "."

            adr1 += y[0]
            adr2 += y[1]

        address = adr1 + "-" + adr2
    return address
