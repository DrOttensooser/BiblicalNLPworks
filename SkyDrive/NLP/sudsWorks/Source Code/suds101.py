'# -*- coding: utf-8 -*-'
from __future__ import division

__synopsys__        = 'Call  the SOAP interface to the Opinion Calculator' 
__author__          = 'Dr. Avner OTTENSOOSER'
__version__         = '$Revision: 0.01 $'
__email__           = 'avner.ottensooser@gmail.com'

AO_ROOT_PATH        = 'C:/Users/Avner/SkyDrive/NLP/'
AO_PROJECT_NAME     = 'sudsWorks'
AO_sCommonPath      =  AO_ROOT_PATH + 'CommonWorks/'
AO_sCommonCode      =  AO_sCommonPath + 'Source Code'
AO_sHost            =  'file://localhost/'
AO_wsdl_url         =  AO_sHost + AO_ROOT_PATH + AO_PROJECT_NAME +'/Source Code/OpinionWorks.WSDL' 

# import the NLPworks opinion analuser
import sys
sys.path.append(AO_sCommonCode)
#import AO_mOpinionWords

# The suds package use the Python standard lib logging package: all messages are at level DEBUG or ERROR.
# To register a console handler you can use basicConfig:
import logging
logging.basicConfig(level=logging.INFO)

# Once the console handler is configured, the user can enable module specific debugging doing the following:
# logging.getLogger(<desired package>).setLevel(logging.<desired-level>) A common example (show sent/received soap messages):

logging.getLogger('suds.client').setLevel(logging.DEBUG)

from suds.xsd.doctor import Import, ImportDoctor
schema_import = Import(AO_wsdl_url)
schema_doctor = ImportDoctor(schema_import)
                    
from suds.client import Client
client = Client(url=AO_wsdl_url,doctor=schema_doctor)
client.opinionAnalisys_Service.assessOpinion("The fat cat sat on teh mat")


# Commands/prefixes that don't modify the configuration on the device.
READONLY_COMMANDS = ('login', 'logout', 'get', 'save',)


__all__ = ['API', 'InteractionError']


class InteractionError(Exception):
    """Generic API error"""

class API(object):
    """
    Pass any kwargs to init that you would to the suds.client.Client constructor.
    A little bit of magic is performed with the ImportDoctor to cover missing
    types used in the WSDL.

        * If you specify wsdl, this file will be pulled from the default http URL
        * If you specify wsdl_url, it will override the wsdl file. Local
         "file://" URLs work just fine.
        * If you do not specify autosave, it will be enabled by default for
          volatile operations.

    To save time for re-usable code, it is a good idea subclassing this to
    create methods for commonly used commands in your application. Example::

        class MyAPI(netscaler.API):

            def change_password(self, username, newpass):
                return self.run("setsystemuser_password",
                    username=username, password=newpass)

    """
    def __init__(self, host=None, wsdl_url=None, soap_url=None,
                 wsdl=AO_wsdl_url, autosave=True, **kwargs):
        """
        Creates the suds.client.Client object and loads the WSDL.

        Pass autosave=False to disable the auto-save feature.
        """
        self.host = host
        self.wsdl = wsdl
        self.wsdl_url = wsdl_url or "http://%s/api/%s" % (self.host, self.wsdl)
        self.soap_url = soap_url or "http://%s/soap/" % self.host
        self.autosave = autosave

        # Fix missing types with ImportDoctor, otherwise we get:
        # suds.TypeNotFound: Type not found: '(Array, # http://schemas.xmlsoap.org/soap/encoding/, )
        self._import = Import('http://schemas.xmlsoap.org/soap/encoding/')
        self._import.filter.add("urn:NSConfig")
        self.doctor = ImportDoctor(self._import)

        for key, value in kwargs.items():
            # set attributes, but don't reset explicit ones.
            if not hasattr(self, key):
                if DEBUG: print "setting %s to %s" % (key, value)
                setattr(self, key, value)

        if DEBUG:
            print 'wsdl_url:', self.wsdl_url
            print 'soap_url:', self.soap_url

        self.client = Client(self.wsdl_url, doctor=self.doctor, location=self.soap_url, **kwargs)
        self.config_changed = False
        self.logged_in = False

    def __repr__(self):
        return u'<NetScaler:API host:%s user:%s logged_in:%s>' % (self.host,
                                                                  self.username,
                                                                  self.logged_in)

    def __str__(self):
        """Print me!"""
        return str(self.client)

    @property
    def service(self):
        return self.client.service

    def is_readonly(self, cmd):
        """Validates whether a command is read-only based on READONLY_COMMANDS"""
        ret = False
        for ROC in READONLY_COMMANDS:
            if cmd.startswith(ROC):
                    ret = True
        return ret

    def login(self):
        """Performs API login."""
        resp = self.client.service.login(username=self.username, password=self.password)
        if resp.rc != 0:
            raise InteractionError(resp.message)

        if DEBUG: print resp.message
        self.logged_in = True

        return True

    def logout(self):
        """Performs API logout."""
        resp = self.client.service.logout()
        if resp.rc != 0:
            raise InteractionError(resp.message)

        if DEBUG: print resp.message
        self.logged_in = False

        return True

    def save(self):
        """Saves NS Config."""
        resp = self.client.service.savensconfig()
        if resp.rc != 0:
            raise InteractionError(resp.message)

        if DEBUG: print resp.message

        return True

    def run(self, command, **kwargs):
        """
        Runs the equivalent of self.client.service.command(**kwargs).

        Will perform login() if self.logged_in == False.
        Will perform save() on volatile operations if self.autosave == True.
        """
        if not self.logged_in:
            if DEBUG: print 'not logged in; logging you in.'
            _login = self.login()

        resp = getattr(self.client.service, command)(**kwargs)
        if resp.rc != 0:
            raise InteractionError(resp.message)

        # Set this whenever a command is not read-only
        if not self.is_readonly(command):
            if DEBUG: print 'config changed; consider saving!'
            self.config_changed = True

        # Auto save if command changes config
        if self.autosave and self.config_changed:
            if DEBUG: print 'config changed; autosaving.'
            self.save()

        return resp
