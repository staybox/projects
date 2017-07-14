# coding: utf8
from __future__ import print_function
import rfid
import argparse


def push(options):
    """
    for example:
    python pusher.py --do=remove_all --ip=10.66.0.123 --sn=123159516
    python pusher.py --do=add --rfid_id=444411 --ip=10.66.0.123 --sn=123159516
    etc...
    """
#to test password change, if password is '0' it's disabled. password can be max 6 digits; must be an 'integer'.
    try:
        do = options.do
        rfid_id = options.rfid_id
        ip = options.ip
        controller_serial = int(options.serial_number)
        do_list = ['add', 'remove', 'open', 'get_all_cards', 'remove_all', 'set_passwords']
        assert do in do_list, 'Change parameter "do"! It can be "add", "remove", "get_all_cards", "open", "remove_all" or "set_passwords"'
        client = rfid.RFIDClient(ip, controller_serial)

        if do == do_list[3]:
            pass

        else:
            card = rfid.ten_digit_to_comma_format(rfid_id) # rfid_id needs to be converted to "comma format"
            # print('rfid_id = ', rfid_id)
            # print('card number = ', card)
            if do == do_list[0]:
                client.add_user(card, [1]) # add privileges for door 1
                # print('added')
            elif do == do_list[1]:
                client.remove_user(card)
                # print('deleted')
            elif do == do_list[2]:
                client.open_door(1) # Open door 1
                # print('the door is opened')
            elif do == do_list[4]:
                client.remove_all() # remove all entries
                # print('all the entries has been removed')
            elif do == do_list[5]:
                pass_1 = options.pass_1
                pass_2 = options.pass_2
                pass_3 = options.pass_3
                pass_4 = options.pass_4
                client.set_passwords(pass_1, pass_2, pass_3, pass_4) # set 1 to 4 passwords with max 6 digits
                # print('password(s) has been changed')
        print ('true')
    except:
        print ('false')


def argparses():
    parser = argparse.ArgumentParser()
    parser.add_argument('--do', type=str, dest='do', help='remove, add, get card numbers, remove_all or set_passwords')
    parser.add_argument('--rfid_id', type=int, default=0, dest='rfid_id', help='rfid_id for adding to the box')
    parser.add_argument('--ip', type=str, dest='ip', help='ip of the box')
    parser.add_argument('--sn', type=str, dest='serial_number', help='serial number of the box')
    parser.add_argument('--pass_1', type=int, dest='pass_1', default = 0, help='password')
    parser.add_argument('--pass_2', type=int, dest='pass_2', default = 0, help='password')
    parser.add_argument('--pass_3', type=int, dest='pass_3', default = 0, help='password')
    parser.add_argument('--pass_4', type=int, dest='pass_4', default = 0, help='password')
    return parser


if __name__ == '__main__':
    parser = argparses()
    options = parser.parse_args()
    push(options)
