 
#!/usr/bin/env python

import json
import sys
argv = sys.argv
sys.argv = argv[:1]
import ROOT
import optparse
import collections
import os.path

import math


# _____________________________________________________________________________
def getHisto(fileIn, histoName):
     
     histo = fileIn.Get(histoName)
     print (" histo in function = " , histo)
     return histo


def getHistos(fileIn, histoNameTemplate):
     
     histos = {}
     
     keys = fileIn.GetListOfKeys()
     
     for key in keys:
       print (" key = ", key)
       obj = key.ReadObj()
       if (obj.IsA().GetName() != "TProfile"
           and
           obj.InheritsFrom("TH2")
           and 
           obj.InheritsFrom("TH1")
           ) :
         if histoNameTemplate in obj.GetName():
           print (" found : ", obj.GetName() )
           histos[obj.GetName()] = obj
     
     return histos
         



# _____________________________________________________________________________
if __name__ == '__main__':
    sys.argv = argv
    
    print ('''
--------------------------------------------------------------------------------------------------
  __ \          |                                 |       \  |         |                
  |   |   _` |  __|   _` |   __|   _` |   __|  _` |      |\/ |   _` |  |  /   _ \   __| 
  |   |  (   |  |    (   |  (     (   |  |    (   |      |   |  (   |    <    __/  |    
 ____/  \__,_| \__| \__,_| \___| \__,_| _|   \__,_|     _|  _| \__,_| _|\_\ \___| _|    
                                                                                
--------------------------------------------------------------------------------------------------
''')    

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--inputHistoFile'           , dest='inputHistoFile'           , help='Name of the root file with the data histogram'                        , default=None)
    parser.add_option('--dataHistoName'            , dest='dataHistoName'            , help='Name of the TH2F with data'                                           , default=None)
    parser.add_option('--sigHistoName'             , dest='sigHistoName'             , help='Name of the TH2F with signal'                                         , default=None)
    parser.add_option('--sigHistoNameTemplate'     , dest='sigHistoNameTemplate'     , help='Name of the TH2F with signal template. the code will use all of them' , default=None)
    parser.add_option('--bkgHistoName'             , dest='bkgHistoName'             , help='Name of the TH2F with background, MC'                                 , default=None)
    parser.add_option('--nuisancesFile'            , dest='nuisancesFile'            , help='File where nuisances structure is defined'                            , default=None)

    (opt, args) = parser.parse_args()

    ROOT.gROOT.SetBatch()


    print (" inputHistoFile         = ", opt.inputHistoFile         )
    print (" dataHistoName          = ", opt.dataHistoName          )
    print (" sigHistoName           = ", opt.sigHistoName           )
    print (" sigHistoNameTemplate   = ", opt.sigHistoNameTemplate   )
    print (" bkgHistoName           = ", opt.bkgHistoName           )
    print (" nuisancesFile          = ", opt.nuisancesFile          )
    
    
    
    print ("\n\n")
    
    fileIn = ROOT.TFile.Open(opt.inputHistoFile)

    ROOT.TH1.SetDefaultSumw2(True)

    histo_data = getHisto(fileIn, opt.dataHistoName )
   
    if ( opt.sigHistoName != None ) :       
      histo_sig  = getHisto(fileIn, opt.sigHistoName )
      histos_sig[histo_sig.GetName()] = histo_sig
    else :
      print (" Use as signal: ", opt.sigHistoNameTemplate)
      histos_sig  = getHistos(fileIn, opt.sigHistoNameTemplate )
      
    if ( opt.bkgHistoName != None ) :       
      histo_bkg = getHisto(fileIn, opt.bkgHistoName )
    else :
      histo_bkg = getHisto(fileIn, opt.dataHistoName )
    
    print ("\n\n")
    
    print (" histo_data = " , histo_data            )
    print (" histos_sig size = " , len (histos_sig) )
    print (" histos_sig = " , histos_sig            )
    
    nbinsX = histo_data.GetNbinsX()
    nbinsY = histo_data.GetNbinsY()
    print ("\n\n")
    
    print (" nbinsX = " , nbinsX )
    print (" nbinsY = " , nbinsY )

    
    total_num_tags = nbinsX*nbinsY
    tag_names = ["tag_"+str(itag) for itag in range(total_num_tags)]
    
    num_bkg = 1
    bkg_names = ["bkg_"+str(ibkg) for ibkg in range(num_bkg)]
   
    num_sig = len(histos_sig)
    print (" num_sig = ", num_sig    )
    sig_names = [ list(histos_sig.values())[isig].GetName() for isig in range(num_sig)]
    #sig_names = ["sig_"+str(i) for i in range(num_sig)]
    
    print (" tag_names = ", tag_names )


    # Load the nuisances
    nuisances = collections.OrderedDict()
    if opt.nuisancesFile != None :
      if os.path.exists(opt.nuisancesFile) :
        handle = open(opt.nuisancesFile,'r')
        exec(handle.read())
        handle.close()

    
    #
    # Write datacard: 
    #
    
    outputDirDatacard = "test"
   
    cardPath = outputDirDatacard + "/datacard" + "_mytest" + ".txt"
    print ("\n\n"                       )
    print (" Writing to " + cardPath    )

    columndef = 15
    firstcolumndef = 30
 
    card = open( cardPath ,"w")
    
    card.write('## Shape input card\n')

    card.write('imax %d number of channels\n' % total_num_tags)
    card.write('jmax * number of background\n')
    card.write('kmax * number of nuisance parameters\n') 
    
    card.write('-'*100+'\n')
    #card.write('bin         %s' % tagNameToAppearInDatacard+'\n')
    card.write(('bin          ').ljust(firstcolumndef))
    for tag_name in tag_names :
      card.write((' %s ' % tag_name).ljust(columndef))      
    card.write('\n')

    #card.write('observation %.0f\n' % yieldsData['data'])
    card.write(('observation    ').ljust(firstcolumndef))
    for ibinsX in range(nbinsX) :
      for ibinsY in range(nbinsY) :
        #card.write((' %.0f ' % histo_data.GetBinContent(ibinsX+1, ibinsY+1)).ljust(columndef))
        if histo_data.GetBinContent(ibinsX+1, ibinsY+1) < 1 :
          card.write((' %.0f ' % math.ceil(histo_data.GetBinContent(ibinsX+1, ibinsY+1))).ljust(columndef))
        else :
          card.write((' %.0f ' % histo_data.GetBinContent(ibinsX+1, ibinsY+1)).ljust(columndef))
          
    card.write('\n')

    card.write('-'*100+'\n')
    card.write(('bin       ').ljust(firstcolumndef))
    for ibinsX in range(nbinsX) :
      for ibinsY in range(nbinsY) :
        for sig_name in sig_names:
          card.write((' %s' % ("tag_"+str(ibinsX*nbinsY + ibinsY)) ).ljust(columndef))
        for bkg_name in bkg_names:
          card.write((' %s' % ("tag_"+str(ibinsX*nbinsY + ibinsY)) ).ljust(columndef))      
    card.write('\n')

    card.write(('process   ').ljust(firstcolumndef))
    for ibinsX in range(nbinsX) :
      for ibinsY in range(nbinsY) :
        for sig_name in sig_names:
          card.write((' %s' % sig_name).ljust(columndef))
        for bkg_name in bkg_names:
          card.write((' %s' % bkg_name).ljust(columndef))      
    card.write('\n')

    card.write(('process   ').ljust(firstcolumndef))
    for ibinsX in range(nbinsX) :
      for ibinsY in range(nbinsY) :
        for isig in range(num_sig):
          card.write((' %.0f ' % (0-isig)).ljust(columndef))
        for ibkg in range(num_bkg):
          card.write((' %.0f ' % (1+ibkg)).ljust(columndef))      
    card.write('\n')

    card.write('-'*100+'\n')


    card.write(('rate      ').ljust(firstcolumndef))
    for ibinsX in range(nbinsX) :
      for ibinsY in range(nbinsY) :
        for isig in range(num_sig):
          #card.write(((' %.3f ' % histo_sig.GetBinContent(ibinsX+1, ibinsY+1))).ljust(columndef))
          card.write(((' %.3f ' % list(histos_sig.values())[isig].GetBinContent(ibinsX+1, ibinsY+1))).ljust(columndef))
        for ibkg in range(num_bkg):
          #
          # Use data as nominal values for background (if the specific background sample is not provided)
          # This should have 0 effect on the result, since MC is going to be data-driven, but will help in the asimov (maybe?), if alpha, beta, ... are not used in the asimov ...
          #
          # -> this actually should never happen, since using histo_data instead of histo_bkg is already set at the beginning
          #
          card.write(((' %.3f ' % histo_bkg.GetBinContent(ibinsX+1, ibinsY+1))).ljust(columndef))   
          #
          #print ( " Bkg[", ibinsX, "][", ibinsY, "] = ", histo_bkg.GetBinContent(ibinsX+1, ibinsY+1) )
          #
          # FIXME: removed (see motivation above)
          #if histo_bkg.GetBinContent(ibinsX+1, ibinsY+1) > 0 :
            #card.write(((' %.3f ' % histo_bkg.GetBinContent(ibinsX+1, ibinsY+1))).ljust(columndef))               
          #else :
            #card.write(((' %.3f ' % histo_data.GetBinContent(ibinsX+1, ibinsY+1))).ljust(columndef))     
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
#   alpha rateParam A bkg (@0*@1/@2) beta,gamma,delta
#   beta  rateParam B bkg 50
#   gamma rateParam C bkg 100
#   delta rateParam D bkg 500
#


