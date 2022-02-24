#!/usr/bin/env python

execfile("MakeBase.py")

def main() :
    sampManElG, sampManMuG = None, None
    sampManMuG= SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio, readHists=False , weightHistName = "weighthist")
    sampManMuG.ReadSamples( _SAMPCONF )
    sampManElG= SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio ,readHists=False , weightHistName = "weighthist")
    sampManElG.ReadSamples( _SAMPCONF )

    plotvarsbase = [ 
                 #("m_{T}^{l#nu#gamma}","mt_res", 'GeV',(100,0,2500)),
                 ("m_{T}^{l#nu#gamma}_pT(#gamma)","ph_pt[0]:mt_res", 'GeV',(50,0,2500,50,0,2500)),
                 #("p_{T}(#gamma)","ph_pt[0]"    , 'GeV' ,(20,0,500)),
                 #("#eta(#gamma)","ph_eta[0]"    , '' ,(20,-2,2)),
                 #("#phi(#gamma)","ph_phi[0]"    , '' ,(20,-3.14,3.14)),
                 #("MET"         ,"met_pt"     , 'GeV'  ,(20,0,500)),
                 #("#phi(MET)"         ,"met_phi"    , ''   ,(20,-3.14,3.14)),
                ]
    plotvarsel=[ 
                 ("p_{T}(e)","el_pt[0]"  , 'GeV'   ,(20,0,500)),
                 ("#eta(e)","el_eta[0]"     , '', (20,-3,3)),
                 ("#phi(e)","el_phi[0]"  , ''   ,(20,-3.14,3.14)),
                 #("m_{T}^{l#nu#gamma}","mt_res", 'GeV',[0, 150, 189.86, 213.18, 227.26, 265.98, 306.9, 347.38, 500.06, 516.78, 600.38, 605.22, 618.42, 649.66, 671.22, 687.5, 735.02, 768.46, 812.9, 844.58, 857.78, 881.98, 962.94, 1039.94, 1192.18, 1541.1,2200]),
                 ("m_{T}^{l#nu#gamma}","mt_res", 'GeV',[0, 150, 200, 250, 300, 350, 400, 500, 750, 1000, 2500]),
               ]
    plotvarsmu=[ 
                 ("p_{T}(#mu)","mu_pt[0]"   ,'GeV'  ,(20,0,500)),
                 ("#eta(#mu)","mu_eta[0]"   , ''  ,(20,-3,3)),
                 ("#phi(#mu)","mu_phi[0]"  , ''   ,(20,-3.14,3.14)),
                 #("m_{T}^{l#nu#gamma}","mt_res", 'GeV',[0, 150, 181.06, 196.46, 217.58, 243.54, 281.82, 339.46, 500.06, 559.46, 600.38, 611.38, 625.9, 641.3, 653.18, 655.38, 669.46, 686.62, 704.66, 725.78, 753.06, 787.82, 827.86, 878.46, 970.42, 1149.06, 1507.22,2200]),
                 ("m_{T}^{l#nu#gamma}","mt_res", 'GeV',[0, 150, 200, 250, 300, 350, 400, 500, 750, 1000, 2500]),
               ]
    plotvarsel=[]
    plotvarsmu=[]
    for ch, samples in zip(["el","mu"],[sampManElG,sampManMuG]):
    #for ch, samples in zip(["mu","el"],[sampManMuG,sampManElG]):
        labelname = "%i Muon Channel" %options.year if ch == "mu" else "%i Electron Channel" %options.year
        lepname = "e" if ch == "el" else "#mu"
        #labelname+=" scaled to 2016 luminosity"
        if ch == "el":
            selection , weight = defs.makeselstring(ch,  80, 35,  40)
        else:
            selection , weight = defs.makeselstring(ch,  80, 30,  40)
        if options.year == 2018:
            weight = weight.replace("prefweight","1")
        print(ch, samples)
        #weight =weight.replace("PUWeight","PUWeight*0.2")
        weight =weight.replace("PUWeight","PUWeight")
        print(selection ,weight)
        ## prepare config
        hist_config   = {"xlabel":"m_{T}(%s,#gamma,p^{miss}_{T})" %(lepname),"logy":1,"ymin":.02,"weight":weight, "ymax_scale":2.0, "unblind":False} 
        #hist_config   = {"xlabel":"m_{T}(%s,#gamma,p^{miss}_{T})" %(lepname),"logy":1,"ymin":.02,"weight":weight, "ymax_scale":2.0, "unblind":"Entry$%5==1"} ## "unblind":False
        label_config  = {"extra_label":labelname, "extra_label_loc":(.17,.82), "labelStyle":str(options.year)}
        legend_config = {'legendLoc':"Double","legendTranslateX":0.3, "legendCompress":1, "fillalpha":.5, "legendWiden":.9}

        if ch == "el":
            plotvars = plotvarsbase+plotvarsel
        if ch == "mu":
            plotvars = plotvarsbase+plotvarsmu
        print('plotvars',plotvars)

        for xlabel, var, unit, vrange in plotvars:
            print('xlabel, var, vrange', xlabel, var, vrange)
            hist_config["xlabel"] = xlabel
            hist_config["doratio"] = False
            hist_config["drawsignal"] = True
            hist_config["xunit"] = unit
            samples.Draw(var, selection,vrange , hist_config,legend_config,label_config)
            ## save histogram
            varname = var.replace("[","").replace("]","").replace(":","_")
            samples.SaveStack("%s_%i%s.pdf" %(varname,options.year, ch), options.outputDir, "base")
    return sampManMuG, sampManElG


sampmu,sampel = main()



