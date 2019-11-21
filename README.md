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

    python mkDatacards.py  --inputHistoFile abcd_plots_3x3_3-layers_LH_noTag_650_10.root   \
                           --dataHistoName  background   \
                           --sigHistoNameTemplate  Wino   \
                           --bkgHistoName   background  \
                           --nuisancesFile   test/nuisances.py

    python mkDatacards.py  --inputHistoFile abcd_plots_3x3_3-layers_LH_noTag_650_10.root   \
                           --dataHistoName  background   \
                           --sigHistoNameTemplate  Wino_m800_ct20   \
                           --bkgHistoName   background  \
                           --nuisancesFile   test/nuisances.py
                           
    python mkDatacards.py  --inputHistoFile abcd_plots_3x3_4layers.root   \
                           --dataHistoName  data_histo   \
                           --sigHistoNameTemplate  Wino   \
                           --bkgHistoName   W+jets_background  \
                           --nuisancesFile   test/nuisances.py
      
    
    
      
                           
Python3

    python3 mkDatacards.py --inputHistoFile abcd_plots_3x3_4layers.root   \
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
      
      
Closure test:

    scp amassiro@lxplus.cern.ch:/afs/cern.ch/work/j/jniedzie/public/abcdPlots/abcd_plots_Wmunu.root .

    python mkDatacards.py  --inputHistoFile abcd_plots_Wmunu.root   \
                           --dataHistoName  data   \
                           --sigHistoNameTemplate  XXX   \
                           --bkgHistoName   background  \
                           --nuisancesFile   test/nuisances.py

    In text2workspace remember to set "text2workspace.py --X-allow-no-signal"
    
    Where: /afs/cern.ch/work/a/amassiro/Latinos/Framework/Combine/CMSSW_10_2_13/src/

    
    text2workspace.py  --PO verbose \
        --X-allow-no-signal  \
         datacard_mytest.txt -o datacard_mytest.root

    
    combine -M GoodnessOfFit datacard_mytest.root --algo=saturated

    combine -M GoodnessOfFit datacard_mytest.root --algo=saturated \
      --redefineSignalPOIs c_1_0,c_1_1,c_0_2,c_1_2 
      
    
    combine -M GoodnessOfFit datacard_mytest.root --algo=saturated \
      --setParameters r=0 \
      --freezeParameters r \
      -t 500 --toysFrequentist
       
       
       
    
    text2workspace.py --X-allow-no-signal  --PO verbose \
         datacard_example.txt -o datacard_example.root
     
    combine -M GoodnessOfFit datacard_example.root --algo=saturated
       
    combine -M GoodnessOfFit datacard_example.root --algo=saturated \
      -t 500 --toysFrequentist
      
    combine -M GoodnessOfFit datacard_example.root --algo=saturated \
      -t 500 --toysNoSystematics
    
    
    
    
    
    
    text2workspace.py  --PO verbose         --X-allow-no-signal           datacard_example_modified.txt   -o datacard_example_modified.root
    
    combine -M GoodnessOfFit datacard_example_modified.root  --algo=saturated
    
    combine -M GoodnessOfFit datacard_example_modified.root  --algo=saturated   -t 10   --toysNoSystematics
    
    -> it works
    
    
    
    
    
    
     combine -d datacard_mytest.root   -M MultiDimFit \
      --setParameters to_be_frozen=0 \
      --freezeParameters to_be_frozen \
       --redefineSignalPOIs c_1_0,c_1_1,c_0_2,c_1_2 \
     --forceRecreateNLL  \
     --algo singles 


    combine -M GoodnessOfFit -d combined_card.root --algo=saturated -n _result_bonly_CRonly_toy --setParametersForFit mask_ch1=1 --setParametersForEval mask_ch1=0 --freezeParameters r --setParameters r=0,mask_ch1=1
       
    combine -M GoodnessOfFit datacard.txt --algo=saturated -t 10 -s 42

    
    https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit#Goodness_of_fit_tests
    
    
      
      
