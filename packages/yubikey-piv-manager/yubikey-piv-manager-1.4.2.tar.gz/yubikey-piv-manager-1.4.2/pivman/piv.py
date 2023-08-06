# Copyright (c) 2014 Yubico AB
# All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Additional permission under GNU GPL version 3 section 7
#
# If you modify this program, or any covered work, by linking or
# combining it with the OpenSSL project's OpenSSL library (or a
# modified version of that library), containing parts covered by the
# terms of the OpenSSL or SSLeay licenses, We grant you additional
# permission to convey the resulting work. Corresponding Source for a
# non-source form of such a combination shall include the source code
# for the parts of OpenSSL used as well as that of the covered work.

from pivman.libykpiv import YKPIV, ykpiv, ykpiv_state
from pivman.piv_cmd import YkPivCmd
from pivman import messages as m
from pivman.utils import der_read
from pivman.yubicommon.compat import text_type, int2byte
from ctypes import (POINTER, byref, create_string_buffer, sizeof, c_ubyte,
                    c_size_t, c_int)
from binascii import a2b_hex, b2a_hex
import re


_YKPIV_MIN_VERSION = b'1.2.0'

libversion = ykpiv.ykpiv_check_version(_YKPIV_MIN_VERSION)
if not libversion:
    raise Exception('libykpiv >= %s required' % _YKPIV_MIN_VERSION)


class DeviceGoneError(Exception):

    def __init__(self):
        super(DeviceGoneError, self).__init__(m.communication_error)


class PivError(Exception):

    def __init__(self, code):
        message = ykpiv.ykpiv_strerror(code)
        super(PivError, self).__init__(code, message)
        self.code = code
        self.message = message

    def __str__(self):
        return m.ykpiv.ykpiv_error_2 % (self.code, self.message)


class WrongPinError(ValueError):
    m_tries_1 = m.wrong_pin_tries_1
    m_blocked = m.pin_blocked

    def __init__(self, tries):
        super(WrongPinError, self).__init__(self.m_tries_1 % tries
                                            if tries > 0 else self.m_blocked)
        self.tries = tries

    @property
    def blocked(self):
        return self.tries == 0


class WrongPukError(WrongPinError):
    m_tries_1 = m.wrong_puk_tries_1
    m_blocked = m.puk_blocked


def check(rc):
    if rc == YKPIV.PCSC_ERROR:
        raise DeviceGoneError()
    elif rc != YKPIV.OK:
        raise PivError(rc)


def wrap_puk_error(error):
    match = TRIES_PATTERN.search(str(error))
    if match:
        raise WrongPukError(int(match.group(1)))
    raise WrongPukError(0)


KEY_LEN = 24
DEFAULT_KEY = a2b_hex(b'010203040506070801020304050607080102030405060708')

CERT_SLOTS = {
    '9a': YKPIV.OBJ.AUTHENTICATION,
    '9c': YKPIV.OBJ.SIGNATURE,
    '9d': YKPIV.OBJ.KEY_MANAGEMENT,
    '9e': YKPIV.OBJ.CARD_AUTH
}

ATTR_NAME = 'name'

TRIES_PATTERN = re.compile(r'now (\d+) tries')


