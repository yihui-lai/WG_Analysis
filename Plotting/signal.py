
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

    signal_masses    = [300, 350, 400, 450, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]
    signal_widths    = ['5', '0p01']
    signal_masses    = [300, 350, 400, 450, 600, 700, 800, 900, 1200, 1400, 1600, 1800, 2000]
    weightMap,_ = analysis_utils.read_xsfile( _XSFILE, 1, print_values=True )
    print(weightMap)


    sampManMuG = SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, lumi=-1)
    #sampManElG = SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, lumi=-1)
    sampManMuG.ReadSamples( _SAMPCONF )
    #sampManElG.ReadSamples( _SAMPCONF )
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
    signal_widths    = ['5']
    year = '2017'
    ch = 'el'
    sighists={}
    sigModel={}
    c=ROOT.TCanvas()
    ct=0
    leg1 = ROOT.TLegend(0.55,0.73,0.8,0.87);
    leg1.SetFillColor(ROOT.kWhite);
    leg1.SetLineColor(ROOT.kWhite);
    leg2 = ROOT.TLegend(0.65,0.73,0.86,0.87);
    leg2.SetFillColor(ROOT.kWhite);
    leg2.SetLineColor(ROOT.kWhite);
    inputDir = "data/sigfit/%s/" % (year)
    va = RooRealVar("mt_res", "mt_res", 100, 2500)
    for wid in signal_widths:
        for mass in signal_masses:
            wsname = 'wssignal_M%s_W%s_%s' %(str(mass),wid, ch)
            ifile = ROOT.TFile.Open( inputDir+wsname+'.root', 'READ' )
            ws_in = ifile.Get( wsname )
            va.setRange(wsname+'range', ws_in.var("mt_res").getMin(),ws_in.var("mt_res").getMax())
            ifile.Close()
    frame = va.frame()
    from array import array
    x, y = array( 'd' ), array( 'd' )
    for wid in signal_widths:
        for mass in signal_masses:
            wsname = 'wssignal_M%s_W%s_%s' %(str(mass),wid,ch)
            pdfname = 'cb_MG_M%s_W%s_%s%s' %(str(mass),wid,ch,year)
            dataname = 'MG_M%s_W%s_%s%sdatahist' %(str(mass),wid,ch,year)
            ifile = ROOT.TFile.Open( inputDir+wsname+'.root', 'READ' )
            print("try to find ",pdfname, " and ", dataname , " in ", inputDir+wsname+'.root')
            if not ifile:
                print "skipping "
                exit()
            ws_in = ifile.Get( wsname )
            sighists[dataname] = ws_in.data(dataname)
            #print('wssignal_M%s_W%s_el' %(str(mass),wid), "sighists[dataname].sumEntries()",sighists[dataname].sumEntries())
            print("norm:", ws_in.var(pdfname+'_norm').getVal()) 
            x.append(int(mass))
            y.append( ws_in.var(pdfname+'_norm').getVal() )
            
            #continue
            sigModel[pdfname] = ws_in.pdf(pdfname)
            print "number of bins ", sighists[dataname].numEntries()
            print "correct ", (ws_in.var("mt_res").getMax() - ws_in.var("mt_res").getMin())/sighists[dataname].numEntries()
            if(ct==0):
                inorm = (ws_in.var("mt_res").getMax() - ws_in.var("mt_res").getMin())/sighists[dataname].numEntries()
            sighists[dataname].plotOn(frame, RooFit.MarkerColor(ROOT.kRainBow+ct*3),  RooFit.MarkerStyle(2), RooFit.LineColor(kRainBow+ct*3), RooFit.Normalization(1.0/(sighists[dataname].sumEntries()*(ws_in.var("mt_res").getMax() - ws_in.var("mt_res").getMin())/sighists[dataname].numEntries()/inorm),RooAbsReal.NumEvent))
            #weight = RooRealVar("weight","weight",1.0/(sighists[dataname].sumEntries()*(ws_in.var("mt_res").getMax() - ws_in.var("mt_res").getMin())/sighists[dataname].numEntries()/inorm))
            #sighists[dataname].addColumn(weight)
            #sighists[dataname].setAllWeights(1.0/(sighists[dataname].sumEntries()*(ws_in.var("mt_res").getMax() - ws_in.var("mt_res").getMin())/sighists[dataname].numEntries()/inorm))
            sigModel[pdfname].plotOn(frame, RooFit.Name(pdfname), RooFit.LineColor(kRainBow+ct*3), RooFit.LineStyle(2),  RooFit.Range(wsname+'range'),RooFit.Normalization(sighists[dataname].sumEntries()*(ws_in.var("mt_res").getMax() - ws_in.var("mt_res").getMin())/sighists[dataname].numEntries()/inorm,RooAbsReal.NumEvent))
            #sigModel[pdfname].plotOn(frame, RooFit.Name(pdfname), RooFit.LineColor(kRainBow+ct*3), RooFit.LineStyle(2),  RooFit.Range(wsname+'range'))
            ct+=1
            #continue
            if ct<=7:
                entry = leg1.AddEntry(pdfname,"ChargedResonace_%sGeV_width%s" %(str(mass),wid),"L")
            else:
                entry = leg2.AddEntry(pdfname,"ChargedResonace_%sGeV_width%s" %(str(mass),wid),"L")
            entry.SetFillStyle(1001)
            entry.SetLineStyle(1)
            entry.SetLineWidth(1)
            entry.SetTextFont(42)
            entry.SetTextSize(0.04)
            entry.SetLineColor(kRainBow+ct*3)
    frame.Draw()
    leg1.Draw()
    leg2.Draw()
    #c.SaveAs('all_signal_w%s%s%s.pdf'%(wid,ch,year))
    c.SaveAs('all_signal_w%s%s%s.C'%(wid,ch,year))

    gr = ROOT.TGraph( len(x), x, y )
    func = ROOT.TF1('func', '[0]-[1]*TMath::Exp(-x/[2])', 0, 3000)
    func.SetParameters(6841.47,7739.86,617.44)
    fit = gr.Fit('func', '')
    fit = gr.Fit('func', '')
    #gr.Fit("pol2","")
    gr.SetLineColor( 2 )
    gr.SetLineWidth( 4 )
    gr.SetMarkerColor( 4 )
    gr.SetMarkerStyle( 21 )
    gr.SetTitle( 'a simple graph' )
    gr.GetXaxis().SetTitle( 'X title' )
    gr.GetYaxis().SetTitle( 'Y title' )
    #gr.Draw( 'ACP' )
    #input("")
plt_signal_ws()
exit()




