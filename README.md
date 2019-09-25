# DatacardCreatorABCD

Generic datacard creator for ABCD


Create datacard:

    mkDatacards.py

    
How to run:

    python mkDatacards.py  --inputHistoFile abcd_backgrounds.root   \
                           --dataHistoName  ABCD_270_3.6   \
                           --sigHistoName  ABCD_270_3.6
                           
    
    
    python mkDatacards.py  --inputHistoFile abcd_plots.root   \
                           --dataHistoName  ABCD_240_4.3_Backgrounds   \
                           --sigHistoNameTemplate  ABCD_240_4.3_Wino
     
     
    python mkDatacards.py  --inputHistoFile abcd_plots_2.root   \
                           --dataHistoName  ABCD_220_3.0_Backgrounds   \
                           --sigHistoNameTemplate  ABCD_220_3.0_Wino

                           
    python mkDatacards.py  --inputHistoFile abcd_plots_2.root   \
                           --dataHistoName  ABCD_220_3.0_Backgrounds   \
                           --sigHistoNameTemplate  ABCD_220_3.0_Wino   \
                           --nuisancesFile   test/nuisances.py
                           

    python mkDatacards.py  --inputHistoFile abcd_plots_3x3_4layers.root   \
                           --dataHistoName  W+jets_background   \
                           --sigHistoNameTemplate  Wino   \
                           --nuisancesFile   test/nuisances.py

                           
                           
See instructions:

    https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/wiki/settinguptheanalysis
    https://indico.cern.ch/event/577649/contributions/2339440/attachments/1380196/2097805/beyond_simple_datacards.pdf

    
Where:

    /home/amassiro/Cern/Code/CMG/DisappearingTracks/DatacardCreatorABCD

    
Test the datacard:

    See http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/
    
    Where: /afs/cern.ch/work/a/amassiro/Latinos/Framework/Combine/CMSSW_10_2_13/src/
    
    If only one signal sample:
    combine -d datacard_mytest.txt   -M AsymptoticLimits

    Otherwise:
    text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel  --PO verbose \
         --PO 'map=.*/*Wino*:to_be_frozen[1,0,10]' \
         --PO 'map=.*/*Wino_m800_ct20:r[1,0,10]' \
         datacard_mytest.txt -o datacard_mytest.txt.root

    combine -d datacard_mytest.txt.root   -M AsymptoticLimits \
      --setParameters to_be_frozen=0  \
      --freezeParameters to_be_frozen \
      --redefineSignalPOIs r
      
      

      
    text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel  --PO verbose \
         --PO 'map=.*/*Wino*:to_be_frozen[1,0,10]' \
         --PO 'map=.*/*Wino_m800_ct20:r[1,0,10]' \
         datacard_mytest.txt -o datacard_mytest.m800_ct20.root

    combine -d datacard_mytest.m800_ct20.root   -M AsymptoticLimits \
      --setParameters to_be_frozen=0  \
      --freezeParameters to_be_frozen \
      --redefineSignalPOIs r
      
      
      