class YkPiv(object):

    def __init__(self, verbosity=0, reader=None):
        self._cmd = YkPivCmd(verbosity=verbosity, reader=reader)

        self._state = POINTER(ykpiv_state)()
        if not reader:
            reader = 'Yubikey'

        self._chuid = None
        self._ccc = None
        self._pin_blocked = False
        self._verbosity = verbosity
        self._reader = reader
        self._certs = {}

        check(ykpiv.ykpiv_init(byref(self._state), self._verbosity))
        self._connect()
        self._read_status()

        if not self.chuid:
            try:
                self.set_chuid()
            except ValueError:
                pass  # Not autheniticated, perhaps?

        if not self.ccc:
            try:
                self.set_ccc()
            except ValueError:
                pass  # Not autheniticated, perhaps?

    def reconnect(self):
        check(ykpiv.ykpiv_disconnect(self._state))
        self._reset()

    def _connect(self):
        check(ykpiv.ykpiv_connect(self._state, self._reader.encode('utf8')))

        self._read_version()
        self._read_chuid()

    def _read_status(self):
        try:
            check(ykpiv.ykpiv_disconnect(self._state))
            data = self._cmd.run('-a', 'status')
            lines = data.splitlines()
            chunk = []
            while lines:
                line = lines.pop(0)
                if chunk and not line.startswith(b'\t'):
                    self._parse_status(chunk)
                    chunk = []
                chunk.append(line)
            if chunk:
                self._parse_status(chunk)
            self._status = data
        finally:
            self._reset()

    def _parse_status(self, chunk):
        parts, rest = chunk[0].split(), chunk[1:]
        if parts[0] == b'Slot' and rest:
            self._parse_slot(parts[1][:-1], rest)
        elif parts[0] == b'PIN':
            self._pin_blocked = parts[-1] == '0'

    def _parse_slot(self, slot, lines):
        slot = slot.decode('ascii')
        self._certs[slot] = dict(l.strip().split(b':\t', 1) for l in lines)

    def _read_version(self):
        v = create_string_buffer(10)
        check(ykpiv.ykpiv_get_version(self._state, v, sizeof(v)))
        self._version = v.value

    def _read_chuid(self):
        try:
            chuid_data = self.fetch_object(YKPIV.OBJ.CHUID)[29:29 + 16]
            self._chuid = b2a_hex(chuid_data)
        except PivError:  # No chuid set?
            self._chuid = None

    def _read_ccc(self):
        try:
            ccc_data = self.fetch_object(YKPIV.OBJ.CAPABILITY)[29:29 + 16]
            self._ccc = b2a_hex(ccc_data)
        except PivError:  # No ccc set?
            self._ccc = None

    def __del__(self):
        check(ykpiv.ykpiv_done(self._state))

    def _reset(self):
        self._connect()
        if self._cmd._pin is not None:
            self.verify_pin(self._cmd._pin)
        if self._cmd._key is not None:
            self.authenticate(a2b_hex(self._cmd._key))

    @property
    def version(self):
        return self._version

    @property
    def chuid(self):
        return self._chuid

    @property
    def ccc(self):
        return self._ccc

    @property
    def pin_blocked(self):
        return self._pin_blocked

    @property
    def certs(self):
        return dict(self._certs)

    def set_chuid(self):
        try:
            check(ykpiv.ykpiv_disconnect(self._state))
            self._cmd.set_chuid()
        finally:
            self._reset()

    def set_ccc(self):
        try:
            check(ykpiv.ykpiv_disconnect(self._state))
            self._cmd.run('-a', 'set-ccc')
        finally:
            self._reset()

    def authenticate(self, key=None):
        if key is None:
            key = DEFAULT_KEY
        elif len(key) != KEY_LEN:
            raise ValueError('Key must be %d bytes' % KEY_LEN)
        c_key = (c_ubyte * KEY_LEN).from_buffer_copy(key)
        check(ykpiv.ykpiv_authenticate(self._state, c_key))
        self._cmd._key = b2a_hex(key)
        if not self.chuid:
            self.set_chuid()

    def set_authentication(self, key):
        if len(key) != KEY_LEN:
            raise ValueError('Key must be %d bytes' % KEY_LEN)
        c_key = (c_ubyte * len(key)).from_buffer_copy(key)
        check(ykpiv.ykpiv_set_mgmkey(self._state, c_key))
        self._cmd._key = b2a_hex(key)

    def verify_pin(self, pin):
        if isinstance(pin, text_type):
            pin = pin.encode('utf8')
        buf = create_string_buffer(pin)
        tries = c_int(-1)
        rc = ykpiv.ykpiv_verify(self._state, buf, byref(tries))

        if rc == YKPIV.WRONG_PIN:
            if tries.value == 0:
                self._pin_blocked = True
                self._cmd._pin = None
            raise WrongPinError(tries.value)
        check(rc)
        self._cmd._pin = pin

    def set_pin(self, pin):
        if isinstance(pin, text_type):
            pin = pin.encode('utf8')
        if len(pin) > 8:
            raise ValueError(m.pin_too_long)
        try:
            check(ykpiv.ykpiv_disconnect(self._state))
            self._cmd.change_pin(pin)
        finally:
            self._reset()

    def reset_pin(self, puk, new_pin):
        if isinstance(new_pin, text_type):
            new_pin = new_pin.encode('utf8')
        if len(new_pin) > 8:
            raise ValueError(m.pin_too_long)
        if isinstance(puk, text_type):
            puk = puk.encode('utf8')
        try:
            check(ykpiv.ykpiv_disconnect(self._state))
            self._cmd.reset_pin(puk, new_pin)
        except ValueError as e:
            wrap_puk_error(e)
        finally:
            self._reset()
            self._read_status()

    def set_puk(self, puk, new_puk):
        if isinstance(puk, text_type):
            puk = puk.encode('utf8')
        if isinstance(new_puk, text_type):
            new_puk = new_puk.encode('utf8')
        if len(new_puk) > 8:
            raise ValueError(m.puk_too_long)

        try:
            check(ykpiv.ykpiv_disconnect(self._state))
            self._cmd.change_puk(puk, new_puk)
        except ValueError as e:
            wrap_puk_error(e)
        finally:
            self._reset()

    def reset_device(self):
        try:
            check(ykpiv.ykpiv_disconnect(self._state))
            self._cmd.run('-a', 'reset')
        finally:
            del self._cmd

    def fetch_object(self, object_id):
        buf = (c_ubyte * 4096)()
        buf_len = c_size_t(sizeof(buf))

        check(ykpiv.ykpiv_fetch_object(self._state, object_id, buf,
                                       byref(buf_len)))
        return b''.join(map(int2byte, buf[:buf_len.value]))

    def save_object(self, object_id, data):
        c_data = (c_ubyte * len(data)).from_buffer_copy(data)
        check(ykpiv.ykpiv_save_object(self._state, object_id, c_data,
                                      len(data)))

    def generate(self, slot, algorithm, pin_policy, touch_policy):
        try:
            check(ykpiv.ykpiv_disconnect(self._state))
            return self._cmd.generate(slot, algorithm, pin_policy, touch_policy)
        finally:
            self._reset()

    def create_csr(self, subject, pubkey_pem, slot):
        try:
            check(ykpiv.ykpiv_disconnect(self._state))
            return self._cmd.create_csr(subject, pubkey_pem, slot)
        finally:
            self._reset()

    def create_selfsigned_cert(self, subject, pubkey_pem, slot, valid_days=365):
        try:
            check(ykpiv.ykpiv_disconnect(self._state))
            return self._cmd.create_ssc(subject, pubkey_pem, slot, valid_days)
        finally:
            self._reset()

    def import_cert(self, cert_pem, slot, frmt='PEM', password=None):
        try:
            check(ykpiv.ykpiv_disconnect(self._state))
            return self._cmd.import_cert(cert_pem, slot, frmt, password)
        finally:
            self._reset()
            self._read_status()

    def import_key(self, cert_pem, slot, frmt, password, pin_policy,
                   touch_policy):
        try:
            check(ykpiv.ykpiv_disconnect(self._state))
            return self._cmd.import_key(cert_pem, slot, frmt, password,
                                        pin_policy, touch_policy)
        finally:
            self._reset()

    def sign_data(self, slot, hashed, algorithm=YKPIV.ALGO.RSA2048):
        c_hashed = (c_ubyte * len(hashed)).from_buffer_copy(hashed)
        buf = (c_ubyte * 4096)()
        buf_len = c_size_t(sizeof(buf))
        check(ykpiv.ykpiv_sign_data(self._state, c_hashed, len(hashed), buf,
                                    byref(buf_len), algorithm, int(slot, 16)))
        return ''.join(map(int2byte, buf[:buf_len.value]))

    def read_cert(self, slot):
        try:
            data = self.fetch_object(CERT_SLOTS[slot])
        except PivError:
            return None
        cert, rest = der_read(data, 0x70)
        zipped, rest = der_read(rest, 0x71)
        if zipped != b'\0':
            pass  # TODO: cert is compressed, uncompress.
        return cert

    def delete_cert(self, slot):
        if slot not in self._certs:
            raise ValueError('No certificate loaded in slot: %s' % slot)

        try:
            check(ykpiv.ykpiv_disconnect(self._state))
            self._cmd.delete_cert(slot)
            del self._certs[slot]
        finally:
            self._reset()
