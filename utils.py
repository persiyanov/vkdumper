import getpass
import vk


def read_passwd(msg):
    return getpass.getpass(msg)


def get_api(app_id, login, passwd):
    session = vk.AuthSession(app_id, login, passwd, scope='messages')
    return vk.API(session)