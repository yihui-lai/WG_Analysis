
import ROOT
from ROOT import gROOT, gSystem, RooIntegralMorph
from ROOT import RooRealVar, RooDataHist,RooAbsReal
from ROOT import RooFit as rf
from uncertainties import ufloat
import uuid
import re
import random
import sys
from collections import namedtuple, OrderedDict
from functools import wraps
from DrawConfig import DrawConfig
gSystem.Load("My_double_CB/RooDoubleCB_cc.so")
from ROOT import gPad, RooFit, kRed, kBlue, kViolet, kRainBow
import analysis_utils
execfile("MakeBase.py")
inputDir = "/data/users/yihuilai/WG_Analysis/Plotting/WG_Analysis/Plotting/data/sigfit/2018/"
outputDir = "./"
_XSFILE   = 'cross_sections/photon16_1fb.py'

_LUMI16   = 36000
_LUMI17   = 41000
_LUMI18   = 59740

global lumi
def lumi(ibin):
    year = ibin['year']
    if year == 2016: return _LUMI16
    if year == 2017: return _LUMI17
    if year == 2018: return _LUMI18
    raise RuntimeError


def plt_signal_ws( ):

    #signal_masses    = [350, 400, 450, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]
    signal_widths    = ['5', '0p01']
    signal_masses    = [300, 350, 400, 450, 600, 700, 800, 900, 1200, 1400, 1600, 1800, 2000]
    weightMap,_ = analysis_utils.read_xsfile( _XSFILE, 1, print_values=True )
    print(weightMap)
    N_tot = {
              "1400_0p01_2016" : 49405,
              "700_0p01_2016" : 49030,
              "200_0p01_2016" : 48997,
              "1000_0p01_2017": 100000,
              "1200_0p01_2017": 44000,
              "1600_0p01_2017": 48000,
              "1600_5_2017": 48000,
              "2000_0p01_2017": 48000,
              "2000_5_2017": 48000,
              "2400_5_2017": 42000,
              "2800_0p01_2017": 48000,
              "2800_5_2017": 48000,
              "3000_5_2017": 46000,
              "4000_0p01_2017": 48000,
              "300_0p01_2018" : 41000,
              "300_0p01_2018" : 46000,
              "350_5_2018" : 46000,
              "700_0p01_2018" : 46000,
              "800_0p01_2018" : 46000,
              "800_5_2018" : 44000,
              "900_5_2018" : 47000,
              "1600_0p01_2018" : 48000,
              "1800_5_2018" : 48000,
              "2000_5_2018" : 46000,
              "2200_0p01_2018" : 48000,
              "2400_0p01_2018" : 48000,
              "3000_0p01_2018" : 48000,
              "3000_5_2018" : 36000,
    }

    #sampManMuG = SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, lumi=-1)
    sampManElG = SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, lumi=-1)
    sampManMuG.ReadSamples( _SAMPCONF )
    sampManElG.ReadSamples( _SAMPCONF )
    #totevt = sampManMuG.weightHist[2] - sampManMuG.weightHist[1]
    #print(totevt)
    #exit()
    #for mass in signal_masses :
    #    scale = weightMap['ResonanceMass%d'%mass]['scale']
    #    xsec = weightMap['ResonanceMass%d'%mass]['cross_section']\
    #           *weightMap['ResonanceMass%d'%mass]['gen_eff']\
    #           *weightMap['ResonanceMass%d'%mass]['k_factor']
    # 
    #    print("scale:",scale, " xsec:",xsec, "cross_section", weightMap['ResonanceMass%d'%mass]['cross_section'], "k_factor", weightMap['ResonanceMass%d'%mass]['k_factor'])
    
    #signal_masses    = [300, 400, 600, 800,1000, 1200,1400, 1600,1800, 2000]
    #signal_masses    = [2000]
    signal_widths    = ['5','0p01']
    year = '2017'
    Years= ['2016','2017','2018']
    ch = 'el'
    sighists={}
    sigModel={}
    ct=0
    leg1 = ROOT.TLegend(0.55,0.73,0.8,0.87);
    leg1.SetFillColor(ROOT.kWhite);
    leg1.SetLineColor(ROOT.kWhite);
    leg2 = ROOT.TLegend(0.65,0.73,0.86,0.87);
    leg2.SetFillColor(ROOT.kWhite);
    leg2.SetLineColor(ROOT.kWhite);
    inputDir = "data/sigfit/%s/" % (year)
    from array import array
    xx={}
    yy={}
    ntot=50000
    #calculate eff*acceptance
    for wid in signal_widths:
        for iyear in Years:
            grname = 'yr%s_W%s' %(iyear,wid)
            xx[grname], yy[grname] = array( 'd' ),  array( 'd' )
            for mass in signal_masses:
                if("%s_%s_%s"%(str(mass),wid,iyear) in N_tot):
                    ntot= N_tot["%s_%s_%s"%(str(mass),wid,iyear)]
                    print("%s_%s_%s"%(str(mass),wid,iyear), N_tot["%s_%s_%s"%(str(mass),wid,iyear)])
                else:
                    ntot=50000
                    print("%s_%s_%s"%(str(mass),wid,iyear), 50000)
                wsname = 'wssignal_M%s_W%s_%s' %(str(mass),wid,ch)
                pdfname = 'cb_MG_M%s_W%s_%s%s' %(str(mass),wid,ch,iyear)
                dataname = 'MG_M%s_W%s_%s%sdatahist' %(str(mass),wid,ch,iyear)
                inputDir = "data/sigfit/%s/" % (iyear)
                ifile = ROOT.TFile.Open( inputDir+wsname+'.root', 'READ' )
                print("try to find ",pdfname, " and ", dataname , " in ", inputDir+wsname+'.root')
                if not ifile:
                    print "skipping "
                    exit()
                ws_in = ifile.Get( wsname )
                sighists[dataname] = ws_in.data(dataname)
                #print('wssignal_M%s_W%s_el' %(str(mass),wid), "sighists[dataname].sumEntries()",sighists[dataname].sumEntries())
                print("pdfname+'_norm':", pdfname+'_norm')
                print( "norm", ws_in.var(pdfname+'_norm').getVal())
                (xx[grname]).append(int(mass))
                (yy[grname]).append( ws_in.var(pdfname+'_norm').getVal()/ntot )
                #(yy[grname]).append( ws_in.var(pdfname+'_norm').getVal() )
                print("apppend ", int(mass), ws_in.var(pdfname+'_norm').getVal())
    ceff=ROOT.TCanvas()
    gr= {}
    func={}
    leg1 = ROOT.TLegend(0.55,0.73,0.8,0.87);
    leg1.SetFillColor(ROOT.kWhite);
    leg1.SetLineColor(ROOT.kWhite);
    ct=-1
    grsum=ROOT.TMultiGraph()
    if(True):
        for wid in signal_widths:
            for iyear in Years:
                ct+=1
                grname = 'yr%s_W%s' %(iyear,wid)
                print(xx[grname] , yy[grname])
                gr[grname] = ROOT.TGraph( len(xx[grname]), xx[grname], yy[grname] )
                func[grname] = ROOT.TF1(grname, '[0]-[1]*TMath::Exp(-x/[2])', 0, 3000)
                func[grname].SetParameters(6841.47,7739.86,617.44)
                #fit = gr[grname].Fit(grname, '')
                (gr[grname]).SetLineColor( kRainBow + ct*7 )
                (gr[grname]).SetLineWidth( 3 )
                (gr[grname]).SetMarkerColor( kRainBow + ct*7 )
                (gr[grname]).SetMarkerStyle( 21 )
                (gr[grname]).GetXaxis().SetTitle( 'X title' )
                (gr[grname]).GetYaxis().SetTitle( 'Y title' )
                gr[grname].Draw( 'ACP' )
                grsum.Add(gr[grname])
                entry = leg1.AddEntry(gr[grname],grname,"L")
                entry.SetFillStyle(1001)
                entry.SetLineStyle(1)
                entry.SetLineWidth(1)
                entry.SetTextFont(42)
                entry.SetTextSize(0.04)
                entry.SetLineColor(kRainBow+ct*7)
    grsum.Draw("ACP")
    grsum.GetXaxis().SetTitle( 'm_{T} (GeV)' )
    grsum.GetYaxis().SetTitle( 'selection eff.' )
    leg1.Draw()
    input("")

plt_signal_ws()
exit()
















