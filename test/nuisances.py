

nuisances['lumi']  = {
               'name'  : 'lumi', 
               'type'  : 'lnN',
               'samples'  : {
                   'Signal' : '1.02',
                   }
               }
               

#nuisances['test']  = {
               #'name'  : 'test', 
               #'type'  : 'lnN',
               #'samples'  : {
                   #'bkg_0' : { 'tag_0' : '1.02',
                               #'tag_1' : '1.02',
                               #'tag_2' : '1.05',
                             #}
                   #}
               #}



#
# To be applied to all signal saamples
#

nuisances['jetpt']  = {
               'name'  : 'jet_pt', 
               'type'  : 'shape',
               'rootFileUp'   : 'abcd_plots_3x3_4layers_jet_pt_up.root',
               'rootFileDown' : 'abcd_plots_3x3_4layers_jet_pt_down.root',
               'samples'  : { }
               }
