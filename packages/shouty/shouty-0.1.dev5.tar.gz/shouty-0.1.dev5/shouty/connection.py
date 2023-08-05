import logging
import atexit
import ctypes.util
from ctypes import CDLL, c_int, c_char_p, c_void_p, c_size_t
from .enums import ShoutErr, Format, Protocol

logger = logging.getLogger(__name__)

so_file = ctypes.util.find_library('shout')

if not so_file:
    raise Exception('Library shout not found')

lib = CDLL(so_file)
lib.shout_init()
atexit.register(lib.shout_shutdown)


def check_error_code(f):
    def decorated(self, *args, **kwargs):
        err = f(self, *args, **kwargs)

        if err != ShoutErr.SUCCESS:
            err_name = ShoutErr(err).name

            lib.shout_get_error.restype = c_char_p
            lib.shout_get_error.argtypes = [c_void_p]
            err_str = lib.shout_get_error(self.obj).decode()

            raise Exception('Failed {}\nError code: {}\nError description: {}'
                            .format(f.__name__,
                                    err_name, err_str))
    return decorated


class Connection:
    def __init__(self, **kwargs):
        logger.debug('Init connection')

        lib.shout_new.restype = c_void_p
        self.obj = lib.shout_new()
        if not self.obj:
            raise Exception('Memory error')

        self.set_params(**kwargs)

        lib.shout_open.argtypes = [c_void_p]
        lib.shout_send.argtypes = [c_void_p, c_char_p, c_size_t]
        lib.shout_sync.argtypes = [c_void_p]
        lib.shout_close.argtypes = [c_void_p]
        lib.shout_free.argtypes = [c_void_p]

    def set_params(self,
                   host='localhost', port=8000,
                   user='source', password='',
                   protocol=Protocol.HTTP,
                   format=Format.OGG,
                   mount='/shouty',
                   dumpfile=None, agent=None,
                   public=0,
                   name=None, url=None, genre=None, description=None,
                   audio_info=None):

        self.set_int(lib.shout_set_port, port)
        self.set_str(lib.shout_set_host, host)

        self.set_str(lib.shout_set_user, user)
        self.set_str(lib.shout_set_password, password)

        self.set_int(lib.shout_set_protocol, protocol)
        self.set_int(lib.shout_set_format, format)
        self.set_str(lib.shout_set_mount, mount)

        self.set_optional_str(lib.shout_set_dumpfile, dumpfile)
        self.set_optional_str(lib.shout_set_agent, agent)

        self.set_int(lib.shout_set_public, public)

        self.set_optional_str(lib.shout_set_name, name)
        self.set_optional_str(lib.shout_set_url, url)
        self.set_optional_str(lib.shout_set_genre, genre)
        self.set_optional_str(lib.shout_set_description, description)

        lib.shout_set_audio_info.argtypes = [c_void_p, c_char_p, c_char_p]
        if audio_info:
            for k, v in audio_info.items():
                self.set_audio_info(k, v)

    @check_error_code
    def set_str(self, f, s):
        f.argtypes = [c_void_p, c_char_p]
        return f(self.obj, s.encode('ascii'))

    @check_error_code
    def set_int(self, f, n):
        f.argtypes = [c_void_p, c_int]
        return f(self.obj, n)

    def set_optional_str(self, f, s):
        if s:
            self.set_str(f, s)

    @check_error_code
    def set_audio_info(self, name, value):
        return lib.shout_set_audio_info(self.obj,
                                        name.encode('ascii'),
                                        value.encode('ascii'))

    @check_error_code
    def open(self):
        logger.debug('Open connection')
        return lib.shout_open(self.obj)

    @check_error_code
    def send(self, chunk):
        return lib.shout_send(self.obj, chunk, len(chunk))

    def sync(self):
        return lib.shout_sync(self.obj)

    @check_error_code
    def close(self):
        logger.debug('Close connection')
        return lib.shout_close(self.obj)

    def send_file(self, file_name):
        logger.debug('Sending: ' + file_name)
        self.set_int(lib.shout_set_format, Format.OGG)
        with open(file_name, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break

                self.send(chunk)
                self.sync()

    def free(self):
        logger.debug('Free library')
        lib.shout_free(self.obj)
