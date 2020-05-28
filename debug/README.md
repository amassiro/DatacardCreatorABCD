Debug
====

    cd /afs/cern.ch/user/a/amassiro/Framework/Combine/DisapTracks/CMSSW_10_2_13/src

    cmsenv
    
    cp /afs/cern.ch/work/j/jniedzie/public/limitsDebugging/datacard_3x3_4-layers_Chargino_300_1.txt .
    
    text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
             --PO verbose --PO 'map=.*/*Chargino*:to_be_frozen[1,0,10]' --PO 'map=.*/*Chargino_300_10$:r[1,0,10]' \
             datacard_3x3_4-layers_Chargino_300_1.txt \
             -o datacard.root


    combine -d datacard.root -M AsymptoticLimits --setParameters to_be_frozen=0 \
            --freezeParameters to_be_frozen --redefineSignalPOIs r -t -1 \
            --setParameterRanges c_1_0=0.001,100:c_0_2=0.001,100:c_1_2=0.001,100:c_1_1=0.001,100


Error.

Now the following:

            
    combine -d datacard.root -M AsymptoticLimits --setParameters to_be_frozen=0 \
            --freezeParameters to_be_frozen --redefineSignalPOIs r -t -1 \
            --setParameterRanges c_2_0=0.001,100:c_2_1=0.001,100:c_0_2=0.001,100:c_1_2=0.001,100:c_2_2=0.001,100
        
        
     