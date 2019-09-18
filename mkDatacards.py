 
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

    
    total_num_tags = nbinsX*nbinsY
    tag_names = ["tag_"+str(i) for i in range(total_num_tags)]
    
    num_bkg = 1
    bkg_names = ["bkg_"+str(i) for i in range(num_bkg)]
   
    num_sig = 1
    sig_names = ["sig_"+str(i) for i in range(num_sig)]
    
    
    
    print " tag_names = ", tag_names
    
    #
    # Write datacard: 
    #
    
    outputDirDatacard = "test"
   
    cardPath = outputDirDatacard + "/datacard" + "_mytest_" + ".txt"
    print "\n\n"
    print " Writing to " + cardPath 

    columndef = 10
 
    card = open( cardPath ,"w")
    
    card.write('## Shape input card\n')

    card.write('imax 1 number of channels\n')
    card.write('jmax * number of background\n')
    card.write('kmax * number of nuisance parameters\n') 
    
    card.write('-'*100+'\n')
    #card.write('bin         %s' % tagNameToAppearInDatacard+'\n')
    card.write('bin          ')
    for tag_name in tag_names :
      card.write((' %s ' % tag_name).ljust(columndef))      
    card.write('\n')

    #card.write('observation %.0f\n' % yieldsData['data'])
    card.write('observation    ')
    for ibinsX in range(nbinsX) :
      for ibinsY in range(nbinsY) :
        card.write((' %.0f ' % histo_data.GetBinContent(ibinsX+1, ibinsY+1)).ljust(columndef))
    card.write('\n')

    card.write('-'*100+'\n')
    card.write('bin       ')
    for ibinsX in range(nbinsX) :
      for ibinsY in range(nbinsY) :
        for sig_name in sig_names:
          card.write((' %s' % ("tag_"+str(ibinsX*nbinsY + ibinsY)) ).ljust(columndef))
        for bkg_name in bkg_names:
          card.write((' %s' % ("tag_"+str(ibinsX*nbinsY + ibinsY)) ).ljust(columndef))      
    card.write('\n')

    card.write('process   ')
    for ibinsX in range(nbinsX) :
      for ibinsY in range(nbinsY) :
        for sig_name in sig_names:
          card.write((' %s' % sig_name).ljust(columndef))
        for bkg_name in bkg_names:
          card.write((' %s' % bkg_name).ljust(columndef))      
    card.write('\n')

    card.write('process   ')
    for ibinsX in range(nbinsX) :
      for ibinsY in range(nbinsY) :
        for isig in range(num_sig):
          card.write((' %.0f ' % (0-isig)).ljust(columndef))
        for ibkg in range(num_bkg):
          card.write((' %.0f ' % (1+ibkg)).ljust(columndef))      
    card.write('\n')

    card.write('-'*100+'\n')


    card.write('rate      ')
    for ibinsX in range(nbinsX) :
      for ibinsY in range(nbinsY) :
        for isig in range(num_sig):
          card.write(((' %.3f ' % histo_sig.GetBinContent(ibinsX+1, ibinsY+1))).ljust(columndef))
        for ibkg in range(num_bkg):
          #
          # Use data as nominal values for background
          # This should have 0 effect on the result, since MC is going to be data-driven, but will help in the asimov (maybe?), if alpha, beta, ... are not used in the asimov ...
          #
          card.write(((' %.0f ' % histo_data.GetBinContent(ibinsX+1, ibinsY+1))).ljust(columndef))     
    card.write('\n')

    card.write('-'*100+'\n')




#-------                                         
#bin                   B      C       D        A   
#process               bkg    bkg     bkg      bkg 
#process               1      1       1         1   
#rate                  1      1       1         1   
#-------                                         

    #
    # ... and now the "model" part for the data driven estimation
    #
    #
    
#    
#alpha rateParam A bkg (@0*@1/@2) beta,gamma,delta
#beta  rateParam B bkg 50
#gamma rateParam C bkg 100
#delta rateParam D bkg 500
#


#
#
#       ^      ^
#       | \    |
#       |  \   |
#       |   \  |
#       |    \ |
#
#
#      For a fixed "x" move along "y", then move right on "x"     
#      
#      Signal is "expected" in the bottom right corner (although the model is generic enough that it should work)
#
#

#
# The way it works, the model should hold for every background independently
# If only one background considered, it falls back to standard ABCD method
#

#
#    tag_names = ["tag_"+str(i) for i in range(total_num_tags)]
#
#
#   bin        tag_0     tag_0     tag_1     tag_1     tag_2     tag_2     tag_3     tag_3    
#
#

    for ibinsY in range(nbinsY) :
      if (ibinsY != 0) :
        for bkg_name in bkg_names:
          card.write('alpha_%.0f rateParam A_%.0f %s (@0*@1/@2) beta_%.0f,gamma_%.0f,delta_%.0f \n ' % (ibinsY, ibinsY, bkg_name, ibinsY, ibinsY, ibinsY) )

    #for ibinsY in range(nbinsY) :
      #if (ibinsY != 0) :
        #for bkg_name in bkg_names:
          #card.write('alpha_%.0f rateParam A %s (@0*@1/@2) beta_%.0f,gamma_%.0f,delta_%.0f ', ibinsY, bkg_name, ibinsY, ibinsY, ibinsY)


        #card.write('alpha_%.0f rateParam A %s (@0*@1/@2) beta,gamma,delta ', bkg_name)
        
        
        
    #for tag_name in tag_names :






    card.close()



    print "\n\n"
    