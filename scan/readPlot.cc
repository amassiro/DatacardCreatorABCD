


  
  
void setupHisto(TH1F* histo, int icolor) {
  
  Color_t* color = new Color_t [200];
  color[0] = kAzure; //kRed ;
  color[1] = kAzure + 10 ;
  color[2] = kBlack ;
  color[3] = kGreen ;
  color[4] = kGreen + 4 ;
  color[5] = kBlue ;
  color[6] = kCyan ;
  color[7] = kPink + 1 ;
  color[8] = kMagenta + 2 ;
  color[9] = kYellow + 4 ;
  color[10]= kRed ;
  for (int i=0; i<30; i++) {
    color[i+11] = kBlue + i;
  }
  
  
  histo->SetLineColor(color[icolor]);
  histo->SetMarkerColor(color[icolor]);
  histo->SetMarkerSize(1);
  histo->SetMarkerStyle(20+icolor);
}



void readPlot(std::string datacard_name = "datacard_3x3_4-layers_Chargino_300_1.txt.reduced.txt") {
  
  
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
      
      if (what == "process") {
        while (line) {
          line >> value_string;
          samples.push_back(value_string);
        }
      }
      
      if (what == "bin") {
        while (line) {
          line >> value_string;
          tags.push_back(value_string);
        }
      }
      
      if (what == "rate") {
        while (line) {
          line >> value_float;
          values.push_back(value_float);
        }
      }
      
    } 
  }
  
  
  // get unique list of samples
  std::vector<std::string> samples_unique = samples;
  std::vector<std::string>::iterator it;
  it = std::unique (samples_unique.begin(), samples_unique.end());
  samples_unique.resize( std::distance(samples_unique.begin(),it) );
  
  std::vector<std::string> tags_unique = tags;
  it = std::unique (tags_unique.begin(), tags_unique.end());
  tags_unique.resize( std::distance(tags_unique.begin(),it) );
  
  std::cout << " samples_unique.size() = " << samples_unique.size() << std::endl;
  std::cout << " tags_unique.size()    = " << tags_unique.size() << std::endl;
  
  
  TH1F* histos[samples_unique.size()];
  TH1F* histos_normalized[samples_unique.size()];
 
  for (int iSample = 0; iSample<samples_unique.size(); iSample++) {
    TString name = Form ("hist_%d", iSample);
    histos[iSample] = new TH1F (name.Data(), name.Data(), tags_unique.size(), 0, tags_unique.size());
    setupHisto(histos[iSample], iSample);

    TString name_normalized = Form ("hist_normalized_%d", iSample);
    histos_normalized[iSample] = new TH1F (name_normalized.Data(), name_normalized.Data(), tags_unique.size(), 0, tags_unique.size());
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
            histos[iSample]->SetBinContent (iTag+1, values.at(i));
            histos_normalized[iSample]->SetBinContent (iTag+1, values.at(i));
          }
        }
      }
    }
  }

  for (int iSample = 0; iSample<samples_unique.size(); iSample++) {
    float integral = histos_normalized[iSample] -> Integral();
    histos_normalized[iSample]->Scale(1./integral);
  }
  
  TCanvas* cc = new TCanvas("cc", datacard_name.c_str(), 800, 600);
  for (int iSample = 0; iSample<samples_unique.size(); iSample++) {
    if (iSample==0) histos[iSample]->Draw();
    else            histos[iSample]->Draw("same");
  }
  
  TCanvas* cc_normalized = new TCanvas("cc_normalized", "normalized", 800, 600);
  for (int iSample = 0; iSample<samples_unique.size(); iSample++) {
    if (iSample==0) histos_normalized[iSample]->Draw();
    else            histos_normalized[iSample]->Draw("same");
  }
  
  
  
  
}
