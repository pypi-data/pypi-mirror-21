import copy
import logging

from fedoidc import ClientMetadataStatement
from fedoidc import ProviderConfigurationResponse

from oic import oic, OIDCONF_PATTERN
from oic.exception import CommunicationError
from oic.exception import ParameterError
from oic.exception import ParseError
from oic.exception import RegistrationError
from oic.oauth2 import ErrorResponse
from oic.oauth2 import sanitize
from oic.oauth2.message import MissingRequiredAttribute
from oic.oic import RegistrationResponse

from fedoidc.operator import le_dict

try:
    from json import JSONDecodeError
except ImportError:  # Only works for >= 3.5
    _decode_err = ValueError
else:
    _decode_err = JSONDecodeError

logger = logging.getLogger(__name__)

__author__ = 'roland'


class Client(oic.Client):
    def __init__(self, client_id=None, ca_certs=None,
                 client_prefs=None, client_authn_method=None, keyjar=None,
                 verify_ssl=True, config=None, client_cert=None,
                 federation_entity=None, fo_priority=None):
        oic.Client.__init__(
            self, client_id=client_id, ca_certs=ca_certs,
            client_prefs=client_prefs, client_authn_method=client_authn_method,
            keyjar=keyjar, verify_ssl=verify_ssl, config=config,
            client_cert=client_cert)

        self.federation_entity = federation_entity
        self.fo_priority = fo_priority
        self.federation = ''
        self.provider_federations = None
        self.registration_federations = None

    def parse_federation_provider_info(self, resp, issuer):
        """

        :param resp: A MetadataStatement instance
        """
        ms_list = self.federation_entity.get_metadata_statement(
            resp, cls=ProviderConfigurationResponse)

        if not ms_list:  # No metadata statement that I can use
            raise ParameterError('No trusted metadata')

        # response is a list of metadata statements

        # At this point in time I may not know within which
        # federation I'll be working.
        if len(resp) == 1:
            ms = ms_list[0]
            self.handle_provider_config(ms, issuer)
            self.federation = ms.iss
        else:
            self.provider_federations = ms_list

    def parse_federation_registration(self, resp, issuer):
        """

        :param resp: A MetadataStatement instance or a dictionary
        :param issuer: who is supposed to be issuing this response
        """
        ms_list = self.federation_entity.get_metadata_statement(
            resp, cls=ClientMetadataStatement)

        if not ms_list:  # No metadata statement that I can use
            raise RegistrationError('No trusted metadata')

        # response is a list of registration infos

        # At this point in time I may not know within which
        # federation I'll be working.
        if len(ms_list) == 1:
            ms = ms_list[0]
            self.store_registration_info(ms)
            self.federation = ms.iss
        else:
            self.registration_federations = ms_list

    def handle_response(self, response, issuer, func, response_cls):
        err_msg = 'Got error response: {}'
        unk_msg = 'Unknown response: {}'

        if response.status_code in [200, 201]:
            resp = response_cls().deserialize(response.text, "json")

            # Some implementations sends back a 200 with an error message inside
            if resp.verify():  # got a proper response
                func(resp, issuer)
            else:
                resp = ErrorResponse().deserialize(response.text, "json")
                if resp.verify():
                    logger.error(err_msg.format(sanitize(resp.to_json())))
                    if self.events:
                        self.events.store('protocol response', resp)
                    raise RegistrationError(resp.to_dict())
                else:  # Something else
                    logger.error(unk_msg.format(sanitize(response.text)))
                    raise RegistrationError(response.text)
        else:
            try:
                resp = ErrorResponse().deserialize(response.text, "json")
            except _decode_err:
                logger.error(unk_msg.format(sanitize(response.text)))
                raise RegistrationError(response.text)

            if resp.verify():
                logger.error(err_msg.format(sanitize(resp.to_json())))
                if self.events:
                    self.events.store('protocol response', resp)
                raise RegistrationError(resp.to_dict())
            else:  # Something else
                logger.error(unk_msg.format(sanitize(response.text)))
                raise RegistrationError(response.text)

    def chose_federation(self, ms_list):
        """
        Given the set of possible provider info responses I got chose
        one. This simple one uses federation_priority if present.
        
        :param ms_list: List of metadata statements 
        :return: A ProviderConfigurationResponse instance
        """
        for fo in self.fo_priority:
            for ms in ms_list:
                if ms.iss == fo:
                    return ms

        return ms_list[0]

    def chose_provider_federation(self, issuer):
        _pcr = self.chose_federation(self.provider_federations)
        self.federation = _pcr.iss
        self.handle_provider_config(_pcr, issuer)
        return _pcr

    def chose_registration_federation(self):
        _pcr = self.chose_federation(self.registration_federations)
        self.federation = _pcr.iss
        self.store_registration_info(_pcr)
        return _pcr

    def provider_config(self, issuer, keys=True, endpoints=True,
                        response_cls=ProviderConfigurationResponse,
                        serv_pattern=OIDCONF_PATTERN):
        if issuer.endswith("/"):
            _issuer = issuer[:-1]
        else:
            _issuer = issuer

        url = serv_pattern % _issuer

        pcr = None
        r = self.http_request(url, allow_redirects=True)
        if r.status_code == 200:
            try:
                pcr = response_cls().from_json(r.text)
            except:
                _err_txt = "Faulty provider config response: {}".format(r.text)
                logger.error(sanitize(_err_txt))
                raise ParseError(_err_txt)

        if 'metadata_statements' not in pcr:
            if 'metadata_statement_uris' not in pcr:
                # Talking to a federation unaware OP
                self.store_response(pcr, r.text)
                self.handle_provider_config(pcr, issuer, keys, endpoints)
                return pcr

        # logger.debug("Provider info: %s" % sanitize(pcr))
        if pcr is None:
            raise CommunicationError(
                "Trying '%s', status %s" % (url, r.status_code))

        # 3 possible outcomes
        # a) No usable provider info -> Exception
        # b) Exactly one possible provider info to use
        # c) 2 or more usable provider info responses
        try:
            self.handle_response(r, _issuer,
                                 self.parse_federation_provider_info,
                                 ProviderConfigurationResponse)
        except RegistrationError as err:
            raise

        if self.provider_federations:
            return self.chose_provider_federation(_issuer)
        else:  # Otherwise there should be exactly one metadata statement I
            return self.provider_info

    def federated_client_registration_request(self, **kwargs):
        req = ClientMetadataStatement()

        try:
            req['redirect_uris'] = kwargs['redirect_uris']
        except KeyError:
            try:
                req["redirect_uris"] = self.redirect_uris
            except AttributeError:
                raise MissingRequiredAttribute("redirect_uris", kwargs)
        else:
            del kwargs['redirect_uris']

        req.update(kwargs)

        _fe = self.federation_entity
        if self.federation:
            _cms = _fe.create_metadata_statement_request(req)
            sms = _fe.signer.create_signed_metadata_statement(
                _cms, 'registration', fos=[self.federation])
            req['metadata_statements'] = [sms]
        else:
            _fos = list([r.iss for r in self.provider_federations])
            _cms = _fe.create_metadata_statement_request(copy.copy(req))
            sms = _fe.signer.create_signed_metadata_statement(
                _cms, 'registration', _fos)
            req['metadata_statements'] = [sms]

        return req

    def register(self, url, reg_type='federation', **kwargs):

        if reg_type == 'federation':
            req = self.federated_client_registration_request(**kwargs)
        else:
            req = self.create_registration_request(**kwargs)

        if self.events:
            self.events.store('Protocol request', req)

        headers = {"content-type": "application/json"}

        rsp = self.http_request(url, "POST", data=req.to_json(),
                                headers=headers)

        if reg_type == 'federation':
            self.handle_response(rsp, '', self.parse_federation_registration,
                                 RegistrationResponse)

            if self.registration_federations:
                return self.chose_registration_federation()
            else:  # Otherwise there should be exactly one metadata statement I
                return self.registration_response
        else:
            return self.handle_registration_info(rsp)
