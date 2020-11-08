import argparse
import typing
import requests


def parse_argument():
    """
    Parse entrypoint arguments
    :return:
    """
    parser = argparse.ArgumentParser(description="Console tool for get IP address info",
                                     usage="getip 8.8.8.8",
                                     epilog="GitHub repo: https:github.com/masterbpro/getip")
    parser.add_argument('-ip',
                        help='ip address in IPv4 format ',
                        default="self",
                        metavar='')
    return parser.parse_args()


def get_my_ip() -> str:
    """
    Receive current global host IP
    :return: Host global IP address
    """
    res = requests.get("https://ramziv.com/ip")
    if res.status_code != 200:
        raise requests.exceptions.ConnectionError
    return res.text


def get_ip_info(ip_address: str) -> dict:
    """
    Get info about IP
    :param ip_address: Global IPv4 address
    :return: Information about IP
    """
    res = requests.get(url=f"http://ip-api.com/json/{ip_address}",
                       params={"fields": "status,message,country,countryCode,"
                                         "city,lat,lon,timezone,"
                                         "reverse,queryclear,proxy"
                               }
                       )
    if res.status_code != 200:
        raise requests.exceptions.ConnectionError
    return res.json()


def check_answer_status(service_answer: dict) -> typing.Union[bool, dict]:
    """
    Check API service answer
    :param service_answer:
    :return:
    """
    if service_answer.get("status") == "success":
        service_answer.pop("status")
        return service_answer
    elif service_answer.get("message") == "reserved range":
        return {"[!]": "Reserved IPv4 range"}
    else:
        return {"[!]": "Invalid query, please check your input data"}


def main():
    """
    Entrypoint of program
    :return:
    """
    user_data = parse_argument()
    try:
        ip_address = user_data.ip if user_data.ip != "self" else get_my_ip()
        res_data = get_ip_info(ip_address)
    except requests.exceptions.ConnectionError:
        print("[!]: Please check your Internet connection, and try again")
    except requests.exceptions.InvalidSchema:
        print("[!]: Core error, please contact the developer for fix bug")
    except KeyboardInterrupt:
        print("[!] Thank for using this program, exiting...")
    else:
        check_data = check_answer_status(res_data)
        for key, value in check_data.items():
            print(f"{key.capitalize()}: {value}")