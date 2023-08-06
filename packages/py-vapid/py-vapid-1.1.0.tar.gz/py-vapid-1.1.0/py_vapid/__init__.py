# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import logging
import binascii
import base64
import time
import hashlib

import ecdsa
from jose import jws

# Show compliance version. For earlier versions see previously tagged releases.
VERSION = "VAPID-DRAFT-02/ECE-DRAFT-07"


def b64urldecode(data):
    """Decodes an unpadded Base64url-encoded string."""
    return base64.urlsafe_b64decode(data + "===="[:len(data) % 4])


def b64urlencode(bstring):
    return binascii.b2a_base64(
        bstring).decode('utf8').replace('\n', '').replace(
        '+', '-').replace('/', '_').replace('=', '')


class VapidException(Exception):
    """An exception wrapper for Vapid."""
    pass


class Vapid01(object):
    """Minimal VAPID Draft 01 signature generation library.

    https://tools.ietf.org/html/draft-ietf-webpush-vapid-01

    """
    _private_key = None
    _public_key = None
    _curve = ecdsa.NIST256p
    _hasher = hashlib.sha256
    _schema = "WebPush"

    def __init__(self, private_key=None):
        """Initialize VAPID with an optional private key.

        :param private_key: A private key object
        :type private_key: ecdsa.SigningKey

        """
        self.private_key = private_key

    @classmethod
    def from_raw(cls, private_key):
        """Initialize VAPID using a private key point in "raw" or
        "uncompressed" form.

        :param private_key: A private key point in uncompressed form.
        :type private_key: str

        """
        key = ecdsa.SigningKey.from_string(b64urldecode(private_key),
                                           curve=cls._curve,
                                           hashfunc=cls._hasher)
        return cls(key)

    @classmethod
    def from_pem(cls, private_key):
        """Initialize VAPID using a private key in PEM format.

        :param private_key: A private key in PEM format.
        :type private_key: str

        """
        key = ecdsa.SigningKey.from_pem(private_key)
        return cls(key)

    @classmethod
    def from_der(cls, private_key):
        """Initialize VAPID using a private key in DER format.

        :param private_key: A private key in DER format and Base64-encoded.
        :type private_key: str

        """
        key = ecdsa.SigningKey.from_der(base64.b64decode(private_key))
        return cls(key)

    @classmethod
    def from_file(cls, private_key_file=None):
        """Initialize VAPID using a file containing a private key in PEM or
        DER format.

        :param private_key_file: Name of the file containing the private key
        :type private_key_file: str

        """
        if not os.path.isfile(private_key_file):
            vapid = cls()
            vapid.save_key(private_key_file)
            return vapid
        private_key = open(private_key_file, 'r').read()
        vapid = None
        try:
            if "BEGIN EC" in private_key:
                vapid = cls.from_pem(private_key)
            else:
                vapid = cls.from_der(private_key)
        except Exception as exc:
            logging.error("Could not open private key file: %s", repr(exc))
            raise VapidException(exc)
        return vapid

    @property
    def private_key(self):
        """The VAPID private ECDSA key"""
        if not self._private_key:
            raise VapidException(
                "No private key defined. Please import or generate a key.")
        return self._private_key

    @private_key.setter
    def private_key(self, value):
        """Set the VAPID private ECDSA key

        :param value: the byte array containing the private ECDSA key data
        :type value: bytes

        """
        self._private_key = value
        self._public_key = None

    @property
    def public_key(self):
        """The VAPID public ECDSA key

        The public key is currently read only. Set it via the `.private_key`
        method.

        """
        if not self._public_key:
            self._public_key = self.private_key.get_verifying_key()
        return self._public_key

    def generate_keys(self):
        """Generate a valid ECDSA Key Pair."""
        self.private_key = ecdsa.SigningKey.generate(curve=self._curve)

    def save_key(self, key_file):
        """Save the private key to a PEM file.

        :param key_file: The file path to save the private key data
        :type key_file: str

        """
        file = open(key_file, "wb")
        if not self._private_key:
            self.generate_keys()
        file.write(self._private_key.to_pem())
        file.close()

    def save_public_key(self, key_file):
        """Save the public key to a PEM file.
        :param key_file: The name of the file to save the public key
        :type key_file: str

        """
        with open(key_file, "wb") as file:
            file.write(self.public_key.to_pem())
            file.close()

    def validate(self, validation_token):
        """Sign a Valdiation token from the dashboard

        :param validation_token: Short validation token from the dev dashboard
        :type validation_token: str
        :returns: corresponding token for key verification
        :rtype: str

        """
        sig = self.private_key.sign(
            validation_token,
            hashfunc=self._hasher)
        verification_token = base64.urlsafe_b64encode(sig)
        return verification_token

    def verify_token(self, validation_token, verification_token):
        """Internally used to verify the verification token is correct.

        :param validation_token: Provided validation token string
        :type validation_token: str
        :param verification_token: Generated verification token
        :type verification_token: str
        :returns: Boolean indicating if verifictation token is valid.
        :rtype: boolean

        """
        hsig = base64.urlsafe_b64decode(verification_token)
        return self.public_key.verify(hsig, validation_token,
                                      hashfunc=self._hasher)

    def _base_sign(self, claims):
        if not claims.get('exp'):
            claims['exp'] = str(int(time.time()) + 86400)
        if not claims.get('sub'):
            raise VapidException(
                "Missing 'sub' from claims. "
                "'sub' is your admin email as a mailto: link.")
        return claims

    def sign(self, claims, crypto_key=None):
        """Sign a set of claims.
        :param claims: JSON object containing the JWT claims to use.
        :type claims: dict
        :param crypto_key: Optional existing crypto_key header content. The
            vapid public key will be appended to this data.
        :type crypto_key: str
        :returns: a hash containing the header fields to use in
            the subscription update.
        :rtype: dict

        """
        claims = self._base_sign(claims)
        sig = jws.sign(claims, self.private_key, algorithm="ES256")
        pkey = 'p256ecdsa='
        pubkey = self.public_key.to_string()
        if len(pubkey) == 64:
            pubkey = b'\04' + pubkey
        pkey += b64urlencode(pubkey)
        if crypto_key:
            crypto_key = crypto_key + ';' + pkey
        else:
            crypto_key = pkey

        return {"Authorization": "{} {}".format(self._schema, sig.strip('=')),
                "Crypto-Key": crypto_key}


class Vapid02(Vapid01):
    """Minimal Vapid 02 signature generation library

    https://tools.ietf.org/html/draft-ietf-webpush-vapid-02

    """
    _schema = "vapid"

    def sign(self, claims, crypto_key=None):
        claims = self._base_sign(claims)
        sig = jws.sign(claims, self.private_key, algorithm="ES256")
        pkey = self.public_key.to_string()
        # Make sure that the key is properly prefixed.
        if len(pkey) == 64:
            pkey = b'\04' + pkey
        return{
            "Authorization": "{schema} t={t},k={k}".format(
                schema=self._schema,
                t=sig,
                k=b64urlencode(pkey)
            )
        }


Vapid = Vapid01
