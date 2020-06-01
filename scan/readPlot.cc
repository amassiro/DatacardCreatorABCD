#include "tdrstyle.C"

template <typename T> void remove_duplicates(std::vector<T>& vec) {
  std::sort(vec.begin(), vec.end());
  vec.erase(std::unique(vec.begin(), vec.end()), vec.end());
}  
  
void setupHisto(TH1F* histo, int icolor) {
  
  Color_t* color = new Color_t [200];
  color[0] = kRed ;
  color[1] = kAzure + 7 ;
  color[2] = kGreen + 2 ;
  color[3] = kRed +1 ;
  color[4] = kAzure + 8 ;
  color[5] = kGreen + 3;
  color[6] = kRed +2 ;
  color[7] = kAzure + 9 ;
  color[8] = kGreen + 4 ;
  color[9] = kYellow + 4 ;
  for (int i=0; i<30; i++) {
    color[i+10] = kBlue + i;
  }
  
//   color[0] = kRed ;
//   color[1] = kAzure + 10 ;
//   color[2] = kYellow + 2 ;
//   color[3] = kGreen ;
//   color[4] = kGreen + 4 ;
//   color[5] = kBlue ;
//   color[6] = kCyan ;
//   color[7] = kPink + 1 ;
//   color[8] = kBlack ;
//   color[9] = kYellow + 4 ;
//   for (int i=0; i<30; i++) {
//     color[i+10] = kBlue + i;
//   }
  
  histo->SetLineColor(color[icolor]);
  histo->SetMarkerColor(color[icolor]);
  histo->SetMarkerSize(1);
  histo->SetMarkerStyle(20+icolor);
}



void readPlot(std::string datacard_name = "datacard_3x3_4-layers_Chargino_300_1.txt.reduced.txt") {
  
  gStyle->SetOptStat(0);
  setTDRStyle();
  
  
  std::cerr << "File " << datacard_name << std::endl;
  
  std::ifstream file (datacard_name); 
  
  
  std::vector<float>       values;
  std::vector<std::string> tags;
  std::vector<std::string> samples;
  
  
  
  std::string buffer;
  std::string what;
  
  std::string value_string;
  float value_float;
  
  if(!file.is_open()) {
    std::cerr << "** ERROR: Can't open '" << datacard_name << "' for input" << std::endl;
    return false;
  }
  
  while(!file.eof()) {
    getline(file,buffer);
    if (buffer != ""){ ///---> save from empty line at the end!
      std::stringstream line( buffer );      
      
      line >> what;
      
      std::cout << " what = " << what << std::endl;
      
      if (what == "process" && samples.size()==0) {
        while (line) {
          line >> value_string;
          samples.push_back(value_string);
        }
      }
      
      if (what == "bin" && tags.size()==0) {
        while (line) {
          line >> value_string;
          tags.push_back(value_string);
        }
      }
      
      if (what == "rate" && values.size()==0) {
        while (line) {
          line >> value_float;
          values.push_back(value_float);
        }
      }
      
    } 
  }
  
  
  // get unique list of samples
  std::vector<std::string> samples_unique = samples;
//   std::vector<std::string>::iterator it;
//   it = std::unique (samples_unique.begin(), samples_unique.end());
//   samples_unique.resize( std::distance(samples_unique.begin(),it) );
  remove_duplicates<std::string>(samples_unique);
  
  std::vector<std::string> tags_unique = tags;
//   it = std::unique (tags_unique.begin(), tags_unique.end());
//   tags_unique.resize( std::distance(tags_unique.begin(),it) );
  remove_duplicates<std::string>(tags_unique);
  
  std::cout << " samples.size()        = " << samples.size() << std::endl;
  std::cout << " samples_unique.size() = " << samples_unique.size() << std::endl;
  std::cout << " tags_unique.size()    = " << tags_unique.size() << std::endl;
  
  
  TH1F* histos[samples_unique.size()];
  TH1F* histos_normalized[samples_unique.size()];
 
  for (int iSample = 0; iSample<samples_unique.size(); iSample++) {
    TString name = Form ("hist_%d", iSample);
    histos[iSample] = new TH1F (name.Data(), name.Data(), tags_unique.size()*samples_unique.size(), 0, tags_unique.size()*samples_unique.size());
    setupHisto(histos[iSample], iSample);

    TString name_normalized = Form ("hist_normalized_%d", iSample);
    histos_normalized[iSample] = new TH1F (name_normalized.Data(), name_normalized.Data(), tags_unique.size()*samples_unique.size(), 0, tags_unique.size()*samples_unique.size());
    setupHisto(histos_normalized[iSample], iSample);
    
  }
  
  
  // fill the histograms
  for (int i = 0; i<samples.size(); i++) {
    std::string sample = samples.at(i);
    for (int iSample = 0; iSample<samples_unique.size(); iSample++) {
      if (sample == samples_unique.at(iSample) ) {
        std::string tag = tags.at(i);
        
        for (int iTag = 0; iTag<tags_unique.size(); iTag++) {
          if (tag == tags_unique.at(iTag) ) {
            histos[iSample]->SetBinContent (iTag*samples_unique.size()+iSample+1, values.at(i));
            histos[iSample]->SetBinError   (iTag*samples_unique.size()+iSample+1, 0);
            histos_normalized[iSample]->SetBinContent (iTag*samples_unique.size()+iSample+1, values.at(i));
            histos_normalized[iSample]->SetBinError   (iTag*samples_unique.size()+iSample+1, 0);
          }
        }
      }
    }
  }

  for (int iSample = 0; iSample<samples_unique.size(); iSample++) {
    float integral = histos_normalized[iSample] -> Integral();
    histos_normalized[iSample]->Scale(1./integral);
  }
  
  TLegend* legend_useful = new TLegend(0.81,0.25,0.99,0.90);
  for (int iSample = 0; iSample<samples_unique.size(); iSample++) {
    legend_useful->AddEntry(histos[iSample], TString::Format("%s", samples_unique.at(iSample).c_str()) ,"fp");
  }
  
  
  
  
  
  TCanvas* cc = new TCanvas("cc", datacard_name.c_str(), 1200, 600);
  cc->SetRightMargin(0.2);
  for (int iSample = 0; iSample<samples_unique.size(); iSample++) {
    if (iSample==0) histos[iSample]->Draw();
    else            histos[iSample]->Draw("same");
  }
  legend_useful->Draw();
  
  for (int iTag = 0; iTag<tags_unique.size(); iTag++) {
    TLine ll((iTag+1)*samples_unique.size(), 0, (iTag+1)*samples_unique.size(), 100);
    ll.SetLineColor(kBlack);
    ll.SetLineWidth(3);
    ll.DrawClone();
  }  
  
  
  
  
  
  
  
  TCanvas* cc_normalized = new TCanvas("cc_normalized", "normalized", 1200, 600);
  cc_normalized->SetRightMargin(0.2);
  for (int iSample = 0; iSample<samples_unique.size(); iSample++) {
    if (iSample==0) histos_normalized[iSample]->Draw("P");
    else            histos_normalized[iSample]->Draw("P same");
  }
  histos_normalized[0]->GetYaxis()->SetRangeUser(0.0,0.7);
  legend_useful->Draw();
  
  for (int iTag = 0; iTag<tags_unique.size(); iTag++) {
    TLine ll((iTag+1)*samples_unique.size(), 0, (iTag+1)*samples_unique.size(), 0.7);
    ll.SetLineColor(kBlack);
    ll.SetLineWidth(3);
    ll.DrawClone();
  }  
  
  
  
  
}
