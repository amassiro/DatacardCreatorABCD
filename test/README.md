Combine test
----

See: 

     https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/wiki/settinguptheanalysis
     
     
Understainding the model:

    combine datacard_1.txt -M AsymptoticLimits --redefineSignalPOIs r

    text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/*Signal*:to_be_frozen[1,0,10]' --PO 'map=.*/*Signal_1:r[1,0,10]' datacard_2.txt -o datacard.root
    combine datacard.root -M AsymptoticLimits --setParameters to_be_frozen=0 --freezeParameters to_be_frozen --redefineSignalPOIs r

    text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/*Signal*:to_be_frozen[1,0,10]' --PO 'map=.*/*Signal_1:r[1,0,10]' datacard_3.txt -o datacard.root
    
    text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/*Signal*:to_be_frozen[1,0,10]' --PO 'map=.*/*Signal_1:r[1,0,10]' datacard_4.txt -o datacard.root
    
    text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/*Signal*:to_be_frozen[1,0,10]' --PO 'map=.*/*Signal_3:r[1,0,10]' datacard_4.txt -o datacard.root
    
    
    
Observed Limit: r < 2.6904
Expected  2.5%: r < 1.2598
Expected 16.0%: r < 1.7729
Expected 50.0%: r < 2.6875
Expected 84.0%: r < 4.1980
Expected 97.5%: r < 6.3093
    
    
Observed Limit: r < 2.6907
Expected  2.5%: r < 1.2598
Expected 16.0%: r < 1.7729
Expected 50.0%: r < 2.6875
Expected 84.0%: r < 4.1980
Expected 97.5%: r < 6.3093


Specific tests:

    text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/*Wino*:to_be_frozen[1,0,10]' --PO 'map=.*/*Wino_m300_ct3:r[1,0,10]'  /afs/cern.ch/work/j/jniedzie/public/abcdPlots/datacard_3x3_4-layers_tagSim_noPU_1000_10.txt -o datacard.root

    text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/*Wino*:to_be_frozen[1,0,10]' --PO 'map=.*/*Wino_m300_ct3:r[1,0,10]' --PO 'map=.*/*Wino_m300_ct30:to_be_frozen[1,0,10]' /afs/cern.ch/work/j/jniedzie/public/abcdPlots/datacard_3x3_4-layers_tagSim_noPU_1000_10.txt -o datacard.root

    text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/*Wino*:to_be_frozen[1,0,10]' --PO 'map=.*/*Wino_m300_ct3$:r[1,0,10]' /afs/cern.ch/work/j/jniedzie/public/abcdPlots/datacard_3x3_4-layers_tagSim_noPU_1000_10.txt -o datacard.root

    combine datacard.root -M AsymptoticLimits --setParameters to_be_frozen=0 --freezeParameters to_be_frozen --redefineSignalPOIs r --setParameterRanges c_2_0=0.001,100:c_2_1=0.001,100:c_0_2=0.001,100:c_1_2=0.001,100:c_2_2=0.001,100

    
    
    text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/*Wino:to_be_frozen[1,0,10]' --PO 'map=.*/*Wino_m500_ct20$:r[1,0,100]' datacard_mytest.txt   -o datacard_test.root
    
    combine datacard_test.root -M AsymptoticLimits --setParameters to_be_frozen=0 --freezeParameters to_be_frozen --redefineSignalPOIs r --setParameterRanges c_1_0=0.001,100:c_0_2=0.001,100:c_1_2=0.001,100:c_1_1=0.001,100

    combine datacard_test.root -M AsymptoticLimits --setParameters to_be_frozen=0 --freezeParameters to_be_frozen --redefineSignalPOIs r --setParameterRanges c_1_0=0.001,100:c_0_2=0.001,100:c_1_2=0.001,100:c_1_1=0.001,100     -t -1
    
    

    

