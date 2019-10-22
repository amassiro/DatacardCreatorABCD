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




