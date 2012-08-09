__synopsys__        = 'Expose  the SOAP interface of the Opinion Calculator' 
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
import AO_mOpinionWords



import logging

from rpclib.application import Application          # Application is the glue between one or more service definitions, interface and protocol choices.

from rpclib.decorator import srpc                   # The srpc decorator exposes methods as remote procedure calls and declares the data types it accepts
                                                    # and returns. The ‘s’ prefix is short for static. It means no implicit argument will be passed to
                                                    # the function. In the @rpc case, the function gets a rpclib.MethodContext instance as first argument.

from rpclib.interface.wsdl import Wsdl11            # We are going to expose the service definitions using the Wsdl 1.1 document standard. The methods will
from rpclib.protocol.soap import Soap11             # use Soap 1.1 protocol to communicate with the outside world. They’re instantiated and passed to the
                                                    # Application constructor. You need to pass fresh instances to each application instance

from rpclib.service import ServiceBase              # ServiceBase is the base class for all service definitions.

from rpclib.model.complex import Iterable           # The names of the needed types for implementing this service should be self-explanatory
from rpclib.model.primitive import Integer
from rpclib.model.primitive import String

from rpclib.server.wsgi import WsgiApplication      # Our server is going to use HTTP as transport, so we import the WsgiApplication from the
                                                    # server.wsgi module It’s going to wrap the application instance


# We start by defining our service. The class name will be made public in the wsdl document unless explicitly overridden
# with __service_name__ class attribute.

class opinionAnalisys_Service(ServiceBase):

    # The srpc decorator flags each method as a remote procedure call and defines the types and order of the soap parameters,
    # as well as the type of the return value. This method takes in a string and an integer and returns an iterable of strings, just like that:
    @srpc(String,  _returns=Iterable(String))

    # The method itself has nothing special about it whatsoever. All input variables and return types are standard python objects:
    def opinionAssesmentRequest(AO_sDocument):

       # Analyse the document
        AO_lOpinion = AO_mOpinionWords.AO_lAssessOpinion(AO_sDocument)

        for j in range(0,len(AO_lOpinion)):
            yield str(AO_lOpinion[j])


# Now that we have defined our service, we are ready to share it with the outside world.
# We are going to use the ubiquitious Http protocol as a transport, using a Wsgi-compliant http server.
# This example uses Python’s stock simple wsgi web server. Rpclib has been tested with several other web servers.
# Any WSGI-compliant server should work.

# This is the required import:
if __name__=='__main__':
    try:
        from wsgiref.simple_server import make_server
    except ImportError:
        print "Error: example server code requires Python >= 2.5"

    # Here, we configure the python logger to show debugging output. We have to specifically enable the debug output from the soap handler.
    # That’s because the xml formatting code is run only when explicitly enabled for performance reasons
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('rpclib.protocol.xml').setLevel(logging.DEBUG)

    # We glue the service definition, interface document and input and output protocols under the targetNamespace ‘rpclib.examples.hello.soap’:
    application = Application([opinionAnalisys_Service], 'rpclib.examples.hello.soap', interface=Wsdl11(), in_protocol=Soap11(), out_protocol=Soap11())

    # We then wrap the rpclib application with its wsgi wrapper:
    wsgi_app = WsgiApplication(application)

    server = make_server('127.0.0.1', 7789, WsgiApplication(application))

    print "listening to http://127.0.0.1:7789"
    print "wsdl is at: http://localhost:7789/?wsdl"

    server.serve_forever()
