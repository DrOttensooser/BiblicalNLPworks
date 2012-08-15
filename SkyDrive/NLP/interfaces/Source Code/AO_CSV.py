'# -*- coding: utf-8 -*-'
from __future__ import division

__Synopsys__    = 'Offer an Excle CSV interface to the Opinion Calculator Web service' 
__author__      = 'Dr. Avner OTTENSOOSER'
__version__     = '$Revision: 0.01 $'
__email__       = 'avner.ottensooser@gmail.com'

AO_ROOT_PATH    = 'C:\\Users\\Avner\\SkyDrive\\NLP\\'
AO_PROJECT_NAME = 'interfaces'
AO_DATABASE     = AO_ROOT_PATH + AO_PROJECT_NAME + '\\Data\\Database\\flaskr.db'
AO_sSource      = 'C:\Users\Avner\SkyDrive\NLP\TicketNLPWorks\Data\CSV\Why The LTR Score.csv'
AO_sProcessed   = 'C:\Users\Avner\SkyDrive\NLP\TicketNLPWorks\Data\CSV\Why The LTR ScoreP.csv'


import codecs
from suds.client import Client
try:
    AO_client = Client('http://localhost:7789/?wsdl')
except urllib2.URLError:
    print "Cannot establish connecttion with SOAP server. Please ensure that the SOAP server is running and start again."
    raise SystemExit
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise

def main():

    AO_iIndet = 0
    AO_sPhrase = ''

    try:
        AO_fInput    = codecs.open(AO_sSource,  'r', encoding='utf-8')
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        raise

    try:
        AO_fOut      = codecs.open(AO_sProcessed,        'w', encoding='utf-8')
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        raise
    

    
    # for all the lines in the Documente 
    for line in AO_fInput:
        # remove whight space
        line = line.strip()
        AO_lOpinion=  AO_client.service.opinionAssesmentRequest(line)[0]
            
        for j in range(0,len(AO_lOpinion)):
            line = line + ',' + str(AO_lOpinion[j])

        AO_fOut.write(line)
        AO_fOut.write('\n')
    AO_fInput.close
    AO_fOut.close

if __name__ == '__main__':
   
    main()
