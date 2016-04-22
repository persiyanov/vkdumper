import utils
import codecs
import argparse
import time
import sys

parser = argparse.ArgumentParser(description="Script for dumping specified dialog from VK. "
                                             "Set --user_id to your friend's VK id")

parser.add_argument("--user_id", help="friend VK id", type=int)
parser.add_argument("--out", help="output file", type=str, default="vkdump.txt")

APPLICATION_ID = <TYPE_YOUR_APP_ID_HERE> # 7-digits number


def get_messages_with(api, user_id):
    # Response has format: [<int_total_messages>, {<json_message>}, {<json_message>},...]
    response = api.messages.getHistory(offset=0, count=200, user_id=user_id, rev=1)
    total_messages = response[0]
    print "Total: %d" % total_messages
    messages = response[1:]
    offset = 200
    while offset <= total_messages:
        # Sleep for avoiding API blocks.
        time.sleep(0.3)

        # Tracking information
        sys.stdout.write("\rDone: {0} ({1}%)".format(offset, float(offset) / total_messages * 100))
        sys.stdout.flush()

        response = api.messages.getHistory(offset=offset, count=200, user_id=user_id, rev=1)
        messages.extend(response[1:])
        offset += 200
    sys.stdout.write('\n')
    return messages


def write_messages(messages, fname):
    with codecs.open(fname, 'w', encoding='utf8') as f:
        # Message format:
        # {u'body': u'140\u0440', u'uid': 19255756, u'mid': 877596, u'date': 1448724424,
        # u'out': 0, u'read_state': 1, u'from_id': 19255756}
        i = 0
        total_messages = len(messages)
        while i < total_messages:
            user_id = messages[i]['from_id']
            f.write(str(user_id) + ':\n')

            j = i
            while j < total_messages and messages[j]['from_id'] == user_id:
                f.write(messages[j]['body'] + '\n')
                j += 1
            i = j
            f.write('\n')


if __name__ == '__main__':
    args = parser.parse_args()

    # Reading credentials and authenticating
    login = str(raw_input("VK Login: "))
    passwd = utils.read_passwd("Password: ")
    api = utils.get_api(APPLICATION_ID, login, passwd)
    print "Authenticated"

    # Downloading all messages in dialog
    messages = get_messages_with(api, args.user_id)

    print "Writing messages to file '{0}'".format(args.out)
    write_messages(messages, args.out)
