#!/usr/bin/env python
import matplotlib.pyplot as plt
import sys, json
from collections import OrderedDict, defaultdict


def addparser(parser):
    parser.add_argument('--massplots',  action='store_true', help='Make nuisance parameters vs mass plots' )
    parser.add_argument('--ch',         default="el",        help='Choose muon or electron channel [mu/el]' )
execfile("MakeBase.py")

### This script makes N-1/ final selection distribution plots
###

year = options.year
lconf = {"labelStyle":str(year),"extra_label":"%i Electron Channel" %year, "extra_label_loc":(.17,.82)}
lgconf = {'legendLoc':"Double","legendTranslateX":0.33, "legendCompress":.8, "fillalpha":.5, "legendWiden":.95}
hlist = []


sampManElG.ReadSamples( _SAMPCONF )
samples = sampManElG
if(options.ch=='el'):
    selection = "el_n==1 && ph_n==1"
else:
    sampManMuG.ReadSamples( _SAMPCONF )
    samples = sampManMuG
    selection = "mu_n==1 && ph_n==1"

sf = samples.SetFilter(selection)
hlist=[]


varlist = [ ("met_pt","MET","GeV",(100,0,500)),
            #("ph_pt[0]", "leading #gamma pT", "GeV", (80,0,400)),
            #("mt_lep_met_ph","m_{T}(#mu,#gamma,p_{T}^{miss})","GeV",(1000,0,2000)),
            ]

if(options.ch=='el'):
    sellist, weight =  defs.makeselstringlist( ch = "el", phpt = 40, leppt = 35, met = 40 )
else:
    sellist, weight =  defs.makeselstringlist( ch = "mu", phpt = 40, leppt = 35, met = 40 )
#sellist +=["mt_res>500"]
selfull = " && ".join(sellist) ## full signal selection
print("sellist",sellist)
print("weight",weight)
print("selfull",selfull)

print("varlist",varlist)

weight = weight.replace("*jet_btagSF","") ## No btag
if options.year == 2018:
    weight = weight.replace("prefweight","1")


for var in varlist:
    varname = str.translate(var[0],None,"[]_")
    print('var',var)
    print('varname',varname)
    sel = " && ".join([s for s in sellist if var[0] not in s ])
    if(options.ch=='el'):
        save_as = ("%s_%ielg_ln_ratio.pdf" %(varname,year), options.outputDir, "base")
    else:
        save_as = ("%s_%imug_ln_ratio.pdf" %(varname,year), options.outputDir, "base")
    print('save_as',save_as)
    #continue
    hconf = { "xlabel":var[1],"xunit":var[2],"drawsignal":False, "logy":True,"ymin":0.01, "ymax":10000}
    if "pt" in var[0]:
        hconf["drawsignal"]=True
    if "phi" in var[0] or "eta" in var[0]:
        hconf["ymax_scale"]=2.
    hf = sf.SetHisto1DFast(var[0], sel, var[3], weight, hconf, lgconf , lconf, save_as, data_exp = True)
    hlist.append(hf)
    #save_as = ("%s_%ielel_elselln.pdf" %(varname,year), options.outputDir, "base")
    #sel = (el_eb+elpt40).lstrip("& ")
    #hf = sf.SetHisto1DFast(var[0], sel, var[3], weight, hconf, lgconf , lconf, save_as)
    #hlist.append(hf)

#exit()

for hf in hlist:
    hf.DrawSave()
    #sc = samples.get_stack_count(includeData=True)
    #nmc = sc["TOTAL"][0]
    #ndt = sc["Data"][0]
    #print "mccount, datacount, mc/dt: ", nmc, ndt, nmc/ ndt

exit()

sel,w = defs.makeselstring()

samplelist =  ["WGamma", "AllTop", "Zgamma","TopW"]
hconf = {"weight":w,"doratio":1,"logy":1,"normalize":True,"bywidth":True,"rlabel":"ratio to W#gamma","xlabel":"m_{T}^{res}(e, #gamma, #slash{E}_{T})","ymin":1e-6,"reverseratio":1}
lconf = {"labelStyle":str(year),"extra_label":["%i Electron Channel" %year,"p_{T}^{e}>35GeV, MET>40GeV","Tight barrel #gamma p_{T}^{#gamma}>80GeV"], "extra_label_loc":(.27,.82)}
mlist=[]
samples.CompareSelections("mt_res",[sel+"&&mt_res>200"]*len(samplelist),samplelist,mlist, hconf, lconf)
samples.SaveStack("mtres_mug%i_sigsel_bkgdcomp.pdf" %year,options.outputDir,"base")




