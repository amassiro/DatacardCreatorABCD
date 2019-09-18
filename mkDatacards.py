 
#!/usr/bin/env python

import json
import sys
argv = sys.argv
sys.argv = argv[:1]
import ROOT
import optparse


# _____________________________________________________________________________
def getHisto(fileIn, histoName):
     
     histo = fileIn.Get(histoName)
     print " histo in function = " , histo
     return histo


# _____________________________________________________________________________
if __name__ == '__main__':
    sys.argv = argv
    
    print '''
--------------------------------------------------------------------------------------------------
  __ \          |                                 |       \  |         |                
  |   |   _` |  __|   _` |   __|   _` |   __|  _` |      |\/ |   _` |  |  /   _ \   __| 
  |   |  (   |  |    (   |  (     (   |  |    (   |      |   |  (   |    <    __/  |    
 ____/  \__,_| \__| \__,_| \___| \__,_| _|   \__,_|     _|  _| \__,_| _|\_\ \___| _|    
                                                                                
--------------------------------------------------------------------------------------------------
'''    

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--inputHistoFile'   , dest='inputHistoFile'   , help='Name of the root file with the data histogram'           , default=None)
    parser.add_option('--dataHistoName'    , dest='dataHistoName'    , help='Name of the TH2F with data'                              , default=None)
    parser.add_option('--sigHistoName'     , dest='sigHistoName'     , help='Name of the TH2F with signal'                            , default=None)



    (opt, args) = parser.parse_args()

    ROOT.gROOT.SetBatch()


    print " inputHistoFile = ", opt.inputHistoFile
    print " dataHistoName  = ", opt.dataHistoName
    print " sigHistoName   = ", opt.sigHistoName
    
    print "\n\n"
    
    fileIn = ROOT.TFile.Open(opt.inputHistoFile)

    ROOT.TH1.SetDefaultSumw2(True)

    histo_data = getHisto(fileIn, opt.dataHistoName )
    histo_sig  = getHisto(fileIn, opt.sigHistoName )
    
    print "\n\n"
    
    print " histo_data = " , histo_data
    print " histo_sig  = " , histo_sig
    
    nbinsX = histo_data.GetNbinsX()
    nbinsY = histo_data.GetNbinsY()
    print "\n\n"
    
    print " nbinsX = " , nbinsX
    print " nbinsY = " , nbinsY

    
    #
    # Write datacard: 
    #
    
    outputDirDatacard = "test"
   
    cardPath = outputDirDatacard + "/datacard" + "_mytest_" + ".txt"
    print " Writing to " + cardPath 
 
    card = open( cardPath ,"w")



    print "\n\n"
    