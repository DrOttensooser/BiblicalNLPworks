'# -*- coding: utf-8 -*-'
from __future__ import division

__Synopsys__    = 'Offer an Excle XLS interface to the Opinion Calculator Web service' 
__author__      = 'Dr. Avner OTTENSOOSER'
__version__     = '$Revision: 0.01 $'
__email__       = 'avner.ottensooser@gmail.com'

AO_sSource      = "C:\Users\Avner\SkyDrive\NLP\TicketNLPWorks\Data\Excel\Book2.xls"
AO_sDestinatiom = "C:\Users\Avner\SkyDrive\NLP\TicketNLPWorks\Data\Excel\Book2 - NLP.xls"


from xlrd import open_workbook,cellname
from xlwt import Workbook

import urllib2
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
    AO_xlsSourceBook = open_workbook(AO_sSource)
    AO_xlsDestinationBook = Workbook()

    for k in range (0,1):
        AO_xlsSourceSeet  = AO_xlsSourceBook.sheet_by_index(k)
        AO_xlsDestinationSeet = AO_xlsDestinationBook.add_sheet(AO_xlsSourceSeet.name)
        

        for row_index in range(AO_xlsSourceSeet.nrows):
            for col_index in range(AO_xlsSourceSeet.ncols):
                AO_xlsDestinationSeet.write(row_index, col_index, AO_xlsSourceSeet.cell(row_index,col_index).value)
                if col_index == 1:
                    AO_lOpinion=  AO_client.service.opinionAssesmentRequest(AO_xlsSourceSeet.cell(row_index,col_index).value)[0]
            for j in range(0,len(AO_lOpinion)-1):
                AO_xlsDestinationSeet.write(row_index, col_index +1+ j,AO_lOpinion[j])
    



    AO_xlsDestinationBook.save(AO_sDestinatiom)
if __name__ == '__main__':
    main()
