#!/usr/bin/env python3
import json
import os

from oic.utils.jwt import JWT
from oic.utils.keyio import KeyJar
from oic.utils.keyio import build_keyjar

from fedoidc.file_system import FileSystem


class JWKSBundle(object):
    """
    A class to keep a number of signing keys from different issuers.
    """

    def __init__(self, iss, sign_keys=None):
        self.iss = iss
        self.sign_keys = sign_keys  # These are my signing keys as a KeyJar
        self.bundle = {}

    def __setitem__(self, key, value):
        """

        :param key: issuer ID
        :param value: Supposed to be KeyJar or a JWKS (JSON document)
        """
        if not isinstance(value, KeyJar):
            kj = KeyJar()
            kj.import_jwks(value, issuer=key)
            value = kj
        else:
            _val = value.copy()
            _iss = list(_val.keys())
            if _iss == ['']:
                _val.issuer_keys[key] = _val.issuer_keys['']
                del _val.issuer_keys['']
            elif len(_iss) == 1:
                if _iss[0] != key:
                    _val.issuer_keys[key] = _val.issuer_keys[_iss[0]]
                    del _val.issuer_keys[_iss[0]]
            else:
                raise ValueError('KeyJar contains to many issuers')

            value = _val

        self.bundle[key] = value

    def __getitem__(self, item):
        """
        Returns a KeyJar instance representing the keys belonging to an
        issuer
        :param item: Issuer ID
        :return: A KeyJar instance
        """
        kj = self.bundle[item]
        if item not in list(kj.issuer_keys.keys()):
            kj.issuer_keys[item] = kj.issuer_keys['']
            del kj.issuer_keys['']

        return kj

    def __delitem__(self, key):
        """
        Remove the KeyJar that belong to a specific issuer
        :param key: Issuer ID
        """
        del self.bundle[key]

    def create_signed_bundle(self, sign_alg='RS256', iss_list=None):
        """
        Create a signed JWT containing a dictionary with Issuer IDs as keys
        and JWKSs as values
        :param sign_alg: Which algorithm to use when signing the JWT
        :return: A signed JWT
        """
        #data = json.dumps(self.dict(iss_list))
        data = self.dict(iss_list)
        _jwt = JWT(self.sign_keys, iss=self.iss, sign_alg=sign_alg)
        return _jwt.pack(bundle=data)

    def loads(self, jstr):
        """
        Upload a bundle from an unsigned JSON document

        :param jstr:
        :return:
        """
        if isinstance(jstr, dict):
            _info = jstr
        else:
            _info = json.loads(jstr)

        for iss, jwks in _info.items():
            kj = KeyJar()
            kj.import_jwks(jwks, issuer=iss)
            self.bundle[iss] = kj
        return self

    def dumps(self, iss_list=None):
        return json.dumps(self.dict(iss_list))

    def __str__(self):
        return json.dumps(self.dict())

    def keys(self):
        return self.bundle.keys()

    def items(self):
        return self.bundle.items()

    def dict(self, iss_list=None):
        _int = {}
        for iss, kj in self.bundle.items():
            if iss_list is None or iss in iss_list:
                try:
                    _int[iss] = kj.export_jwks(issuer=iss)
                except KeyError:
                    _int[iss] = kj.export_jwks()
        return _int

    def upload_signed_bundle(self, sign_bundle, ver_keys):
        jwt = verify_signed_bundle(sign_bundle, ver_keys)
        self.loads(jwt['bundle'])

    def as_keyjar(self):
        kj = KeyJar()
        for iss, k in self.bundle.items():
            kj.issuer_keys[iss] = k.issuer_keys[iss]
        return kj


def verify_signed_bundle(signed_bundle, ver_keys):
    """

    :param signed_bundle: A signed JWT where the body is a JWKS bundle
    :param ver_keys: Keys that can be used to verify signatures of the
        signed_bundle as a KeyJar.
    :return: The bundle or None
    """
    _jwt = JWT(ver_keys)
    return _jwt.unpack(signed_bundle)


def get_bundle(iss, ver_keys, bundle_file):
    fp = open(bundle_file, 'r')
    signed_bundle = fp.read()
    fp.close()
    return JWKSBundle(iss, None).upload_signed_bundle(signed_bundle, ver_keys)


def get_signing_keys(eid, keydef, key_file):
    """
    If the *key_file* file exists then read the keys from there, otherwise
    create the keys and store them a file with the name *key_file*.

    :param eid: The ID of the entity that the keys belongs to
    :param keydef: What keys to create
    :param key_file: A file name
    :return: A KeyJar instance
    """
    if os.path.isfile(key_file):
        kj = KeyJar()
        kj.import_jwks(json.loads(open(key_file, 'r').read()), eid)
    else:
        kj = build_keyjar(keydef)[1]
        # make it know under both names
        fp = open(key_file, 'w')
        fp.write(json.dumps(kj.export_jwks()))
        fp.close()
        kj.issuer_keys[eid] = kj.issuer_keys['']

    return kj


def jwks_to_keyjar(jwks):
    """

    :param jwks: String representation of a JWKS
    :return: A KeyJar instance
    """
    try:
        _jwks = json.loads(jwks)
    except json.JSONDecodeError:
        raise ValueError('No proper JWKS')
    kj = KeyJar()
    kj.import_jwks(_jwks, issuer='')
    return kj


def k_to_k(keyjar, private=False):
    k = list(keyjar.keys())
    if len(k) == 1:
        return json.dumps(keyjar.export_jwks(issuer=k[0], private=private))
    elif len(k) == 2 and '' in k:
        k.remove('')
        return json.dumps(keyjar.export_jwks(issuer=k[0], private=private))
    else:
        raise ValueError('Too many issuers')


def keyjar_to_jwks(keyjar):
    return k_to_k(keyjar)


def keyjar_to_jwks_private(keyjar):
    return k_to_k(keyjar, private=True)


class FSJWKSBundle(JWKSBundle):
    def __init__(self, iss, sign_keys=None, fdir='./', key_conv=None):
        JWKSBundle.__init__(self, iss, sign_keys=sign_keys)
        self.bundle = FileSystem(fdir, key_conv=key_conv,
                                 value_conv={'to': keyjar_to_jwks,
                                             'from': jwks_to_keyjar})