#
#
#       ^      ^      ^      ^      ^
#       | \    | \    | \    | \    |
#       |  \   |  \   |  \   |  \   |
#       |   \  |   \  |   \  |   \  |
#       |    \ |    \ |    \ |    \ |
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

    #
    # Only if at least 4 bins!
    #
    
    if nbinsY*nbinsX>=4 :

      card.write('\n')
  
      for ibinsY in range(nbinsY) :
        for ibinsX in range(nbinsX) :
          if (ibinsY != (nbinsY-1) and ibinsX != (nbinsX-1) ) :
            for bkg_name in bkg_names:
              card.write('c_%.0f_%.0f rateParam   %s      %s   (@0*@1/@2) c_%.0f_%.0f,c_%.0f_%.0f,c_%.0f_%.0f \n' % (ibinsX, ibinsY,
                                                                                                                      ("tag_"+str(ibinsX*nbinsY + ibinsY)),
                                                                                                                      bkg_name,
                                                                                                                      ibinsX+1, ibinsY, 
                                                                                                                      ibinsX  , ibinsY+1,
                                                                                                                      ibinsX+1, ibinsY+1 
                                                                                                                      ) )
  
  
      for ibinsY in range(nbinsY) :
        for ibinsX in range(nbinsX) :
          if (ibinsY == (nbinsY-1) or ibinsX == (nbinsX-1) ) :
            for bkg_name in bkg_names:
              card.write('c_%.0f_%.0f rateParam   %s      %s   %.2f \n' % (ibinsX, ibinsY, 
                                                                            ("tag_"+str(ibinsX*nbinsY + ibinsY)),
                                                                            bkg_name,
                                                                            1.0
                                                                            ) )
                                                                            #histo_data.GetBinContent(ibinsX+1, ibinsY+1)) )
                                                                            #
                                                                            # Either you put 1 here or in the "rate" line. Otherwise the default value will not be reasonable
                                                                            #
  
  
      card.write('\n\n\n')
  
      card.write('-'*100+'\n')
  
      #
      # Write standard nuisances
      #
      for nuisanceName, nuisance in nuisances.items():
        if "Signal" in nuisance['samples'] :   
          card.write((nuisance['name'] + "  " + nuisance['type']).ljust(firstcolumndef))
          for ibinsX in range(nbinsX) :
             for ibinsY in range(nbinsY) :
               for isig in range(num_sig):
                 card.write((' %s ' % nuisance['samples']['Signal'] ).ljust(columndef))
               for ibkg in range(num_bkg):
                 card.write((' - ' ).ljust(columndef))     
          card.write('\n')
               
      card.write('\n')
      for nuisanceName, nuisance in nuisances.items():
        if "Signal" not in nuisance['samples'] :   
          card.write((nuisance['name'] + "  " + nuisance['type']).ljust(firstcolumndef))
          for ibinsX in range(nbinsX) :
             for ibinsY in range(nbinsY) :
               for isig in range(num_sig):
                 card.write((' - ' ).ljust(columndef))
               for ibkg in range(num_bkg):      
                 if "bkg_"+str(ibkg)  in nuisance['samples'] :
                   temp_tag = ("tag_"+str(ibinsX*nbinsY + ibinsY))
                   if temp_tag in nuisance['samples']["bkg_"+str(ibkg)] :
                     card.write((' %s ' % nuisance['samples']["bkg_"+str(ibkg)][temp_tag] ).ljust(columndef))
                   else:
                     card.write((' - ' ).ljust(columndef))     
                 else :
                   card.write((' - ' ).ljust(columndef))     
                 
          card.write('\n')
         
      card.write('-'*100+'\n')
  
      #
      # now write nuisances built from non-closure of the ABCD method: it uses MC!
      #
  
      for ibinsY in range(nbinsY) :
        for ibinsX in range(nbinsX) :
          if (ibinsY != (nbinsY-1) and ibinsX != (nbinsX-1) ) :
            for bkg_name in bkg_names:
              
              # A/B = C/D --> A = B*C/D
              #                                    +1            +1 ---> naming convention and ROOT
              B = histo_bkg.GetBinContent(ibinsX+1 +1 , ibinsY   +1)
              C = histo_bkg.GetBinContent(ibinsX   +1 , ibinsY+1 +1)
              D = histo_bkg.GetBinContent(ibinsX+1 +1 , ibinsY+1 +1)
              
              #
              # D has to be >0 !!! ... actually all of them MUST be
              #
              B_times_C_divided_D = B*C/D
              
              #                                  +1         +1 ---> naming convention and ROOT            
              A = histo_bkg.GetBinContent(ibinsX +1, ibinsY +1)
  
              print (" A, B, C, D = ", A, ", ", B, ", ", C, ", ", D)
  
              #if A == 0: 
                #A = 1
                
              #
              # including "A" must be >0 !
              #
              non_closure = (A-B_times_C_divided_D) / A
  
              #
              # this threshold should be put proportional to the statistical uncertainty ... missing ...
              #
              if abs(non_closure) > 0.03 :
                nuisance_name = "c_" + str(ibinsX) + "_" + str(ibinsY) + "_non_closure"
                print ( " non_closure = ", non_closure )
                # Only absolute value is meaningful
                non_closure = abs(non_closure)
                #
                card.write((nuisance_name + "  " + "lnN").ljust(firstcolumndef))
    
                for ibinsX_to_write in range(nbinsX) :
                  for ibinsY_to_write in range(nbinsY) :
    
                    for isig in range(num_sig):
                      card.write((' - ' ).ljust(columndef))
                    for ibkg in range(num_bkg):  
                      if ibinsX_to_write == ibinsX and ibinsY_to_write == ibinsY :
                        card.write((' %s ' % str(round(1+non_closure, 2)) ).ljust(columndef))
                      else:
                        card.write((' - ' ).ljust(columndef))     
              
              card.write('\n')

    card.write('\n\n\n')


    card.close()



    print ("\n\n")
    