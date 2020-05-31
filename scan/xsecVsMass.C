
vector<tuple<int, double>> xsections = {
  { 300, 387 },
  { 400, 121 },
  { 500, 46  },
  { 600, 20  },
  { 700, 9.5 },
  { 800, 4.8 },
  { 900, 2.5 },
};
  
void xsecVsMass()
{
  TGraph *graph = new TGraph();
  int iPoint=0;
  
  for(auto &[mass, xsec] : xsections) graph->SetPoint(iPoint++, mass, xsec);
  
  graph->SetMarkerStyle(20);
  graph->GetXaxis()->SetTitle("m (GeV)");
  graph->GetYaxis()->SetTitle("#sigma (fb)");
  
  graph->Draw("AP");
  graph->GetYaxis()->SetRangeUser(0, 500);
  
  TF1 *fun = new TF1("fun", "[0]*exp([1]*x)", 0, 1000);
  fun->SetParameter(0, 14000);
  fun->SetParameter(1, -0.012);
  
  graph->Fit(fun);
}
