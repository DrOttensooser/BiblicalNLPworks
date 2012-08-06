'# -*- coding: utf-8 -*-'
from __future__ import division

__synopsys__        = 'Offer a SOAP interface to the Opinion Calculator' 
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


