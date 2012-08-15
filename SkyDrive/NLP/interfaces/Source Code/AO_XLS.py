'# -*- coding: utf-8 -*-'
from __future__ import division

__Synopsys__    = 'Offer an Excle XLS interface to the Opinion Calculator Web service. Implant an opinion analisys in a spreadsheet.' 
__author__      = 'Dr. Avner OTTENSOOSER'
__version__     = '$Revision: 0.01 $'
__email__       = 'avner.ottensooser@gmail.com'

AO_sSource      = "C:\Users\Avner\SkyDrive\NLP\TicketNLPWorks\Data\Excel\Book2.xls"
AO_sDestinatiom = "C:\Users\Avner\SkyDrive\NLP\TicketNLPWorks\Data\Excel\Book2 - NLP.xls"

# the two excle pakages
from xlrd import open_workbook,cellname
from xlwt import Workbook

# suds allow us to call a web service
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

    # try open the source spreadsheet
    try:
        AO_xlsSourceBook = open_workbook(AO_sSource)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        raise
    
    # open the destination spreadsheet
    AO_xlsDestinationBook = Workbook()

    # for the two sheets in the source 
    for k in range (0,2):

        # find a worksheet
        AO_xlsSourceSeet  = AO_xlsSourceBook.sheet_by_index(k)

        # create a new corseponding worksheet with the same name
        AO_xlsDestinationSeet = AO_xlsDestinationBook.add_sheet(AO_xlsSourceSeet.name)
        
        # for all the rows in the source workseet
        for row_index in range(AO_xlsSourceSeet.nrows):

            # for all the colouns in source the worksheet
            for col_index in range(AO_xlsSourceSeet.ncols):

                # Add a cell to the destination worksheet
                AO_xlsDestinationSeet.write(row_index, col_index, AO_xlsSourceSeet.cell(row_index,col_index).value)

                # if the cell has oinion, analyse it
                if col_index == 1:
                    AO_lOpinion=  AO_client.service.opinionAssesmentRequest(AO_xlsSourceSeet.cell(row_index,col_index).value)[0]

            # finaly place the analisys as the last columns in the row, but ignore the last one parameter which is too verbus        
            for j in range(0,len(AO_lOpinion)-1):
                AO_xlsDestinationSeet.write(row_index, col_index +1+ j,AO_lOpinion[j])
    
    # abnd when you finished the last cell in the last sheet, try to save the destination WorkBook
    try:
        AO_xlsDestinationBook.save(AO_sDestinatiom)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        raise
    
if __name__ == '__main__':
    main()
