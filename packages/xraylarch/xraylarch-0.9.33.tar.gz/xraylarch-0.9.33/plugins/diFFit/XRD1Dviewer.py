#!/usr/bin/env pythonw
'''
GUI for displaying 1D XRD images

'''
import os
import numpy as np
import sys
import time
import re

from threading import Thread
from functools import partial

try:
    from cStringIO import StringIO #python 2
except:
    from io import StringIO #python 3

import wx
import wx.lib.agw.flatnotebook as flat_nb
import wx.lib.mixins.listctrl  as listmix

from wxmplot import PlotPanel
from wxmplot.basepanel import BasePanel
from wxutils import MenuItem,pack,EditableListBox,SimpleText

import larch
from larch_plugins.cifdb import (cifDB,SearchCIFdb,QSTEP,QMIN,CATEGORIES,SPACEGROUPS,
                                 match_database)
from larch_plugins.xrd import (d_from_q,twth_from_q,q_from_twth, lambda_from_E,
                               E_from_lambda,calcCIFpeaks,d_from_twth,
                               instrumental_fit_uvw,peakfinder,peaklocater,peakfitter,
                               peakfilter,xrd_background,xrd1d,calc_broadening)
from larch_plugins.xrmmap import read1DXRDFile

###################################

VERSION = '1 (03-April-2017)'

SLIDER_SCALE = 1000. ## sliders step in unit 1. this scales to 0.001
CIFSCALE = 1000

FIT_METHODS = ['scipy.signal.find_peaks_cwt']

FNB_STYLE = flat_nb.FNB_NO_X_BUTTON|flat_nb.FNB_SMART_TABS|flat_nb.FNB_NO_NAV_BUTTONS

CEN = wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL
LEFT = wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL
RIGHT = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL
ALL_CEN =  wx.ALL|CEN
ALL_LEFT =  wx.ALL|LEFT
ALL_RIGHT =  wx.ALL|RIGHT
###################################

def YesNo(parent, question, caption = 'Yes or no?'):
    dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
    return result

def calcFrameSize(x,y):
    '''
    Calculates an appropriate frame size based on user's display
    '''
    screenSize = wx.DisplaySize()
    if x > screenSize[0] * 0.9:
        x = int(screenSize[0] * 0.9)
        y = int(x*0.6)
        
    return x,y

def loadXYfile(event=None,parent=None,xrdviewer=None):

    wildcards = 'XRD data file (*.xy)|*.xy|All files (*.*)|*.*'
    dlg = wx.FileDialog(parent, message='Choose 1D XRD data file',
                        defaultDir=os.getcwd(),
                        wildcard=wildcards, style=wx.FD_OPEN)

    path, read = None, False
    if dlg.ShowModal() == wx.ID_OK:
        read = True
        path = dlg.GetPath().replace('\\', '/')
    dlg.Destroy()
    
    if read:
        data1dxrd = xrd1d(file=path)
        if xrdviewer is None:
            return data1dxrd
        else:
            xrdviewer.add1Ddata(data1dxrd)

class diFFit1DFrame(wx.Frame):
    def __init__(self,_larch=None):

        x,y = calcFrameSize(1500, 750)
        label = 'diFFit : 1D XRD Data Analysis Software'
        wx.Frame.__init__(self, None,title=label,size=(x,y))

        self.statusbar = self.CreateStatusBar(3,wx.CAPTION)

        panel = wx.Panel(self)
        self.nb = wx.Notebook(panel)
        
        self.openDB(dbname='amcsd_cif.db')

        ## create the page windows as children of the notebook
        self.xrd1Dviewer  = Viewer1DXRD(self.nb,owner=self)
        self.xrd1Dfitting = Fitting1DXRD(self.nb,owner=self)
        ## include database tab? #self.xrddatabase  = DatabaseXRD(self.nb,owner=self)

        ## add the pages to the notebook with the label to show on the tab
        self.nb.AddPage(self.xrd1Dviewer, 'Viewer')
        self.nb.AddPage(self.xrd1Dfitting, 'Fitting')
        ## include database tab? #self.nb.AddPage(self.xrddatabase, 'XRD Database')

        ## put the notebook in a sizer for the panel to manage the layout
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, -1, wx.EXPAND)
        panel.SetSizer(sizer)

        self.XRD1DMenuBar()

    def closeDB(self,event=None):

        self.cifdatabase.close_database()

    def openDB(self,dbname='amcsd_cif.db'):

        try:
            self.closeDB()
        except:
            pass

        self.cifdatabase = cifDB(dbname=dbname)

    def onExit(self, event=None):
        try:
            if hasattr(self.exit_callback, '__call__'):
                self.exit_callback()
        except:
            pass
        try:
            self.closeDB()
        except:
            pass

        try:
            self.Destroy()
        except:
            pass


    def XRD1DMenuBar(self):

        menubar = wx.MenuBar()

        ###########################
        ## diFFit1D
        diFFitMenu = wx.Menu()

        MenuItem(self, diFFitMenu, '&Open 1D dataset', '', self.xrd1Dviewer.load_file)
        MenuItem(self, diFFitMenu, 'Open &CIFile', '', self.xrd1Dviewer.loadCIF)
        MenuItem(self, diFFitMenu, 'Sa&ve displayed image to file', '', self.xrd1Dviewer.onSAVEfig)
#         MenuItem(self, diFFitMenu, '&Add analysis to map file', '', None)
        MenuItem(self, diFFitMenu, '&Quit', 'Quit program', self.onExit)
        
        menubar.Append(diFFitMenu, '&diFFit1D')


        ###########################
        ## Process
        #ProcessMenu = wx.Menu()
        #
        #MenuItem(self, ProcessMenu, 'Fit &background', '', None)
        #MenuItem(self, ProcessMenu, 'Save &background', '', None)
        #MenuItem(self, ProcessMenu, '&Remove current background', '', None)
        #
        #menubar.Append(ProcessMenu, '&Process')

        ###########################
        ## Analyze
        AnalyzeMenu = wx.Menu()

        MenuItem(self, AnalyzeMenu, '&Select data for fitting', '', self.fit1Dxrd)
        AnalyzeMenu.AppendSeparator()
        MenuItem(self, AnalyzeMenu, '&Change database', '', self.xrd1Dfitting.open_database)
        AnalyzeMenu.AppendSeparator()
        MenuItem(self, AnalyzeMenu, '&Fit instrumental broadening coefficients', '', self.xrd1Dfitting.fit_instrumental)

        menubar.Append(AnalyzeMenu, '&Analyze')

        ###########################
        ## Help
        HelpMenu = wx.Menu()
        
        MenuItem(self, HelpMenu, '&About', 'About diFFit1D viewer', self.onAbout)

        menubar.Append(HelpMenu, '&Help')
        
        ###########################
        ## Create Menu Bar
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_CLOSE, self.onExit)

    def write_message(self, s, panel=0):
        '''write a message to the Status Bar'''
        self.statusbar.SetStatusText(s, panel)

##############################################
#### HELP FUNCTIONS
    def onAbout(self, event=None):
        info = wx.AboutDialogInfo()
        info.SetName('diFFit1D XRD Data Viewer')
        desc = 'Using X-ray Larch version: %s' % larch.version.__version__
        info.SetDescription(desc)
        info.SetVersion(VERSION)
        info.AddDeveloper('Margaret Koker: koker at cars.uchicago.edu')
        dlg = wx.AboutBox(info)

##############################################
#### 
    def fit1Dxrd(self,event=None):
        '''
        GUI interface for loading data to fitting panel (from data in viewer or file)
        mkak 2017.03.23
        '''
        xrdv = self.xrd1Dviewer
        xrdf = self.xrd1Dfitting
        
        indicies = [i for i,name in enumerate(xrdv.data_name) if 'cif' not in name]
        okay = False

        xi = xrdv.ch_xaxis.GetSelection()
        xrdf.rngpl.ch_xaxis.SetSelection(xi)

        if len(indicies) > 0:
            self.list = [xrdv.data_name[i] for i in indicies]
            self.all_data = xrdv.xy_data
            dlg = SelectFittingData(self)
            if dlg.ShowModal() == wx.ID_OK:
                okay = True
                index = dlg.slct_1Ddata.GetSelection()
            dlg.Destroy()
        else:
            index = -1
            loadXYfile(parent=self,xrdviewer=xrdv)
            if len(xrdv.xy_data) > 0: okay = True
        if okay:
            seldat = xrdv.xy_data[index]
            self.nb.SetSelection(1) ## switches to fitting panel

            adddata = True
            if xrdf.xrd1dgrp is not None:
                question = 'Replace current data file %s with selected file %s?' % \
                               (xrdf.xrd1dgrp.label,name)
                adddata = YesNo(self,question,caption='Overwrite warning')

            if adddata:

                if xrdf.xrd1dgrp is not None:
                    xrdf.reset_fitting()

                xrdf.xrd1dgrp = seldat
                xrdf.xrd1dgrp.label = xrdf.xrd1dgrp.label
                xrdf.plt_data = xrdf.xrd1dgrp.all_data()

                xrdf.xmin     = np.min(xrdf.plt_data[xi])
                xrdf.xmax     = np.max(xrdf.plt_data[xi])
                


                xrdf.optionsON()
                xrdv.optionsON()
                xrdf.check1Daxis()
                
                xrdf.ttl_energy.SetLabel('Energy: %0.3f keV (%0.4f A)' % (seldat.energy,
                                                                          seldat.wavelength))

class SelectFittingData(wx.Dialog):
    def __init__(self,parent):

        """Constructor"""
        dialog = wx.Dialog.__init__(self, parent, title='Select data for fitting',
                                    style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.OK)
                                    #size = (210,410))
        self.parent = parent
        self.createPanel()

        ix,iy = self.panel.GetBestSize()
        self.SetSize((ix+20, iy+20))

    def createPanel(self):

        self.panel = wx.Panel(self)
        mainsizer = wx.BoxSizer(wx.VERTICAL)

        ## Add things
        self.slct_1Ddata = wx.ListBox(self.panel, 26, wx.DefaultPosition, (170, 130),
                                      self.parent.list, wx.LB_SINGLE)
        btn_new = wx.Button(self.panel,label='Load data from file')
        btn_new.Bind(wx.EVT_BUTTON, self.load_file)

        #####
        ## OKAY!
        oksizer = wx.BoxSizer(wx.HORIZONTAL)
        #hlpBtn = wx.Button(self.panel, wx.ID_HELP    )
        self.okBtn  = wx.Button(self.panel, wx.ID_OK      )
        canBtn = wx.Button(self.panel, wx.ID_CANCEL  )

        #oksizer.Add(hlpBtn,flag=wx.RIGHT,  border=8)
        oksizer.Add(canBtn, flag=wx.RIGHT, border=8)
        oksizer.Add(self.okBtn,  flag=wx.RIGHT,  border=8)

        mainsizer.Add(self.slct_1Ddata, flag=wx.ALL, border=8)
        mainsizer.AddSpacer(15)
        mainsizer.Add(btn_new, flag=wx.ALL, border=5)
        mainsizer.AddSpacer(15)
        mainsizer.Add(oksizer, flag=wx.ALL|wx.ALIGN_RIGHT, border=10)

        self.panel.SetSizer(mainsizer)

    def load_file(self,event=None):

        loadXYfile(parent=self,xrdviewer=self.parent.xrd1Dviewer)

        self.parent.list.append(self.parent.xrd1Dviewer.data_name[-1])
        self.slct_1Ddata.Set(self.parent.list)
        self.slct_1Ddata.SetSelection(-1)

class Fitting1DXRD(BasePanel):
    '''
    Panel for housing 1D XRD fitting
    '''
    label='Fitting'
    def __init__(self,parent,owner=None,_larch=None):

        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.owner = owner

        ## Default information
        self.xrd1dgrp   = None
        self.plt_data   = None

        self.plt_peaks  = None
        self.peaklist   = []

        self.xmin       = None
        self.xmax       = None
        self.x, self.y  = 0,0

        self.xlabel     = 'q (1/$\AA$)' #'q (A^-1)'
        self.ylabel     = 'Intensity (a.u.)'
        self.xunit      = '1/A'
        self.dlimit     = 7.5 # A -> 2th = 5 deg.; q = 0.8 1/A
        
        self.SetFittingDefaults()
        self.Panel1DFitting()

    def SetFittingDefaults(self):

        # Peak fitting defaults
        self.iregions = 20
        self.gapthrsh = 5
        self.halfwidth = 40
        self.intthrsh = 100

        # Background fitting defaults
        self.exponent   = 20
        self.compress   = 2
        self.width      = 4

##############################################
#### PANEL DEFINITIONS
    def Panel1DFitting(self):
        '''
        Frame for housing all 1D XRD viewer widgets
        '''
        leftside  = self.LeftSidePanel(self)
        rightside = self.RightSidePanel(self)

        panel1D = wx.BoxSizer(wx.HORIZONTAL)
        panel1D.Add(leftside,flag=wx.ALL,border=10)
        panel1D.Add(rightside,proportion=1,flag=wx.EXPAND|wx.ALL,border=10)

        self.SetSizer(panel1D)


    def showCIF(self, event=None, **kws):

        if event is not None and self.xrd1dgrp is not None:
            cifname = event.GetString()
            amcsd_id = int(cifname.split()[0])
            ciffile = '/%s' % cifname
            
            energy = self.xrd1dgrp.energy
            wavelength = self.xrd1dgrp.wavelength
            maxI = np.max(self.plt_data[3])*0.8
            maxq = np.max(self.plt_data[0])*1.05
            
            xi = self.rngpl.ch_xaxis.GetSelection()
        
            cifmatch = self.owner.cifdatabase.return_cif(amcsd_id)
            qall,Fall = calcCIFpeaks(ciffile,energy,verbose=True,fid=StringIO(cifmatch),qmax=maxq)
            Fall = Fall/max(Fall)*maxI            

            self.plot_data()
            cifargs = {'label':cifname,'title':self.xrd1dgrp.label,'color':'green','label':cifname,'xlabel':self.xlabel,'ylabel':self.ylabel,'marker':'','markersize':0,'show_legend':True}
            try:
                cif = []
                for i,F in enumerate(Fall):
                    if F != 0: cif.append([qall[i], twth_from_q(qall[i],wavelength), d_from_q(qall[i]), F])
                cif = np.array(zip(*cif))
                u,v,w = self.xrd1dgrp.uvw
                D = self.xrd1dgrp.D
                F = calc_broadening(cif,self.plt_data[1],wavelength,u=u,v=v,w=w,D=D)
                self.plot1D.oplot(self.plt_data[xi],F,**cifargs)  
            except:
                cifpks = np.array([qall, twth_from_q(qall,wavelength), d_from_q(qall), Fall])
                self.plot1D.oplot(cifpks[xi],cifpks[3],**cifargs)

    
    def createFittingPanels(self,parent):
        
        pattern_title    = SimpleText(parent, 'DATABASE FILTERING', size=(200, -1))

        #self.pnb = flat_nb.FlatNotebook(parent, wx.ID_ANY, agwStyle=FNB_STYLE)
        self.pnb = wx.Notebook(parent)
        self.pnbpanels = []

        self.srchpl = SearchPanel(self.pnb, owner=self)
        self.instpl = InstrPanel(self.pnb, owner=self)
        self.rtgpl = ResultsPanel(self.pnb, owner=self)
        for p in (self.instpl, self.srchpl, self.rtgpl):
            self.pnb.AddPage(p,p.label.title(),True)
            self.pnbpanels.append(p)
            p.SetSize((300,600))

        self.pnb.SetSelection(1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(pattern_title, 0, ALL_CEN)
        sizer.Add(self.pnb,1, wx.ALL|wx.EXPAND)
        parent.SetSize((300,600))
        pack(parent,sizer)


    def FilterTools(self,panel):
        '''
        Frame for visual toolbox
        '''

        vbox = wx.BoxSizer(wx.VERTICAL)

        fitting_panel = wx.Panel(panel)
        self.createFittingPanels(fitting_panel)
        vbox.Add(fitting_panel, flag=wx.ALL, border=10)

        return vbox


    def createPatternPanels(self,parent):

        pattern_title    = SimpleText(parent, 'PATTERN PROCESSING', size=(200, -1))
        #self.pnb = flat_nb.FlatNotebook(parent, wx.ID_ANY, agwStyle=FNB_STYLE)
        self.pnb = wx.Notebook(parent)
        self.pnbpanels = []

        self.rngpl = RangeToolsPanel(self.pnb, owner=self)
        self.bkgdpl = BackgroundToolsPanel(self.pnb, owner=self)
        self.pkpl = PeakToolsPanel(self.pnb, owner=self)
        for p in (self.rngpl, self.bkgdpl, self.pkpl):
            self.pnb.AddPage(p,p.label.title(),True)
            self.pnbpanels.append(p)
            p.SetSize((300,600))

        self.pnb.SetSelection(0)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(pattern_title, 0, ALL_CEN)
        sizer.Add(self.pnb,1, wx.ALL|wx.EXPAND)
        parent.SetSize((300,600))
        pack(parent,sizer)


    def PatternTools(self,panel):
        '''
        Frame for visual toolbox
        '''

        vbox = wx.BoxSizer(wx.VERTICAL)

        pattern_panel = wx.Panel(panel)
        self.createPatternPanels(pattern_panel)
        vbox.Add(pattern_panel, flag=wx.ALL, border=10)

        return vbox

    def MatchPanel(self,panel):
        '''
        Matches
        '''
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.txt_amcsd_cnt = wx.StaticText(self, label='')
        vbox.Add(self.txt_amcsd_cnt, flag=wx.LEFT, border=10)
        
        return vbox

    def LeftSidePanel(self,panel):

        vbox = wx.BoxSizer(wx.VERTICAL)

        pattools = self.PatternTools(self)
        vbox.Add(pattools,flag=wx.TOP|wx.LEFT,border=10)
       
        filtools = self.FilterTools(self)
        vbox.Add(filtools,flag=wx.TOP|wx.LEFT,border=10)
        
        matchbx = self.MatchPanel(self)
        vbox.Add(matchbx,flag=wx.LEFT,border=10)        

        return vbox

    def SettingsPanel(self,panel):

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.ttl_energy = wx.StaticText(self, label=('Energy: %0.3f keV (%0.4f A)' % (0,0)))

        vbox.Add(self.ttl_energy, flag=wx.EXPAND|wx.ALL, border=8)

        return vbox

    def RightSidePanel(self,panel):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.plot1DXRD(panel)

        settings = self.SettingsPanel(self)
        btnbox = self.QuickButtons(panel)

        vbox.Add(self.plot1D,proportion=1,flag=wx.ALL|wx.EXPAND,border = 10)
        hbox.Add(settings,flag=wx.RIGHT,border=10)
        hbox.Add(btnbox,flag=wx.LEFT,border = 1)
        vbox.Add(hbox,flag=wx.ALL|wx.ALIGN_RIGHT,border = 10)
        return vbox

    def QuickButtons(self,panel):
        buttonbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_img = wx.Button(panel,label='SAVE FIGURE')
        btn_calib = wx.Button(panel,label='PLOT SETTINGS')
        btn_integ = wx.Button(panel,label='RESET PLOT')

        btn_img.Bind(wx.EVT_BUTTON,   self.onSAVEfig)
        btn_calib.Bind(wx.EVT_BUTTON, self.onPLOTset)
        btn_integ.Bind(wx.EVT_BUTTON, self.onRESETplot)

        buttonbox.Add(btn_img, flag=wx.ALL, border=8)
        buttonbox.Add(btn_calib, flag=wx.ALL, border=8)
        buttonbox.Add(btn_integ, flag=wx.ALL, border=8)
        return buttonbox


##############################################
#### DATA CALCULATIONS FUNCTIONS

    def plot_data(self,event=None):

        xi = self.rngpl.ch_xaxis.GetSelection()
        pltargs = {'title':self.xrd1dgrp.label,'color':'blue','label':'Data','xlabel':self.xlabel,'ylabel':self.ylabel,'marker':'','markersize':0,'show_legend':True}
        self.plot1D.plot(self.plt_data[xi],self.plt_data[3],**pltargs)
        
        self.plot_background()
        self.plot_peaks()

        self.rescale1Daxis(xaxis=True,yaxis=False)

##############################################
#### RANGE FUNCTIONS

    def reset_fitting(self,name=None,min=0,max=1):

        self.xrd1dgrp.label = name

        self.rngpl.val_xmin.SetValue('%0.3f' % min)
        self.rngpl.val_xmax.SetValue('%0.3f' % max)
        self.rngpl.ch_xaxis.SetSelection(0)

        self.pkpl.btn_fdpks.Enable()
        self.pkpl.btn_opks.Enable()

        self.bkgdpl.btn_obkgd.Enable()
        self.bkgdpl.btn_fbkgd.Enable()
        self.bkgdpl.btn_rbkgd.Disable()
        self.bkgdpl.ck_bkgd.SetValue(False)
        self.bkgdpl.ck_bkgd.Disable()
        
        self.xmin     = min
        self.xmax     = max
        self.trim_data()
        self.delete_all_peaks()
        self.remove_background()

        self.SetFittingDefaults()
        self.plot_data()

    def onSetRange(self,event=None):

        self.check_range()
        self.trim_data()
        
        self.plot_data()

    def check_range(self,event=None):

        xmin,xmax = self.rngpl.val_xmin,self.rngpl.val_xmax
        minval,maxval = float(xmin.GetValue()),float(xmax.GetValue())

        xi = self.rngpl.ch_xaxis.GetSelection()
        x = self.xrd1dgrp.slct_xaxis(xi=xi)

        if abs(self.xmax-maxval) > 0.005 or abs(self.xmin-minval) > 0.005:
            if xmax < minval: minval,maxval = float(xmax.GetValue()),float(xmin.GetValue())
            self.xmin = max(minval,np.min(x))
            self.xmax = min(maxval,np.max(x))

            if xi == 2: self.xmax = min(self.xmax,self.dlimit)
            
            self.delete_all_peaks()
            self.remove_background()

        xmin.SetValue('%0.3f' % self.xmin)
        xmax.SetValue('%0.3f' % self.xmax)

    def onReset(self,event=None):

        self.plt_peaks,self.xrd1dgrp.pki = None,[]
        self.peaklist = []

        self.reset_range()
        self.plot_data()

    def reset_range(self,event=None):

        xi = self.rngpl.ch_xaxis.GetSelection()
        x = self.xrd1dgrp.slct_xaxis(xi=xi)

        self.xmin,self.xmax = np.min(x),np.max(x)
        if xi == 2: self.xmax = min(self.xmax,self.dlimit)

        self.rngpl.val_xmin.SetValue('%0.3f' % self.xmin)
        self.rngpl.val_xmax.SetValue('%0.3f' % self.xmax)

        self.trim_data()
        self.remove_background()

    def trim_data(self):

        xi = self.rngpl.ch_xaxis.GetSelection()
        self.xrd1dgrp.set_trim(self.xmin,self.xmax,xi=xi)
        self.plt_data = self.xrd1dgrp.all_data()

##############################################
#### BACKGROUND FUNCTIONS

    def onFitBkgd(self,event=None):

        self.xrd1dgrp.fit_background()
        self.plt_data = self.xrd1dgrp.plot(bkgd=False)

        self.plot_data()
        
        self.bkgdpl.btn_rbkgd.Enable()
        self.bkgdpl.ck_bkgd.Enable()

    def onSbtrctBkgd(self,event=None):

        self.plt_data = self.xrd1dgrp.plot(bkgd=self.bkgdpl.ck_bkgd.GetValue())
        self.plot_data()


    def onRmvBkgd(self,event=None):

        self.remove_background()
        self.plot_data()

    def remove_background(self,event=None):

        self.xrd1dgrp.reset_bkgd()
        self.plt_data = self.xrd1dgrp.plot(bkgd=False)

        self.bkgdpl.ck_bkgd.SetValue(False)
        self.bkgdpl.ck_bkgd.Disable()
        self.bkgdpl.btn_rbkgd.Disable()

    def plot_background(self,event=None):

        if self.xrd1dgrp is not None and not self.bkgdpl.ck_bkgd.GetValue():
            if np.max(self.plt_data[4]) > 0:
                xi = self.rngpl.ch_xaxis.GetSelection()
                bgrarg = {'title':self.xrd1dgrp.label,'color':'red','label':'Background','xlabel':self.xlabel,'ylabel':self.ylabel,'marker':'','markersize':0,'show_legend':True}
                self.plot1D.oplot(self.plt_data[xi],self.plt_data[4],**bgrarg)

    def background_options(self,event=None):

        myDlg = BackgroundOptions(self)

        fit = False
        if myDlg.ShowModal() == wx.ID_OK:
            self.exponent = int(myDlg.val_exp.GetValue())
            self.compress = int(myDlg.val_comp.GetValue())
            self.width    = int(myDlg.val_wid.GetValue())
            fit = True
        myDlg.Destroy()

        if fit:
            self.onFitBkgd()


##############################################
#### PEAK FUNCTIONS

    def onPeaks(self,event=None,filter=False):

        self.find_peaks(filter=filter)

        if len(self.xrd1dgrp.pki) > 0:
            self.srchpl.owner.val_gdnss.Enable()
            self.srchpl.btn_mtch.Enable()

    def onAddPks(self,event=None):
        
        xi = self.rngpl.ch_xaxis.GetSelection()
        idx = (np.abs(self.plt_data[xi]-self.x)).argmin()
        self.xrd1dgrp.pki.append(idx)

        self.peak_display()
        self.plot_data()
    
    def onRmvPksAll(self,event=None,filter=False):

        self.remove_all_peaks()
        self.srchpl.owner.val_gdnss.Disable()
        self.srchpl.btn_mtch.Disable()

    def find_peaks(self,event=None,filter=False):

        newpeaks = True
        if len(self.xrd1dgrp.pki) > 0:
            question = 'Are you sure you want to remove current peaks and search again?'
            newpeaks = YesNo(self,question,caption='Replace peaks warning')

        if newpeaks:
            xi = self.rngpl.ch_xaxis.GetSelection()

            ## clears previous searches
            self.remove_all_peaks()

            self.intthrsh = int(self.pkpl.val_intthr.GetValue())
            self.xrd1dgrp.find_peaks(bkgd=self.bkgdpl.ck_bkgd.GetValue(),threshold=self.intthrsh)
                    
            self.peak_display()
            self.plot_peaks()

            self.pkpl.btn_rmvpks.Enable()
            
    def peak_display(self):

        self.define_peaks()

        self.peaklist = []
        self.peaklistbox.Clear()

        str = 'Peak (%6d cts @ %2.3f %s )'
        xi = self.rngpl.ch_xaxis.GetSelection()
        for i,ii in enumerate(self.xrd1dgrp.pki):
            peakname = str % (self.plt_peaks[3,i],self.plt_peaks[xi,i],self.xunit)
            self.peaklist += [peakname]
            self.peaklistbox.Append(peakname)
        self.pkpl.ttl_cntpks.SetLabel('Total: %i peaks' % (len(self.xrd1dgrp.pki)))

    def onClrInstr(self,event=None):
            
        self.xrd1dgrp.uvw = None
        self.instpl.val_u.SetValue('1.0')
        self.instpl.val_v.SetValue('1.0')
        self.instpl.val_w.SetValue('1.0')

    def onClrSize(self,event=None):
            
        self.xrd1dgrp.D = None
        self.instpl.val_D.SetValue('')

    def onGetSize(self,event=None):
            
        try:
            self.xrd1dgrp.D = float(self.instpl.val_D.GetValue())
        except:
            self.onClrSize()

    def onSetInstr(self,event=None):
        u,v,w = self.xrd1dgrp.uvw
        self.instpl.val_u.SetValue('%0.6f' % u)
        self.instpl.val_v.SetValue('%0.6f' % v)
        self.instpl.val_w.SetValue('%0.6f' % w)

    def onGetInstr(self,event=None):
            
        try:
            self.xrd1dgrp.uvw = (float(self.instpl.val_u.GetValue()),
                                 float(self.instpl.val_v.GetValue()),
                                 float(self.instpl.val_w.GetValue()))
            self.onSetInstr()
        except:
            self.onClrInstr()
            

    def fit_instrumental(self,event=None):

        try:
            self.xrd1dgrp.uvw = instrumental_fit_uvw(self.xrd1dgrp.pki,
                                                     self.plt_data[1],self.plt_data[3],
                                                     halfwidth=self.halfwidth,
                                                     verbose=False)
            self.onSetInstr()
        except:
            pass

#     def fit_peaks(self,event=None):
#         
#         pktwth,pkFWHM,pkI = peakfitter(self.xrd1dgrp.pki,self.plt_data[1],self.plt_data[3],
#                                                 halfwidth=self.halfwidth,
#                                                 fittype='double',
#                                                 verbose=True)
#         print('\nFit results:')
#         for i,(twthi,fwhmi,inteni) in enumerate(zip(pktwth,pkFWHM,pkI)):
#             print('Peak %i @ %0.2f deg. (fwhm %0.3f deg, %i counts)' % (i,twthi,fwhmi,inteni))
#         print
#         
#         ## Updates variable and plot with fit results
#         wavelength = self.xrd1dgrp.wavelength
#         self.plt_peaks = np.zeros((4,len(pktwth)))
#         self.plt_peaks[0] = q_from_twth(pktwth,wavelength)
#         self.plt_peaks[1] = pktwth
#         self.plt_peaks[2] = d_from_twth(pktwth,wavelength)
#         self.plt_peaks[3] = pkI
# 
#         self.plot_data()

    def plot_peaks(self):

        if len(self.xrd1dgrp.pki) > 0:
            self.define_peaks()

            xi = self.rngpl.ch_xaxis.GetSelection()
            pkarg = {'marker':'o','color':'red','markersize':8,'linewidth':0,'label':'Found peaks','show_legend':True}
            self.plot1D.oplot(self.plt_peaks[xi],self.plt_peaks[3],**pkarg)

    def remove_all_peaks(self,event=None):

        self.delete_all_peaks()
        self.plot_data()

        self.pkpl.btn_rmvpks.Disable()

    def delete_all_peaks(self,event=None):

        self.plt_peaks,self.xrd1dgrp.pki = None,[]

        self.peaklist = []
        self.peaklistbox.Clear()
        self.pkpl.ttl_cntpks.SetLabel('Total: 0 peaks')

    def peak_options(self,event=None):

        myDlg = PeakOptions(self)

        fit = False
        if myDlg.ShowModal() == wx.ID_OK:
            self.iregions  = int(myDlg.val_regions.GetValue())
            self.gapthrsh  = int(myDlg.val_gapthr.GetValue())
            self.halfwidth = int(myDlg.val_hw.GetValue())
#             self.intthrsh  = int(myDlg.val_intthr.GetValue())
            fit = True
        myDlg.Destroy()

        if fit:
            self.find_peaks(filter=True)

    def select_peak(self, evt=None, peakname=None,  **kws):

        if peakname is None and evt is not None:
            peakname = evt.GetString()

    def define_peaks(self):
    
        peaks=np.zeros((5,len(self.xrd1dgrp.pki)))
        for axis,data in enumerate(self.plt_data):
            peaks[axis] = peaklocater(self.xrd1dgrp.pki,data)
        self.plt_peaks = peaks
    
    def rm_sel_peaks(self, peakname, event=None):

        if peakname in self.peaklist:

            pki = self.peaklist.index(peakname)

            self.peaklist.pop(pki)
            self.xrd1dgrp.pki.pop(pki)

            self.define_peaks()

            self.plot_data()

        self.pkpl.ttl_cntpks.SetLabel('Total: %i peaks' % (len(self.xrd1dgrp.pki)))

##############################################
#### PLOTPANEL FUNCTIONS
    def plot1DXRD(self,panel):

        self.plot1D = PlotPanel(panel,size=(1000, 500),messenger=self.owner.write_message)
        self.plot1D.cursor_mode = 'zoom'
        self.plot1D.cursor_callback = self.on_cursor

    def on_cursor(self,x=None, y=None, **kw):
        self.x,self.y = x,y

    def onSAVEfig(self,event=None):
        self.plot1D.save_figure()

    def onPLOTset(self,event=None):
        self.plot1D.configure()

    def onRESETplot(self,event=None):
        self.plot1D.reset_config()

    def onChangeXscale(self,event=None):

        self.check1Daxis()

    def optionsON(self,event=None):

        ## RangeToolsPanel
        self.rngpl.ch_xaxis.Enable()
        self.rngpl.val_xmin.Enable()
        self.rngpl.val_xmax.Enable()
        self.rngpl.btn_rngreset.Enable()
        ## BackgroundToolsPanel
        self.bkgdpl.btn_fbkgd.Enable()
        self.bkgdpl.btn_obkgd.Enable()
        self.bkgdpl.btn_rbkgd.Disable()
        self.bkgdpl.ck_bkgd.Disable()
        ## PeakToolsPanel
        self.pkpl.btn_fdpks.Enable()
        self.pkpl.btn_opks.Enable()
        self.pkpl.val_intthr.Enable()
        self.pkpl.btn_rmvpks.Disable() #Enable()
        self.pkpl.btn_addpks.Enable()
        ## InstrumentToolsPanel
        self.instpl.val_u.Enable()
        self.instpl.val_v.Enable()
        self.instpl.val_w.Enable()
        self.instpl.val_D.Enable()
        self.instpl.btn_clrinst.Enable()
        self.instpl.btn_clrsize.Enable()


    def check1Daxis(self,event=None,yaxis=False):

        xi = self.rngpl.ch_xaxis.GetSelection()
        minx,maxx = np.min(self.plt_data[xi]),np.max(self.plt_data[xi])
        if xi == 2: maxx = min(maxx,self.dlimit)
                
        self.rngpl.val_xmin.SetValue('%0.3f' % minx)
        self.rngpl.val_xmax.SetValue('%0.3f' % maxx)

        ## d
        if xi == 2:
            self.xlabel = 'd ($\AA$)'
            self.xunit = 'A' #'$\AA$'
        ## 2theta
        elif xi == 1:
            self.xlabel = r'$2\Theta$'+r' $(^\circ)$'
            self.xunit = 'deg.' #'$(^\circ)$'
        ## q
        else:
            self.xlabel = 'q (1/$\AA$)'
            self.xunit = '1/A' #'1/$\AA$'
        self.rngpl.unit_xmin.SetLabel(self.xunit)
        self.rngpl.unit_xmax.SetLabel(self.xunit)

        self.plot_data()

    def rescale1Daxis(self,xaxis=True,yaxis=False):

        xi = self.rngpl.ch_xaxis.GetSelection()
        x,y = self.plt_data[xi],self.plt_data[3]

        if xaxis: self.set_xview(np.min(x), np.max(x))
        if yaxis: self.set_yview(np.min(y), np.max(y))

    def set_xview(self, x1, x2):

        xi = self.rngpl.ch_xaxis.GetSelection()
        xmin,xmax = np.min(self.plt_data[xi]),np.max(self.plt_data[xi])

        x1,x2 = max(xmin,x1),min(xmax,x2)
        if xi == 2: x2 = min(x2,self.dlimit)

        self.plot1D.axes.set_xlim((x1, x2))
        self.plot1D.canvas.draw()

    def set_yview(self, y1, y2):

        ymin,ymax = np.min(plt_data[3]),np.max(plt_data[3])
        y1,y2 = max(ymin,y1),min(ymax,y2)

        self.plot1D.axes.set_ylim((y1, y2))
        self.plot1D.canvas.draw()

##############################################
#### DATABASE FUNCTIONS

    def database_info(self,event=None):

        
        myDlg = DatabaseInfoGUI(self)

        change = False
        if myDlg.ShowModal() == wx.ID_OK:
#             self.elem_include = myDlg.incl_elm
#             self.elem_exclude = myDlg.excl_elm
            change = True
        myDlg.Destroy()        

    def open_database(self,event=None):

        wildcards = 'AMCSD database file (*.db)|*.db|All files (*.*)|*.*'
        dlg = wx.FileDialog(self, message='Choose AMCSD database file',
                           defaultDir=os.getcwd(),
                           wildcard=wildcards, style=wx.FD_OPEN)

        path, read = None, False
        if dlg.ShowModal() == wx.ID_OK:
            read = True
            path = dlg.GetPath().replace('\\', '/')
        dlg.Destroy()

        if read:
            try:
                self.owner.openDB(dbname=path)
                print('Now using database: %s' % os.path.split(path)[-1])
            except:
               print('Failed to import file as database: %s' % path)
               
        return path


    def filter_database(self,event=None):

        myDlg = XRDSearchGUI(self)
        

        filter = False
        if myDlg.ShowModal() == wx.ID_OK:
            
            self.elem_include = myDlg.srch.elem_incl
            self.elem_exclude = myDlg.srch.elem_excl
            filter = True
            if myDlg.Mineral.IsTextEmpty():
                self.mnrl_include = None
            else: 
                self.mnrl_include = myDlg.Mineral.GetStringSelection()
            if myDlg.Author.GetValue() == '':
                self.auth_include = None
            else: 
                self.auth_include = myDlg.Author.GetValue().split(',')
        myDlg.Destroy()

        list_amcsd = None
        if filter == True:
            cif = self.owner.cifdatabase
            if len(self.elem_include) > 0 or len(self.elem_exclude) > 0:
                list_amcsd = cif.amcsd_by_chemistry(include=self.elem_include,
                                                    exclude=self.elem_exclude,
                                                    list=list_amcsd)
            if self.mnrl_include is not None:
                list_amcsd = cif.amcsd_by_mineral(include=self.mnrl_include,
                                                  list=list_amcsd)
            if self.auth_include is not None:
                list_amcsd = cif.amcsd_by_author(include=self.auth_include,
                                                 list=list_amcsd)
        self.displayMATCHES(list_amcsd)


    def onMatch(self,event=None):

        gdness = float(self.val_gdnss.GetValue())
        if gdness > 1 or gdness < 0:
            self.val_gdnss.SetValue('0.85')
            gdness = float(self.val_gdnss.GetValue())
        list_amcsd = match_database(fracq=gdness,q=self.plt_data[0],ipks=self.xrd1dgrp.pki,
                                    cifdatabase=self.owner.cifdatabase)
        self.displayMATCHES(list_amcsd)
        
    def displayMATCHES(self,list_amcsd):
        '''
        Populates Results Panel with list
        '''
        self.rtgpl.amcsdlistbox.Clear()

        if list_amcsd is not None:
            for amcsd in list_amcsd:
                elem,name,spgp,autr = self.owner.cifdatabase.all_by_amcsd(amcsd)
                entry = '%i : %s' % (amcsd,name)
                self.rtgpl.amcsdlistbox.Append(entry)
            if len(list_amcsd) == 1:
                self.txt_amcsd_cnt.SetLabel('1 MATCH')
            elif len(list_amcsd) > 1:
                self.txt_amcsd_cnt.SetLabel('%i MATCHES' % len(list_amcsd))
            else:
                self.txt_amcsd_cnt.SetLabel('')
                
        self.rtgpl.btn_clr.Enable()

    def clearMATCHES(self,list_amcsd):
        '''
        Populates Results Panel with list
        '''
        self.rtgpl.amcsdlistbox.Clear()
        self.txt_amcsd_cnt.SetLabel('')
        self.rtgpl.btn_clr.Disable()        
        
        self.plot_data()

class BackgroundOptions(wx.Dialog):
    def __init__(self,parent):

        """Constructor"""
        dialog = wx.Dialog.__init__(self, parent, title='Background fitting options',
                                    style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER,
                                    size = (210,410))
        self.parent = parent

        self.createPanel()

        ## Set defaults
        self.val_exp.SetValue(str(self.parent.exponent))
        self.val_comp.SetValue(str(self.parent.compress))
        self.val_wid.SetValue(str(self.parent.width))

        ix,iy = self.panel.GetBestSize()
        self.SetSize((ix+20, iy+20))

    def createPanel(self):

        self.panel = wx.Panel(self)

        mainsizer = wx.BoxSizer(wx.VERTICAL)

        ## Exponent
        expsizer = wx.BoxSizer(wx.VERTICAL)

        ttl_exp = wx.StaticText(self.panel, label='EXPONENT')

        self.val_exp = wx.TextCtrl(self.panel,wx.TE_PROCESS_ENTER)
        expsizer.Add(ttl_exp,  flag=wx.RIGHT, border=5)
        expsizer.Add(self.val_exp,  flag=wx.RIGHT, border=5)

        ## Compress
        compsizer = wx.BoxSizer(wx.VERTICAL)

        ttl_comp = wx.StaticText(self.panel, label='COMPRESS')

        self.val_comp = wx.TextCtrl(self.panel,wx.TE_PROCESS_ENTER)
        compsizer.Add(ttl_comp,  flag=wx.RIGHT, border=5)
        compsizer.Add(self.val_comp,  flag=wx.RIGHT, border=5)

        ## Width
        widsizer = wx.BoxSizer(wx.VERTICAL)

        ttl_wid = wx.StaticText(self.panel, label='WIDTH')

        self.val_wid = wx.TextCtrl(self.panel,wx.TE_PROCESS_ENTER)
        widsizer.Add(ttl_wid,  flag=wx.RIGHT, border=5)
        widsizer.Add(self.val_wid,  flag=wx.RIGHT, border=5)


        #####
        ## OKAY!
        oksizer = wx.BoxSizer(wx.HORIZONTAL)

        hlpBtn     = wx.Button(self.panel, wx.ID_HELP   )
        self.okBtn = wx.Button(self.panel, wx.ID_OK     )
        canBtn     = wx.Button(self.panel, wx.ID_CANCEL )

        hlpBtn.Bind(wx.EVT_BUTTON, lambda evt: wx.TipWindow(
            self, 'These values are specific to the background fitting defined in:'
            ' Nucl. Instrum. Methods (1987) B22, 78-81.\n'
            ' EXPONENT : Specifies the power of polynomial which is used.\n'
            ' COMPRESS : Compression factor to apply before fitting the background.\n'
            ' WIDTH : Specifies the width of the polynomials which are concave downward.'))

        oksizer.Add(hlpBtn,     flag=wx.RIGHT,  border=8 )
        oksizer.Add(canBtn,     flag=wx.RIGHT,  border=8 )
        oksizer.Add(self.okBtn, flag=wx.RIGHT,  border=8 )

        mainsizer.Add(expsizer,  flag=wx.ALL, border=8)
        mainsizer.AddSpacer(15)
        mainsizer.Add(compsizer, flag=wx.ALL, border=5)
        mainsizer.AddSpacer(15)
        mainsizer.Add(widsizer,  flag=wx.ALL, border=8)
        mainsizer.AddSpacer(15)
        mainsizer.Add(oksizer,   flag=wx.ALL|wx.ALIGN_RIGHT, border=10)


        self.panel.SetSizer(mainsizer)

class PeakOptions(wx.Dialog):
    def __init__(self,parent):

        """Constructor"""
        dialog = wx.Dialog.__init__(self, parent, title='Peak searching options',
                                    style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER,
                                    size = (210,410))
        self.parent = parent

        self.createPanel()

        ## Set defaults
        self.val_regions.SetValue(str(self.parent.iregions))
        self.val_gapthr.SetValue(str(self.parent.gapthrsh))
        self.val_hw.SetValue(str(self.parent.halfwidth))
#         self.val_intthr.SetValue(str(self.parent.intthrsh))

        ix,iy = self.panel.GetBestSize()
        self.SetSize((ix+20, iy+20))

    def createPanel(self):

        self.panel = wx.Panel(self)

        mainsizer = wx.BoxSizer(wx.VERTICAL)

        ##  Fit type
        fitsizer = wx.BoxSizer(wx.VERTICAL)

        ttl_fit = wx.StaticText(self.panel, label='Fit type')
        self.ch_pkfit = wx.Choice(self.panel,choices=FIT_METHODS)

        self.ch_pkfit.Bind(wx.EVT_CHOICE, None)

        fitsizer.Add(ttl_fit,  flag=wx.RIGHT, border=5)
        fitsizer.Add(self.ch_pkfit,  flag=wx.RIGHT, border=5)

         ## Regions
        hwsizer = wx.BoxSizer(wx.VERTICAL)

        ttl_hw = wx.StaticText(self.panel, label='Number of data points in half width')
        self.val_hw = wx.TextCtrl(self.panel,wx.TE_PROCESS_ENTER)

        hwsizer.Add(ttl_hw,  flag=wx.RIGHT, border=5)
        hwsizer.Add(self.val_hw,  flag=wx.RIGHT, border=5)

        ## Regions
        rgnsizer = wx.BoxSizer(wx.VERTICAL)

        ttl_rgn = wx.StaticText(self.panel, label='Number of regions')
        self.val_regions = wx.TextCtrl(self.panel,wx.TE_PROCESS_ENTER)

        rgnsizer.Add(ttl_rgn,  flag=wx.RIGHT, border=5)
        rgnsizer.Add(self.val_regions,  flag=wx.RIGHT, border=5)

        ## Gap threshold
        gpthrsizer = wx.BoxSizer(wx.VERTICAL)

        ttl_gpthr = wx.StaticText(self.panel, label='Gap threshold')

        self.val_gapthr = wx.TextCtrl(self.panel,wx.TE_PROCESS_ENTER)
        gpthrsizer.Add(ttl_gpthr,  flag=wx.RIGHT, border=5)
        gpthrsizer.Add(self.val_gapthr,  flag=wx.RIGHT, border=5)


        #####
        ## OKAY!
        oksizer = wx.BoxSizer(wx.HORIZONTAL)

        hlpBtn     = wx.Button(self.panel, wx.ID_HELP   )
        self.okBtn = wx.Button(self.panel, wx.ID_OK     , label='Find peaks')
        canBtn     = wx.Button(self.panel, wx.ID_CANCEL )

        hlpBtn.Bind(wx.EVT_BUTTON, lambda evt: wx.TipWindow(
            self, 'These values are specific to the built-in scipy function:'
            ' scipy.signal.find_peaks_cwt(vector, widths, wavelet=None,'
            ' max_distances=None, gap_thresh=None, min_length=None,'
            ' min_snr=1, noise_perc=10), where he number of regions defines the'
            ' width squence [widths = arange(int(len(x_axis)/regions))]'))

        oksizer.Add(hlpBtn,     flag=wx.RIGHT,  border=8)
        oksizer.Add(canBtn,     flag=wx.RIGHT, border=8)
        oksizer.Add(self.okBtn, flag=wx.RIGHT,  border=8)

        mainsizer.Add(fitsizer,   flag=wx.ALL, border=8)
        mainsizer.AddSpacer(10)
        mainsizer.Add(hwsizer,   flag=wx.ALL, border=8)
        mainsizer.AddSpacer(10)
        mainsizer.Add(rgnsizer,   flag=wx.ALL, border=8)
        mainsizer.AddSpacer(10)
        mainsizer.Add(gpthrsizer, flag=wx.ALL, border=5)
        mainsizer.AddSpacer(10)
        mainsizer.Add(oksizer,    flag=wx.ALL|wx.ALIGN_RIGHT, border=10)


        self.panel.SetSizer(mainsizer)

class Viewer1DXRD(wx.Panel):
    '''
    Panel for housing 1D XRD viewer
    '''
    label='Viewer'
    def __init__(self,parent,owner=None,_larch=None):

        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.owner = owner

        ## Default information
        self.plotlist     = []
        self.xlabel       = 'q (1/$\AA$)' #'q (A^-1)'
        self.ylabel       = 'Intensity (a.u.)'
        self.dlimit       = 7.5 # A -> 2th = 5 deg.; q = 0.8 1/A

        self.data_name    = []
        self.xy_data      = []
        self.xy_plot      = []
        self.xy_scale     = []
        self.idata        = []

        self.cif_name     = []
        self.cif_plot     = []
        self.cif_path     = []
        self.cif_scale    = []
        self.icif         = []

        self.Panel1DViewer()

##############################################
#### PANEL DEFINITIONS
    def Panel1DViewer(self):
        '''
        Frame for housing all 1D XRD viewer widgets
        '''
        leftside  = self.LeftSidePanel(self)
        rightside = self.RightSidePanel(self)

        panel1D = wx.BoxSizer(wx.HORIZONTAL)
        panel1D.Add(leftside,flag=wx.ALL,border=10)
        panel1D.Add(rightside,proportion=1,flag=wx.ALL,border=10)

        self.SetSizer(panel1D)

    def LeftSidePanel(self,panel):

        vbox = wx.BoxSizer(wx.VERTICAL)

        plttools = self.Toolbox(self)
        addbtns = self.AddPanel(self)
        dattools = self.DataBox(self)
        ciftools = self.CIFBox(self)

        vbox.Add(plttools,flag=wx.ALL,border=10)
        vbox.Add(addbtns,flag=wx.ALL,border=10)
        vbox.Add(dattools,flag=wx.ALL,border=10)
        vbox.Add(ciftools,flag=wx.ALL,border=10)
        return vbox

    def RightSidePanel(self,panel):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.plot1DXRD(panel)

#         settings = self.SettingsPanel(self)
        btnbox = self.QuickButtons(panel)

        vbox.Add(self.plot1D,proportion=1,flag=wx.ALL|wx.EXPAND,border = 10)
#         hbox.Add(settings,flag=wx.RIGHT,border=10)
        hbox.Add(btnbox,flag=wx.LEFT,border = 1)
        vbox.Add(hbox,flag=wx.ALL|wx.ALIGN_RIGHT,border = 10)
        return vbox


    def Toolbox(self,panel):
        '''
        Frame for visual toolbox
        '''

        tlbx = wx.StaticBox(self,label='PLOT TOOLBOX')
        vbox = wx.StaticBoxSizer(tlbx,wx.VERTICAL)

        ###########################
        ## X-Scale
        hbox_xaxis = wx.BoxSizer(wx.HORIZONTAL)
        ttl_xaxis = wx.StaticText(self, label='X-SCALE')
        xunits = ['q',u'2\u03B8','d']
        self.ch_xaxis = wx.Choice(self,choices=xunits)

        self.ch_xaxis.Bind(wx.EVT_CHOICE, self.check1Daxis)

        hbox_xaxis.Add(ttl_xaxis, flag=wx.RIGHT, border=8)
        hbox_xaxis.Add(self.ch_xaxis, flag=wx.EXPAND, border=8)
        vbox.Add(hbox_xaxis, flag=wx.ALL, border=10)

        ###########################
        ## Y-Scale
        hbox_yaxis = wx.BoxSizer(wx.HORIZONTAL)
        ttl_yaxis = wx.StaticText(self, label='Y-SCALE')
        yscales = ['linear','log']
        self.ch_yaxis = wx.Choice(self,choices=yscales)

        self.ch_yaxis.Bind(wx.EVT_CHOICE,   self.onLogLinear)

        hbox_yaxis.Add(ttl_yaxis, flag=wx.RIGHT, border=8)
        hbox_yaxis.Add(self.ch_yaxis, flag=wx.EXPAND, border=8)
        vbox.Add(hbox_yaxis, flag=wx.ALL, border=10)

        self.ch_xaxis.Disable()
        self.ch_yaxis.Disable()

        return vbox

    def DataBox(self,panel):
        '''
        Frame for data toolbox
        '''

        tlbx = wx.StaticBox(self,label='DATA TOOLBOX')
        vbox = wx.StaticBoxSizer(tlbx,wx.VERTICAL)


        ###########################
        ## DATA CHOICE

        self.ch_data = wx.Choice(self,choices=self.data_name)
        self.ch_data.Bind(wx.EVT_CHOICE,   self.onSELECT)
        vbox.Add(self.ch_data, flag=wx.BOTTOM|wx.TOP|wx.EXPAND, border=8)

        ###########################
        # Energy display
        self.ttl_energy = wx.StaticText(self, label=('Energy:'))
        vbox.Add(self.ttl_energy, flag=wx.RIGHT, border=8)

        ###########################
        ## Scale
        hbox_scl = wx.BoxSizer(wx.HORIZONTAL)
        ttl_scl = wx.StaticText(self, label='SCALE Y TO:')
        self.val_scale = wx.TextCtrl(self,style=wx.TE_PROCESS_ENTER)
        self.btn_reset = wx.Button(self,label='reset')

        self.val_scale.Bind(wx.EVT_TEXT_ENTER, self.normalize1Ddata)
        self.btn_reset.Bind(wx.EVT_BUTTON, self.reset1Dscale)

        hbox_scl.Add(ttl_scl, flag=wx.RIGHT, border=8)
        hbox_scl.Add(self.val_scale, flag=wx.RIGHT, border=8)
        hbox_scl.Add(self.btn_reset, flag=wx.RIGHT, border=8)

        vbox.Add(hbox_scl, flag=wx.BOTTOM|wx.TOP, border=8)

        ## Disable until data
        self.btn_reset.Disable()
        self.val_scale.Disable()
        
        return vbox   

    def CIFBox(self,panel):
        '''
        Frame for data toolbox
        '''

        tlbx = wx.StaticBox(self,label='CIF TOOLBOX')
        vbox = wx.StaticBoxSizer(tlbx,wx.VERTICAL)

        ###########################
        ## DATA CHOICE

        self.ch_cif = wx.Choice(self,choices=self.cif_name)
        self.ch_cif.Bind(wx.EVT_CHOICE,   self.selectCIF)
        vbox.Add(self.ch_cif, flag=wx.BOTTOM|wx.TOP|wx.EXPAND, border=8)

        ###########################
        ## Energy
        hbox_E = wx.BoxSizer(wx.HORIZONTAL)
        self.slctEorL = wx.Choice(self,choices=['Energy (keV)','Wavelength (A)'])
        self.val_cifE = wx.TextCtrl(self,style=wx.TE_PROCESS_ENTER)

        self.slctEorL.Bind(wx.EVT_CHOICE, self.onEorLSel)
        self.val_cifE.Bind(wx.EVT_TEXT_ENTER, self.onResetE)

        hbox_E.Add(self.slctEorL, flag=wx.RIGHT, border=8)
        hbox_E.Add(self.val_cifE, flag=wx.RIGHT, border=8)
        vbox.Add(hbox_E, flag=wx.BOTTOM|wx.TOP, border=8)

        ###########################
        ## Scale
        hbox_scl = wx.BoxSizer(wx.HORIZONTAL)
        ttl_scl = wx.StaticText(self, label='SCALE Y TO:')
        self.val_cifscale = wx.TextCtrl(self,style=wx.TE_PROCESS_ENTER)
        self.btn_cifreset = wx.Button(self,label='reset')

        self.val_cifscale.Bind(wx.EVT_TEXT_ENTER, partial(self.normalize1Ddata,cif=True))
        self.btn_cifreset.Bind(wx.EVT_BUTTON, self.resetCIFscale)

        hbox_scl.Add(ttl_scl, flag=wx.RIGHT, border=8)
        hbox_scl.Add(self.val_cifscale, flag=wx.RIGHT, border=8)
        hbox_scl.Add(self.btn_cifreset, flag=wx.RIGHT, border=8)

        vbox.Add(hbox_scl, flag=wx.BOTTOM|wx.TOP, border=8)

        ## Disable until data
        self.val_cifscale.Disable()
        self.btn_cifreset.Disable()
        self.slctEorL.Disable()
        self.val_cifE.Disable()

        return vbox

    def AddPanel(self,panel):

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        btn_data = wx.Button(panel,label='ADD NEW DATA SET')
        btn_data.Bind(wx.EVT_BUTTON, self.load_file)

        btn_cif = wx.Button(panel,label='ADD NEW CIF')
        btn_cif.Bind(wx.EVT_BUTTON, self.loadCIF)

        hbox.Add(btn_data, flag=wx.ALL, border=8)
        hbox.Add(btn_cif, flag=wx.ALL, border=8)
        return hbox

#     def SettingsPanel(self,panel):
# 
#         vbox = wx.BoxSizer(wx.VERTICAL)
#         self.ttl_energy = wx.StaticText(self, label=('Energy: %0.3f keV (%0.4f A)' % (0,0)))
#         vbox.Add(self.ttl_energy, flag=wx.EXPAND|wx.ALL, border=8)
# 
#         return vbox

    def QuickButtons(self,panel):
        buttonbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_img = wx.Button(panel,label='SAVE FIGURE')
        btn_calib = wx.Button(panel,label='PLOT SETTINGS')
        btn_integ = wx.Button(panel,label='RESET PLOT')

        btn_img.Bind(wx.EVT_BUTTON,   self.onSAVEfig)
        btn_calib.Bind(wx.EVT_BUTTON, self.onPLOTset)
        btn_integ.Bind(wx.EVT_BUTTON, self.onRESETplot)

        buttonbox.Add(btn_img, flag=wx.ALL, border=8)
        buttonbox.Add(btn_calib, flag=wx.ALL, border=8)
        buttonbox.Add(btn_integ, flag=wx.ALL, border=8)
        return buttonbox


##############################################
#### PLOTPANEL FUNCTIONS
    def plot1DXRD(self,panel):

        self.plot1D = PlotPanel(panel,size=(1000, 500),messenger=self.owner.write_message)
        self.plot1D.cursor_mode = 'zoom'
  
    def onSAVEfig(self,event=None):
        self.plot1D.save_figure()

    def onPLOTset(self,event=None):
        self.plot1D.configure()

    def onRESETplot(self,event=None):
        self.plot1D.reset_config()

    def onLogLinear(self, event=None):

        self.plot1D.axes.set_yscale(self.ch_yaxis.GetString(self.ch_yaxis.GetSelection()))
        self.rescale1Daxis(xaxis=False,yaxis=True)


##############################################
#### XRD PLOTTING FUNCTIONS

    def addCIFdata(self,newcif,path):

        cif_no = len(self.cif_name)
        
        ## Add 'raw' data to array
        self.cif_plot.append(newcif)
        self.cif_path.append(path)
        
        cifscale = np.max(self.cif_plot[-1][3])
        self.cif_scale.append(int(cifscale))

        if path is None:
            datalabel = 'cif %i' % len(self.cif_plot)
        else:
            datalabel = 'cif: %s' % os.path.split(path)[-1]
        self.cif_name.append(datalabel)

        ## Plot data (x,y)
        self.icif.append(len(self.plotlist))
        xi = self.ch_xaxis.GetSelection()

        cifarg = {'xlabel':self.xlabel,'ylabel':self.ylabel,'label':datalabel,'marker':'','markersize':0,'show_legend':True}
        self.plotlist.append(self.plot1D.oplot(self.cif_plot[-1][xi],self.cif_plot[-1][3],**cifarg))

        ## Use correct x-axis units
        self.check1Daxis()

        self.ch_cif.Set(self.cif_name)
        self.ch_cif.SetStringSelection(datalabel)

        ## Update toolbox panel, scale all cif to 1000
        self.val_cifscale.SetValue('%i' % self.cif_scale[cif_no])
        self.optionsON(data=False,cif=True)

    def readCIF(self,path,cifscale=CIFSCALE,verbose=False):
    
        energy = self.getE()
        
        maxq = 5
        for i,data in enumerate(self.xy_plot):
            if 1.05*np.max(data[0]) > maxq:
                maxq = 1.05*np.max(data[0])

        qall,Fall = calcCIFpeaks(path,energy,verbose=verbose,qmax=maxq)
        
        if len(Fall) > 0:
        
            Fall = Fall/np.max(Fall)*cifscale

            wavelength = lambda_from_E(energy)
            q    = qall
            twth = twth_from_q(q,wavelength)
            d    = d_from_q(q)
            I    = Fall
        else:
            print('No real structure factors found in range.')
            return
        
        return [q,twth,d,I]

    def onResetE(self,event=None):

        xi = self.ch_xaxis.GetSelection()
        for i,cif_no in enumerate(self.icif):
            self.cif_plot[i] = self.readCIF(self.cif_path[i],cifscale=self.cif_scale[i])
            self.plot1D.update_line(cif_no,np.array(self.cif_plot[i][xi]),
                                           np.array(self.cif_plot[i][3]))
        self.plot1D.canvas.draw()

    def onEorLSel(self,event=None):

        try:
            current = float(self.val_cifE.GetValue())
        except:
            return
        
        if self.slctEorL.GetSelection() == 1 and current > 5:
            new = '%0.4f' % lambda_from_E(current)
        elif self.slctEorL.GetSelection() == 0 and current < 5:
            new = '%0.4f' % E_from_lambda(current)
        else:
            return
        
        self.val_cifE.SetValue(new)

    def optionsON(self,data=True,cif=False):

        self.ch_xaxis.Enable()
        self.ch_yaxis.Enable()
        if data:
            self.val_scale.Enable()
            self.btn_reset.Enable()
        if cif:
            self.val_cifscale.Enable()
            self.btn_cifreset.Enable()
            self.slctEorL.Enable()
            self.val_cifE.Enable()

    def add1Ddata(self,data1dxrd):

        try:
            len(data1dxrd.I)
        except:
            return

        self.xy_data.append(data1dxrd)

        if self.xy_data[-1].label is None:
            self.xy_data[-1].label = 'dataset %i' % len(self.xy_data)
        else:
            self.xy_data[-1].label = 'data: %s' % self.xy_data[-1].label
        datalabel = self.xy_data[-1].label

        self.data_name.append(datalabel)
        self.idata.append(len(self.plotlist))
        self.xy_scale.append(np.max(self.xy_data[-1].I))

        self.xy_plot.append(self.xy_data[-1].all_data())

        ## Plot data (x,y)
        xi = self.ch_xaxis.GetSelection()
        datarg = {'xlabel':self.xlabel,'ylabel':self.ylabel,'label':datalabel,'marker':'',
                  'show_legend':True}
        x,y = self.xy_plot[-1][xi],self.xy_plot[-1][3]
        self.plotlist.append(self.plot1D.oplot(x,y,**datarg))

        ## Use correct x-axis units
        self.check1Daxis(yaxis=True)

        self.ch_data.Set(self.data_name)
        self.ch_data.SetStringSelection(datalabel)

        ## Update toolbox panel
        self.val_scale.SetValue('%i' % self.xy_scale[-1])
        self.optionsON(data=True,cif=False)
        self.ttl_energy.SetLabel('Energy: %0.3f keV (%0.4f A)' % (self.xy_data[-1].energy,
                                                             self.xy_data[-1].wavelength))

    def normalize1Ddata(self,event=None,cif=False):

        if cif:
            cif_no = self.ch_cif.GetSelection()
            y = self.cif_plot[cif_no][3]

            self.cif_scale[cif_no] = float(self.val_cifscale.GetValue())
            if self.cif_scale[cif_no] <= 0:
                self.cif_scale[cif_no] = CIFSCALE
                self.val_cifscale.SetValue('%i' % self.cif_scale[cif_no])
            self.cif_plot[cif_no][3] = y/np.max(y) * self.cif_scale[cif_no]
        else:
            plt_no = self.ch_data.GetSelection()
            y = self.xy_data[plt_no].I

            self.xy_scale[plt_no] = float(self.val_scale.GetValue())
            if self.xy_scale[plt_no] <= 0:
                self.xy_scale[plt_no] = np.max(y)
                self.val_scale.SetValue('%i' % self.xy_scale[plt_no])
            self.xy_plot[plt_no][3] = y/np.max(y) * self.xy_scale[plt_no]

        self.plot1D.unzoom_all()
        self.rescale1Daxis(xaxis=False,yaxis=True)

#     def remove1Ddata(self,event=None):
#         ## mkak 2016.11.10
#         try:
#             plt_no = self.ch_data.GetSelection()
#             name = self.data_name[plt_no]
#             question = 'Remove %s from XRD 1D viewer?' % name
#             rmdata = YesNo(self,question,caption='Overwrite warning')
#         except:
#             pass
#             
#         if rmdata:
#             print 'EVENTUALLY, button will remove plot: %s' % self.data_name[plt_no]
# 
#             ## removing name from list works... do not activate till rest is working
#             ## mkak 2016.11.10
#             self.data_name.remove(self.data_name[plt_no])
#             self.ch_data.Set(self.data_name)
#             
#             if len(self.data_name) < 1:
#                 print 'HERE: remove all buttons that need data to exist'

    def onSELECT(self,event=None):

        data_str = self.ch_data.GetString(self.ch_data.GetSelection())

        plt_no = self.ch_data.GetSelection()
        self.val_scale.SetValue('%i' % self.xy_scale[plt_no])
        
        self.ttl_energy.SetLabel('Energy: %0.3f keV (%0.4f A)' % (self.xy_data[plt_no].energy,
                                                                  self.xy_data[plt_no].wavelength))

    def selectCIF(self,event=None):

        cif_str = self.ch_cif.GetString(self.ch_cif.GetSelection())

        cif_no = self.ch_cif.GetSelection()
        self.val_cifscale.SetValue('%i' % self.cif_scale[cif_no])

    def check1Daxis(self,event=None,yaxis=False):

        self.plot1D.unzoom_all()

        ## d
        if self.ch_xaxis.GetSelection() == 2:
            self.xlabel = 'd ($\AA$)'
        ## 2theta
        elif self.ch_xaxis.GetSelection() == 1:
            self.xlabel = r'$2\Theta$'+r' $(^\circ)$'
        ## q
        else:
            self.xlabel = 'q (1/$\AA$)'

        self.rescale1Daxis(xaxis=True,yaxis=yaxis)

    def rescale1Daxis(self,xaxis=True,yaxis=False):

        xi = self.ch_xaxis.GetSelection()

        xmin,xmax,ymin,ymax = 0,10,0,10
        
        for i,plt_no in enumerate(self.icif):

            x = np.array(self.cif_plot[i][xi])
            y = np.array(self.cif_plot[i][3])

            if xmax < np.max(x): xmax = np.max(x)
            if xmin > np.min(x): xmin = np.min(x)
            if ymax < np.max(y): ymax = np.max(y)
            if ymin > np.min(y): ymin = np.min(y)

            self.plot1D.update_line(plt_no,x,y)
            
        for i,plt_no in enumerate(self.idata):
            x = np.array(self.xy_plot[i][xi])
            y = np.array(self.xy_plot[i][3])

            if xmax < np.max(x): xmax = np.max(x)
            if xmin > np.min(x): xmin = np.min(x)
            if ymax < np.max(y): ymax = np.max(y)
            if ymin > np.min(y): ymin = np.min(y)

            self.plot1D.update_line(plt_no,x,y)

        if xi == 2: xmax = min(xmax,self.dlimit)
        if xaxis: self.set_xview(xmin, xmax)
        if yaxis: self.set_yview(ymin, ymax)

    def reset1Dscale(self,event=None):

        plt_no = self.ch_data.GetSelection()
        xi = self.ch_xaxis.GetSelection()

        self.xy_plot[plt_no][3] = self.xy_data[plt_no].I
        self.plot1D.update_line(int(self.idata[plt_no]),
                                    np.array(self.xy_plot[plt_no][xi]),
                                    np.array(self.xy_plot[plt_no][3]))
        self.xy_scale[plt_no] = np.max(self.xy_data[plt_no].I)
        self.val_scale.SetValue('%i' % self.xy_scale[plt_no])

        self.plot1D.canvas.draw()
        self.plot1D.unzoom_all()
        self.rescale1Daxis(xaxis=xaxis,yaxis=xaxis)


    def resetCIFscale(self,event=None):

        cif_no = self.ch_cif.GetSelection()
        xi = self.ch_xaxis.GetSelection()

        self.cif_scale[cif_no] = CIFSCALE
        self.val_cifscale.SetValue('%i' % self.cif_scale[cif_no])
        self.normalize1Ddata(cif=True)
        
        self.plot1D.update_line(int(self.icif[cif_no]),
                                np.array(self.cif_plot[cif_no][xi]),
                                np.array(self.cif_plot[cif_no][3]))
        self.plot1D.canvas.draw()
        self.plot1D.unzoom_all()
        
        self.rescale1Daxis(xaxis=False,yaxis=True)
        
#         self.val_cifscale.SetValue('%i' % self.cif_scale[cif_no])

    def set_xview(self, x1, x2):

        if len(self.xy_plot) > 0:
            xydata = self.xy_plot
        elif len(self.cif_plot) > 0:
            xydata = self.cif_plot
        else:
            return
        xi = self.ch_xaxis.GetSelection()
        xmin,xmax = self.abs_limits(xydata,axis=xi)

        x1 = max(xmin,x1)
        x2 = min(xmax,x2)

        self.plot1D.axes.set_xlim((x1, x2))
        self.plot1D.set_xlabel(self.xlabel)
        self.plot1D.canvas.draw()

    def set_yview(self, y1, y2):

        if len(self.xy_plot) > 0:
            xydata = self.xy_plot
        elif len(self.cif_plot) > 0:
            xydata = self.cif_plot
        else:
            return
        ymin,ymax = self.abs_limits(xydata,axis=3)

        y1 = max(ymin,y1)
        y2 = min(ymax,y2)

        self.plot1D.axes.set_ylim((y1, y2))
        self.plot1D.set_ylabel(self.ylabel)
        self.plot1D.canvas.draw()

    def abs_limits(self,xydata,axis=0):

        mini, maxi = 0,1
        for axisi in xydata:
            mini = np.min(axisi[axis]) if np.min(axisi[axis]) < mini else mini
            maxi = np.max(axisi[axis]) if np.max(axisi[axis]) > maxi else maxi

        return mini,maxi

##############################################
#### XRD FILE OPENING/SAVING
    def load_file(self,event=None):

        loadXYfile(parent=self,xrdviewer=self)

    def saveXYFILE(self,event=None):
        wildcards = 'XRD data file (*.xy)|*.xy|All files (*.*)|*.*'
        dlg = wx.FileDialog(self, 'Save data as...',
                           defaultDir=os.getcwd(),
                           wildcard=wildcards,
                           style=wx.SAVE|wx.OVERWRITE_PROMPT)

        path, save = None, False
        if dlg.ShowModal() == wx.ID_OK:
            save = True
            path = dlg.GetPath().replace('\\', '/')
        dlg.Destroy()

        if save:
            ## mkak 2016.11.16
            print('Not yet capable of saving data. Function yet to be written.')

    def loadCIF(self,event=None):

        wildcards = 'XRD cifile (*.cif)|*.cif|All files (*.*)|*.*'
        dlg = wx.FileDialog(self, message='Choose CIF',
                           defaultDir=os.getcwd(),
                           wildcard=wildcards, style=wx.FD_OPEN)

        path, read = None, False
        if dlg.ShowModal() == wx.ID_OK:
            read = True
            path = dlg.GetPath().replace('\\', '/')
        dlg.Destroy()

        if read:
            newcif = self.readCIF(path,verbose=True)

            if newcif is not None:
                self.addCIFdata(newcif,path)
    
    def getE(self):
    
        try:
            energy = float(self.val_cifE.GetValue())
        except:
            energy = None
        
        if energy is None:
            try:
                plt_no = self.ch_data.GetSelection()
                energy = self.xy_data[plt_no].energy
            except:
                energy = 19.0
            self.val_cifE.SetValue('%0.3f' % energy)
            self.slctEorL.SetSelection(0)
        else:
            if self.slctEorL.GetSelection() == 0:
                energy = float(self.val_cifE.GetValue())
            else:
                energy = E_from_lambda(float(self.val_cifE.GetValue()))
        return energy


class RangeToolsPanel(wx.Panel):
    '''
    Panel for housing range tools in fitting panel
    '''
    label='Range'
    def __init__(self,parent,owner=None,_larch=None):

        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.owner = owner

        ## Default information


        rangepanel = self.RangeTools()

        panel1D = wx.BoxSizer(wx.HORIZONTAL)
        panel1D.Add(rangepanel,flag=wx.ALL,border=10)
        self.SetSizer(panel1D)

    def RangeTools(self):

        ###########################
        ## Range tools
        vbox_rng = wx.BoxSizer(wx.VERTICAL)
        hbox_xaxis = wx.BoxSizer(wx.HORIZONTAL)
        hbox_xmin = wx.BoxSizer(wx.HORIZONTAL)
        hbox_xmax = wx.BoxSizer(wx.HORIZONTAL)
        hbox_xset = wx.BoxSizer(wx.HORIZONTAL)

        ###########################
        ## X-Scale

        ttl_xaxis = wx.StaticText(self, label='X-SCALE')
        xunits = ['q',u'2\u03B8','d']
        self.ch_xaxis = wx.Choice(self,choices=xunits)
        self.ch_xaxis.Bind(wx.EVT_CHOICE, self.owner.onChangeXscale)
        hbox_xaxis.Add(ttl_xaxis, flag=wx.RIGHT, border=8)
        hbox_xaxis.Add(self.ch_xaxis, flag=wx.EXPAND, border=8)

        ###########################
        ## X-Range
        ttl_xmin = wx.StaticText(self, label='minimum')
        self.val_xmin = wx.TextCtrl(self,style=wx.TE_PROCESS_ENTER)
        self.unit_xmin = wx.StaticText(self, label=self.owner.xunit)
        self.val_xmin.Bind(wx.EVT_TEXT_ENTER, self.owner.onSetRange)
        hbox_xmin.Add(ttl_xmin, flag=wx.RIGHT, border=8)
        hbox_xmin.Add(self.val_xmin, flag=wx.RIGHT, border=8)
        hbox_xmin.Add(self.unit_xmin, flag=wx.RIGHT, border=8)

        ttl_xmax= wx.StaticText(self, label='maximum')
        self.val_xmax = wx.TextCtrl(self,style=wx.TE_PROCESS_ENTER)
        self.unit_xmax = wx.StaticText(self, label=self.owner.xunit)
        self.val_xmax.Bind(wx.EVT_TEXT_ENTER, self.owner.onSetRange)
        hbox_xmax.Add(ttl_xmax, flag=wx.RIGHT, border=8)
        hbox_xmax.Add(self.val_xmax, flag=wx.RIGHT, border=8)
        hbox_xmax.Add(self.unit_xmax, flag=wx.RIGHT, border=8)

        self.btn_rngreset = wx.Button(self,label='reset')
        self.btn_rngreset.Bind(wx.EVT_BUTTON, self.owner.onReset)

        hbox_xset.Add(self.btn_rngreset, flag=wx.RIGHT, border=8)

        vbox_rng.Add(hbox_xaxis, flag=wx.ALL, border=10)
        vbox_rng.Add(hbox_xmin, flag=wx.BOTTOM, border=8)
        vbox_rng.Add(hbox_xmax, flag=wx.BOTTOM, border=8)
        vbox_rng.Add(hbox_xset, flag=wx.BOTTOM|wx.ALIGN_RIGHT, border=8)

        ## until data is loaded:
        self.ch_xaxis.Disable()
        self.val_xmin.Disable()
        self.val_xmax.Disable()
        self.btn_rngreset.Disable()

        return vbox_rng


class BackgroundToolsPanel(wx.Panel):
    '''
    Panel for housing background tools in fitting panel
    '''
    label='Background'
    def __init__(self,parent,owner=None,_larch=None):

        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.owner = owner

        ## Default information



        bkgdpanel = self.BackgroundTools()

        panel1D = wx.BoxSizer(wx.HORIZONTAL)
        panel1D.Add(bkgdpanel,flag=wx.ALL,border=10)
        self.SetSizer(panel1D)

    def BackgroundTools(self):

        ###########################
        ## Background tools
        vbox_bkgd = wx.BoxSizer(wx.VERTICAL)
        hbox_bkgd = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_fbkgd = wx.Button(self,label='Fit')
        self.btn_fbkgd.Bind(wx.EVT_BUTTON,   self.owner.onFitBkgd)
        hbox_bkgd.Add(self.btn_fbkgd, flag=wx.RIGHT, border=8)

        self.btn_obkgd = wx.Button(self,label='Options')
        self.btn_obkgd.Bind(wx.EVT_BUTTON,   self.owner.background_options)
        hbox_bkgd.Add(self.btn_obkgd, flag=wx.RIGHT, border=8)

        self.btn_rbkgd = wx.Button(self,label='Remove')
        self.btn_rbkgd.Bind(wx.EVT_BUTTON,   self.owner.onRmvBkgd)

        vbox_bkgd.Add(hbox_bkgd, flag=wx.BOTTOM, border=8)
        vbox_bkgd.Add(self.btn_rbkgd, flag=wx.BOTTOM, border=8)

        self.ck_bkgd = wx.CheckBox(self,label='Subtract')
        self.ck_bkgd.Bind(wx.EVT_CHECKBOX,  self.owner.onSbtrctBkgd)
        vbox_bkgd.Add(self.ck_bkgd, flag=wx.BOTTOM, border=8)

        ## until data is loaded:
        self.btn_fbkgd.Disable()
        self.btn_obkgd.Disable()
        self.btn_rbkgd.Disable()
        self.ck_bkgd.Disable()

        return vbox_bkgd


class PeakToolsPanel(wx.Panel):
    '''
    Panel for housing background tools in fitting panel
    '''
    label='Peaks'
    def __init__(self,parent,owner=None,_larch=None):

        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.owner = owner

        ## Default information


        pkspanel = self.PeakTools()

        panel1D = wx.BoxSizer(wx.HORIZONTAL)
        panel1D.Add(pkspanel,flag=wx.ALL,border=10)
        self.SetSizer(panel1D)

    def PeakTools(self):

        ###########################
        ## Peak tools
        vbox_pks = wx.BoxSizer(wx.VERTICAL)
        hbox1_pks = wx.BoxSizer(wx.HORIZONTAL)
        hbox2_pks = wx.BoxSizer(wx.HORIZONTAL)
        hbox3_pks = wx.BoxSizer(wx.HORIZONTAL)
        hbox4_pks = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_fdpks = wx.Button(self,label='Find peaks')
        self.btn_fdpks.Bind(wx.EVT_BUTTON, partial(self.owner.onPeaks, filter=True))
        hbox1_pks.Add(self.btn_fdpks, flag=wx.RIGHT, border=8)

        self.btn_opks = wx.Button(self,label='Search options')
        self.btn_opks.Bind(wx.EVT_BUTTON, self.owner.peak_options)
        hbox1_pks.Add(self.btn_opks, flag=wx.RIGHT, border=8)


        intthrsizer = wx.BoxSizer(wx.VERTICAL)

        ttl_intthr = wx.StaticText(self, label='Intensity threshold')
        self.val_intthr = wx.TextCtrl(self,wx.TE_PROCESS_ENTER)
        self.val_intthr.Bind(wx.EVT_TEXT_ENTER, partial(self.owner.find_peaks, filter=True))
        hbox2_pks.Add(ttl_intthr,  flag=wx.RIGHT, border=8)
        hbox2_pks.Add(self.val_intthr,  flag=wx.RIGHT, border=8)

        self.owner.peaklistbox = EditableListBox(self, self.owner.select_peak,
                                        remove_action=self.owner.rm_sel_peaks,
                                        size=(250, -1) #, style =  wx.LB_MULTIPLE
                                        )

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.ttl_cntpks = wx.StaticText(self, label=('Total: 0 peaks'))
        hbox3_pks.Add(self.ttl_cntpks, flag=wx.EXPAND|wx.ALL, border=8)

        self.btn_addpks = wx.Button(self,label='Add last click')
        self.btn_addpks.Bind(wx.EVT_BUTTON, self.owner.onAddPks)
        hbox4_pks.Add(self.btn_addpks, flag=wx.RIGHT, border=8)

        self.btn_rmvpks = wx.Button(self,label='Remove all')
        self.btn_rmvpks.Bind(wx.EVT_BUTTON, self.owner.onRmvPksAll)
        hbox4_pks.Add(self.btn_rmvpks, flag=wx.RIGHT, border=8)

        vbox_pks.Add(hbox1_pks, flag=wx.BOTTOM, border=8)
        vbox_pks.Add(hbox2_pks, flag=wx.BOTTOM, border=8)
        vbox_pks.Add(self.owner.peaklistbox, flag=wx.BOTTOM, border=8)
        vbox_pks.Add(hbox3_pks, flag=wx.BOTTOM, border=8)
        vbox_pks.Add(hbox4_pks, flag=wx.BOTTOM, border=8)

        self.val_intthr.SetValue(str(self.owner.intthrsh))

        ## until data is loaded:
        self.btn_fdpks.Disable()
        self.btn_opks.Disable()
        self.val_intthr.Disable()
        self.btn_rmvpks.Disable()
        self.btn_addpks.Disable()

        return vbox_pks

class SearchPanel(wx.Panel):
    '''
    Panel for housing range tools in fitting panel
    '''
    label='Search'
    def __init__(self,parent,owner=None,_larch=None):

        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.owner = owner

        matchpanel = self.SearchMatchTools()
        refpanel = self.RefinementTools()

        panel1D = wx.BoxSizer(wx.VERTICAL)
        panel1D.Add(matchpanel,flag=wx.ALL,border=10)
        panel1D.Add(refpanel,flag=wx.ALL,border=10)
        self.SetSizer(panel1D)

    def SearchMatchTools(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        btn_db = wx.Button(self,label='Database info')
        btn_srch = wx.Button(self,label='Filter database')

        btn_db.Bind(wx.EVT_BUTTON,    self.owner.database_info)
        btn_srch.Bind(wx.EVT_BUTTON,  self.owner.filter_database)

        vbox.Add(btn_db,   flag=wx.BOTTOM, border=8)
        vbox.Add(btn_srch, flag=wx.BOTTOM, border=8)

        return vbox

    def RefinementTools(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_mtch = wx.Button(self,label='Search based on q')
        self.btn_mtch.Bind(wx.EVT_BUTTON,   self.owner.onMatch)

        ttl_gdnss = wx.StaticText(self, label='Goodness')
        self.owner.val_gdnss = wx.TextCtrl(self,style=wx.TE_PROCESS_ENTER)
        hbox.Add(ttl_gdnss, flag=wx.RIGHT, border=8)
        hbox.Add(self.owner.val_gdnss, flag=wx.RIGHT, border=8)

        self.owner.val_gdnss.SetValue('0.85')

        vbox.Add(self.btn_mtch, flag=wx.BOTTOM, border=8)
        vbox.Add(hbox,          flag=wx.BOTTOM, border=8)
        
        ## until peaks are available to search
        self.owner.val_gdnss.Disable()
        self.btn_mtch.Disable()

        return vbox



class InstrPanel(wx.Panel):
    '''
    Panel for housing background tools in fitting panel
    '''
    label='Width'
    def __init__(self,parent,owner=None,_larch=None):

        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.owner = owner

        instrpanel = self.InstrumentTools()

        panel1D = wx.BoxSizer(wx.HORIZONTAL)
        panel1D.Add(instrpanel,flag=wx.ALL,border=10)
        self.SetSizer(panel1D)

    def InstrumentTools(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox_inst = wx.BoxSizer(wx.HORIZONTAL)
        hbox_u    = wx.BoxSizer(wx.HORIZONTAL)
        hbox_v    = wx.BoxSizer(wx.HORIZONTAL)
        hbox_w    = wx.BoxSizer(wx.HORIZONTAL)
        hbox_size = wx.BoxSizer(wx.HORIZONTAL)
        hbox_D    = wx.BoxSizer(wx.HORIZONTAL)
        
        ttl_inst = wx.StaticText(self, label='Instrumental')
        ttl_u    = wx.StaticText(self, label='u')
        ttl_v    = wx.StaticText(self, label='v')
        ttl_w    = wx.StaticText(self, label='w')
        ttl_size = wx.StaticText(self, label='Size broadening')
        ttl_D    = wx.StaticText(self, label='D (A)')        

        self.val_u = wx.TextCtrl(self,style=wx.TE_PROCESS_ENTER)
        self.val_v = wx.TextCtrl(self,style=wx.TE_PROCESS_ENTER)
        self.val_w = wx.TextCtrl(self,style=wx.TE_PROCESS_ENTER)
        self.val_D = wx.TextCtrl(self,style=wx.TE_PROCESS_ENTER)

        self.btn_clrinst = wx.Button(self,label='Clear')
        self.btn_clrsize = wx.Button(self,label='Clear')

        self.val_u.Bind(wx.EVT_TEXT_ENTER, self.owner.onGetInstr)
        self.val_v.Bind(wx.EVT_TEXT_ENTER, self.owner.onGetInstr)
        self.val_w.Bind(wx.EVT_TEXT_ENTER, self.owner.onGetInstr)
        self.val_D.Bind(wx.EVT_TEXT_ENTER, self.owner.onGetSize)
        
        self.btn_clrinst.Bind(wx.EVT_BUTTON, self.owner.onClrInstr)
        self.btn_clrsize.Bind(wx.EVT_BUTTON, self.owner.onClrSize)

        hbox_inst.Add(ttl_inst,         flag=wx.RIGHT, border=8)
        hbox_inst.Add(self.btn_clrinst, flag=wx.RIGHT, border=8)

        hbox_u.Add(ttl_u,      flag=wx.RIGHT, border=8)
        hbox_u.Add(self.val_u, flag=wx.RIGHT, border=8)

        hbox_v.Add(ttl_v,      flag=wx.RIGHT, border=8)
        hbox_v.Add(self.val_v, flag=wx.RIGHT, border=8)
        
        hbox_w.Add(ttl_w,      flag=wx.RIGHT, border=8)
        hbox_w.Add(self.val_w, flag=wx.RIGHT, border=8)

        hbox_size.Add(ttl_size,         flag=wx.RIGHT, border=8)
        hbox_size.Add(self.btn_clrsize, flag=wx.RIGHT, border=8)
        
        hbox_D.Add(ttl_D,      flag=wx.RIGHT, border=8)
        hbox_D.Add(self.val_D, flag=wx.RIGHT, border=8)

        vbox.Add(hbox_inst, flag=wx.BOTTOM, border=8)
        vbox.Add(hbox_u,    flag=wx.BOTTOM, border=8)
        vbox.Add(hbox_v,    flag=wx.BOTTOM, border=8)
        vbox.Add(hbox_w,    flag=wx.BOTTOM, border=8)

        vbox.Add(hbox_size, flag=wx.BOTTOM, border=8)
        vbox.Add(hbox_D,    flag=wx.BOTTOM, border=8)

        self.val_u.SetValue('1.0')
        self.val_v.SetValue('1.0')
        self.val_w.SetValue('1.0')
        self.val_D.SetValue('')

        self.val_u.Disable()
        self.val_v.Disable()
        self.val_w.Disable()
        self.val_D.Disable()
        
        self.btn_clrinst.Disable()
        self.btn_clrsize.Disable()


        return vbox

class ResultsPanel(wx.Panel):
    '''
    Panel for housing background tools in fitting panel
    '''
    label='Results'
    def __init__(self,parent,owner=None,_larch=None):

        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.owner = owner

        ## Default information
        respanel = self.ResultsTools()

        panel1D = wx.BoxSizer(wx.HORIZONTAL)
        panel1D.Add(respanel,flag=wx.ALL,border=10)
        self.SetSizer(panel1D)

    def ResultsTools(self):

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.amcsdlistbox = EditableListBox(self, self.owner.showCIF, size=(200,150))

        self.btn_clr = wx.Button(self,label='Clear list')
        self.btn_clr.Bind(wx.EVT_BUTTON, self.owner.clearMATCHES)

        vbox.Add(self.amcsdlistbox,  flag=wx.BOTTOM, border=8)
        vbox.Add(self.btn_clr, flag=wx.RIGHT, border=8)
        
        self.btn_clr.Disable()

        return vbox

##### Pop-up from 2D XRD Viewer to calculate 1D pattern
class Calc1DPopup(wx.Dialog):

    def __init__(self,parent,xrd2Ddata):
        """Constructor"""
        dialog = wx.Dialog.__init__(self, parent, title='Calculate 1DXRD options',
                                    style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER,
                                    size = (210,410))
        self.parent = parent
        self.data2D = xrd2Ddata
        self.steps = 5001

        self.createPanel()
        self.setDefaults()

        ## Set defaults
        self.wedges.SetValue('1')

        ix,iy = self.panel.GetBestSize()
        self.SetSize((ix+20, iy+20))

    def createPanel(self):

        self.panel = wx.Panel(self)

        mainsizer = wx.BoxSizer(wx.VERTICAL)

        ## Azimutal wedges
        wedgesizer = wx.BoxSizer(wx.VERTICAL)

        ttl_wedges = wx.StaticText(self.panel, label='AZIMUTHAL WEDGES')

        wsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.wedges = wx.TextCtrl(self.panel,wx.TE_PROCESS_ENTER)
        spstyle = wx.SP_VERTICAL|wx.SP_ARROW_KEYS|wx.SP_WRAP
        self.wedge_arrow = wx.SpinButton(self.panel, style=spstyle)

        self.wedge_arrow.Bind(wx.EVT_SPIN, self.onSPIN)

        wsizer.Add(self.wedges,flag=wx.RIGHT,border=8)
        wsizer.Add(self.wedge_arrow,flag=wx.RIGHT,border=8)

        wedgesizer.Add(ttl_wedges,flag=wx.BOTTOM,border=8)
        wedgesizer.Add(wsizer,flag=wx.BOTTOM,border=8)


        ## Y-Range
        ysizer = wx.BoxSizer(wx.VERTICAL)

        ttl_yrange = wx.StaticText(self.panel, label='Y-RANGE (a.u.)')

        yminsizer = wx.BoxSizer(wx.HORIZONTAL)
        ttl_ymin = wx.StaticText(self.panel, label='minimum')
        self.ymin = wx.TextCtrl(self.panel,wx.TE_PROCESS_ENTER)
        yminsizer.Add(ttl_ymin,  flag=wx.RIGHT, border=5)
        yminsizer.Add(self.ymin,  flag=wx.RIGHT, border=5)

        ymaxsizer = wx.BoxSizer(wx.HORIZONTAL)
        ttl_ymax = wx.StaticText(self.panel, label='maximum')
        self.ymax = wx.TextCtrl(self.panel,wx.TE_PROCESS_ENTER)
        ymaxsizer.Add(ttl_ymax,  flag=wx.RIGHT, border=5)
        ymaxsizer.Add(self.ymax,  flag=wx.RIGHT, border=5)

        ysizer.Add(ttl_yrange,  flag=wx.BOTTOM, border=5)
        ysizer.Add(yminsizer,  flag=wx.BOTTOM, border=5)
        ysizer.Add(ymaxsizer,  flag=wx.BOTTOM, border=5)



        ## X-Range
        xsizer = wx.BoxSizer(wx.VERTICAL)

        ttl_xrange = wx.StaticText(self.panel, label='X-RANGE')

        self.xunitsizer = wx.BoxSizer(wx.HORIZONTAL)
        xunits = ['q','d',u'2\u03B8']
        ttl_xunit = wx.StaticText(self.panel, label='units')
        self.ch_xunit = wx.Choice(self.panel,choices=xunits)
        self.ch_xunit.Bind(wx.EVT_CHOICE,None)#self.onUnits)

        self.xunitsizer.Add(ttl_xunit, flag=wx.RIGHT, border=5)
        self.xunitsizer.Add(self.ch_xunit, flag=wx.RIGHT, border=5)

        xstepsizer = wx.BoxSizer(wx.HORIZONTAL)
        ttl_xstep = wx.StaticText(self.panel, label='steps')
        self.xstep = wx.TextCtrl(self.panel,wx.TE_PROCESS_ENTER)
        xstepsizer.Add(ttl_xstep,  flag=wx.RIGHT, border=5)
        xstepsizer.Add(self.xstep,  flag=wx.RIGHT, border=5)

        xminsizer = wx.BoxSizer(wx.HORIZONTAL)
        ttl_xmin = wx.StaticText(self.panel, label='minimum')
        self.xmin = wx.TextCtrl(self.panel,wx.TE_PROCESS_ENTER)
        xminsizer.Add(ttl_xmin,  flag=wx.RIGHT, border=5)
        xminsizer.Add(self.xmin,  flag=wx.RIGHT, border=5)

        xmaxsizer = wx.BoxSizer(wx.HORIZONTAL)
        ttl_xmax = wx.StaticText(self.panel, label='maximum')
        self.xmax = wx.TextCtrl(self.panel,wx.TE_PROCESS_ENTER)
        xmaxsizer.Add(ttl_xmax,  flag=wx.RIGHT, border=5)
        xmaxsizer.Add(self.xmax,  flag=wx.RIGHT, border=5)

        xsizer.Add(ttl_xrange,  flag=wx.BOTTOM, border=5)
        xsizer.Add(self.xunitsizer, flag=wx.TOP|wx.BOTTOM, border=5)
        xsizer.Add(xstepsizer, flag=wx.TOP|wx.BOTTOM, border=5)
        xsizer.Add(xminsizer,  flag=wx.TOP|wx.BOTTOM, border=5)
        xsizer.Add(xmaxsizer,  flag=wx.TOP|wx.BOTTOM, border=5)

        ## Plot/save

        self.ch_save = wx.CheckBox(self.panel, label = 'Save 1D?')
        self.ch_plot  = wx.CheckBox(self.panel, label = 'Plot 1D?')

        self.ch_save.Bind(wx.EVT_CHECKBOX, self.onCHECK)
        self.ch_plot.Bind(wx.EVT_CHECKBOX, self.onCHECK)

        minisizer = wx.BoxSizer(wx.VERTICAL)
        minisizer.Add(self.ch_save,  flag=wx.RIGHT, border=5)
        minisizer.Add(self.ch_plot,  flag=wx.RIGHT, border=5)

        #####
        ## OKAY!
        oksizer = wx.BoxSizer(wx.HORIZONTAL)
        #hlpBtn = wx.Button(self.panel, wx.ID_HELP    )
        self.okBtn  = wx.Button(self.panel, wx.ID_OK      )
        canBtn = wx.Button(self.panel, wx.ID_CANCEL  )

        #oksizer.Add(hlpBtn,flag=wx.RIGHT,  border=8)
        oksizer.Add(canBtn, flag=wx.RIGHT, border=8)
        oksizer.Add(self.okBtn,  flag=wx.RIGHT,  border=8)

        mainsizer.Add(wedgesizer, flag=wx.ALL, border=8)
        mainsizer.AddSpacer(15)
        mainsizer.Add(ysizer,     flag=wx.ALL, border=5)
        mainsizer.AddSpacer(15)
        mainsizer.Add(xsizer,     flag=wx.ALL, border=5)
        mainsizer.AddSpacer(15)
        mainsizer.Add(minisizer,  flag=wx.ALL, border=8)
        mainsizer.AddSpacer(15)
        mainsizer.Add(oksizer,    flag=wx.ALL|wx.ALIGN_RIGHT, border=10)


        self.panel.SetSizer(mainsizer)


    def onCHECK(self,event=None):
        if self.ch_save.GetValue() or self.ch_plot.GetValue():
           self.okBtn.Enable()
        else:
            self.okBtn.Disable()

    def setDefaults(self):

        self.ymin.SetValue(str(0))
        self.ymax.SetValue(str(10000))
        self.xstep.SetValue(str(5001))
        self.xmin.SetValue(str(0.1))
        self.xmax.SetValue(str(5.5))
        self.wedges.SetValue(str(1))

        self.wedge_arrow.SetRange(1, 10)
        self.wedge_arrow.SetValue(1)
        self.okBtn.Disable()

        self.ymin.Disable()
        self.ymax.Disable()
        self.xmin.Disable()
        self.xmax.Disable()
        self.wedges.Disable()
        self.wedge_arrow.Disable()
        self.ch_xunit.Disable()

    def onSPIN(self,event=None):
        self.wedges.SetValue(str(event.GetPosition()))
        print('WARNING: not currently using multiple wedges for calculations')

    def getValues(self):

        self.steps = int(self.xstep.GetValue())

class DatabaseInfoGUI(wx.Dialog):
    '''
    Displays number of entries in current database; allows for loading new database files
    mkak 2017.03.23
    '''

    #----------------------------------------------------------------------
    def __init__(self, parent):
        
        wx.Dialog.__init__(self, parent, title='Database Information')
        ## remember: size=(width,height)
        self.parent = parent
        self.panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        
        LEFT = wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL
        
        ## Database info
        self.txt_dbname = wx.StaticText(self.panel, label='Current file : ')
        self.txt_nocif  = wx.StaticText(self.panel, label='Number of cif entries : ')

        ## Database buttons
        db_sizer = wx.BoxSizer(wx.HORIZONTAL)
       
        dbBtn  = wx.Button(self.panel, label='Load new database' )
        rstBtn = wx.Button(self.panel, label='Reset to default database')
        
        dbBtn.Bind(wx.EVT_BUTTON, self.onNewFile  )
        rstBtn.Bind(wx.EVT_BUTTON, self.onResetFile  )
        
        db_sizer.Add(dbBtn,  flag=wx.RIGHT, border=10)
        db_sizer.Add(rstBtn, flag=wx.RIGHT, border=10)
        
        ## Okay, etc. buttons
        ok_sizer = wx.BoxSizer(wx.HORIZONTAL)

        hlpBtn = wx.Button(self.panel, wx.ID_HELP    )
        okBtn  = wx.Button(self.panel, wx.ID_OK,    label='Close')
        #canBtn = wx.Button(self.panel, wx.ID_CANCEL  )

        ok_sizer.Add(hlpBtn,      flag=wx.ALL, border=8)
        #ok_sizer.Add(canBtn,      flag=wx.ALL, border=8)
        ok_sizer.Add(okBtn,       flag=wx.ALL, border=8)
        
        sizer.Add(self.txt_dbname, flag=wx.ALL, border=10)
        sizer.Add(self.txt_nocif,  flag=wx.ALL, border=10)
        sizer.Add(db_sizer,        flag=wx.ALL, border=10)
        sizer.AddSpacer(5)
        sizer.Add(ok_sizer,        flag=wx.ALIGN_RIGHT|wx.ALL, border=10)
        self.panel.SetSizer(sizer)
        
        self.onUpdateText()
        
    def onNewFile(self,event=None):
    
        path = self.parent.open_database()
        self.onUpdateText()
        
    def onResetFile(self,event=None):
    
        self.parent.owner.openDB()
        self.onUpdateText()

    def onUpdateText(self,event=None):
        
        try:
            filename = self.parent.owner.cifdatabase.dbname
        except:
            return
        #filename = os.path.split(filename)[-1]
        nocif = self.parent.owner.cifdatabase.return_no_of_cif()

        self.txt_dbname.SetLabel('Current file : %s' % filename)
        self.txt_nocif.SetLabel('Number of cif entries : %i' % nocif)
        
        ix,iy = self.panel.GetBestSize()
        self.SetSize((ix+40, iy+40))
        self.Show()

#########################################################################
class XRDSearchGUI(wx.Dialog):

    def __init__(self, parent):
        
        wx.Dialog.__init__(self, parent, title='Crystal Structure Database Search')
        ## remember: size=(width,height)
        self.parent = parent
        self.panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        grd_sizer = wx.GridBagSizer( 5, 6)
        ok_sizer = wx.BoxSizer(wx.HORIZONTAL)

        LEFT = wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL

        ## Mineral search
        lbl_Mineral  = wx.StaticText(self.panel, label='Mineral name:' )
        self.minerals = self.parent.owner.cifdatabase.return_mineral_names()
        self.Mineral = wx.ComboBox(self.panel, choices=self.minerals, size=(270, -1), style=wx.TE_PROCESS_ENTER)

        ## Author search
        lbl_Author   = wx.StaticText(self.panel, label='Author(s):' )
        self.Author  = wx.TextCtrl(self.panel, size=(175, -1), style=wx.TE_PROCESS_ENTER)
        self.atrslct = wx.Button(self.panel, label='Select...')

        ## Chemistry search
        lbl_Chemistry  = wx.StaticText(self.panel, label='Chemistry:' )
        self.Chemistry = wx.TextCtrl(self.panel, size=(175, -1), style=wx.TE_PROCESS_ENTER)
        self.chmslct  = wx.Button(self.panel, label='Specify...')

        ## Cell parameter symmetry search
        lbl_Symmetry  = wx.StaticText(self.panel, label='Symmetry/unit cell:' )
        self.Symmetry = wx.TextCtrl(self.panel, size=(175, -1), style=wx.TE_PROCESS_ENTER)
        self.symslct  = wx.Button(self.panel, label='Specify...')

        ## Category search
        opts = wx.LB_EXTENDED|wx.LB_HSCROLL|wx.LB_NEEDED_SB|wx.LB_SORT
        lbl_Category  = wx.StaticText(self.panel, label='Category:', style=wx.TE_PROCESS_ENTER)
        self.Category = wx.ListBox(self.panel, style=opts, choices=CATEGORIES, size=(270, -1))
        
        ## General search
        lbl_Keyword  = wx.StaticText(self.panel, label='Keyword search:' )
        self.Keyword = wx.TextCtrl(self.panel, size=(270, -1), style=wx.TE_PROCESS_ENTER)

        ## Define buttons
        self.rstBtn = wx.Button(self.panel, label='Reset' )
        hlpBtn = wx.Button(self.panel, wx.ID_HELP    )
        okBtn  = wx.Button(self.panel, wx.ID_OK      )
        canBtn = wx.Button(self.panel, wx.ID_CANCEL  )

        ## Bind buttons for functionality
        self.rstBtn.Bind(wx.EVT_BUTTON,  self.onReset     )
        
        self.chmslct.Bind(wx.EVT_BUTTON, self.onChemistry )
        self.atrslct.Bind(wx.EVT_BUTTON, self.onAuthor    )
        self.symslct.Bind(wx.EVT_BUTTON, self.onSymmetry  )

        self.Chemistry.Bind(wx.EVT_TEXT_ENTER, self.entrChemistry )
        self.Mineral.Bind(wx.EVT_TEXT_ENTER,   self.entrMineral   )
        self.Author.Bind(wx.EVT_TEXT_ENTER,    self.entrAuthor    )
        self.Symmetry.Bind(wx.EVT_TEXT_ENTER,  self.entrSymmetry  )
        self.Category.Bind(wx.EVT_TEXT_ENTER,  self.entrCategory  )
        self.Keyword.Bind(wx.EVT_TEXT_ENTER,   self.entrKeyword   )

        grd_sizer.Add(lbl_Mineral,    pos = ( 1,1)               )
        grd_sizer.Add(self.Mineral,   pos = ( 1,2), span = (1,3) )

        grd_sizer.Add(lbl_Author,     pos = ( 2,1)               )
        grd_sizer.Add(self.Author,    pos = ( 2,2), span = (1,2) )
        grd_sizer.Add(self.atrslct,   pos = ( 2,4)               )

        grd_sizer.Add(lbl_Chemistry,  pos = ( 3,1)               )
        grd_sizer.Add(self.Chemistry, pos = ( 3,2), span = (1,2) )
        grd_sizer.Add(self.chmslct,   pos = ( 3,4)               )

        grd_sizer.Add(lbl_Symmetry,   pos = ( 4,1)               )
        grd_sizer.Add(self.Symmetry,  pos = ( 4,2), span = (1,2) )
        grd_sizer.Add(self.symslct,   pos = ( 4,4)               )

        grd_sizer.Add(lbl_Category,   pos = ( 5,1)               )
        grd_sizer.Add(self.Category,  pos = ( 5,2), span = (1,3) )

        grd_sizer.Add(lbl_Keyword,    pos = ( 6,1)               )
        grd_sizer.Add(self.Keyword,   pos = ( 6,2), span = (1,3) )
        
        ok_sizer.Add(hlpBtn,      flag=wx.ALL, border=8)
        ok_sizer.Add(canBtn,      flag=wx.ALL, border=8)
        ok_sizer.Add(self.rstBtn, flag=wx.ALL, border=8)
        ok_sizer.Add(okBtn,       flag=wx.ALL, border=8)        

        sizer.Add(grd_sizer)
        sizer.AddSpacer(15)
        sizer.Add(ok_sizer)
        self.panel.SetSizer(sizer)
        
        ix,iy = self.panel.GetBestSize()
        self.SetSize((ix+40, iy+40))

        self.Show()
        self.srch = SearchCIFdb()

#########################################################################

    def entrAuthor(self,event=None):
        key = 'authors'
        self.srch.read_parameter(self.Author.GetValue(),key=key)
        self.Author.SetValue(self.srch.print_parameter(key=key))
            
    def entrSymmetry(self,event=None):
        self.srch.read_geometry(str(self.Symmetry.GetValue()))
        self.Symmetry.SetValue(self.srch.print_geometry())

            
    def entrCategory(self,event=None):
        key = 'categories'
        self.srch.read_parameter(self.Category.GetValue(),key=key)
        self.Category.SetValue(self.srch.print_parameter(key=key))
             
    def entrKeyword(self,event=None):
        key = 'keywords'
        self.srch.read_parameter(self.Keyword.GetValue(),key=key)
        self.Keyword.SetValue(self.srch.print_parameter(key=key))


    def entrMineral(self,event=None):
        ## need to integrate with SearchCIFdb somehow...
        ## mkak 2017.03.01
        if event.GetString() not in self.minerals:
            self.minerals.insert(1,event.GetString())
            self.Mineral.Set(self.minerals)
            self.Mineral.SetSelection(1)
            self.srch.read_parameter(event.GetString(),key='mnrlname')

    def entrChemistry(self,event=None):
        self.srch.read_chemistry(self.Chemistry.GetValue())
        self.Chemistry.SetValue(self.srch.print_chemistry())


#########################################################################
    def onChemistry(self,event=None):
        dlg = PeriodicTableSearch(self,include=self.srch.elem_incl,
                                       exclude=self.srch.elem_excl)
        update = False
        if dlg.ShowModal() == wx.ID_OK:
            incl = dlg.element_include
            excl = dlg.element_exclude
            update = True
        dlg.Destroy()

        if update:
            self.srch.elem_incl = incl
            self.srch.elem_excl = excl
            self.Chemistry.SetValue(self.srch.print_chemistry())


    def onAuthor(self,event=None):
        authorlist = self.parent.owner.cifdatabase.return_author_names()
        dlg = AuthorListTable(self,authorlist,include=self.srch.authors)
   
        update = False
        if dlg.ShowModal() == wx.ID_OK:
            incl = []
            ii = dlg.authlist.GetSelections()
            for i in ii:
                incl +=[authorlist[i]]
            update = True
        dlg.Destroy()

        if update:
            self.srch.authors = incl
            self.Author.SetValue(self.srch.print_parameter(key='authors'))

    def onSymmetry(self,event=None):
        dlg = XRDSymmetrySearch(self,search=self.srch)
        update = False
        if dlg.ShowModal() == wx.ID_OK:
            vals = [dlg.min_a.GetValue(),     dlg.max_a.GetValue(),
                    dlg.min_b.GetValue(),     dlg.max_b.GetValue(),
                    dlg.min_c.GetValue(),     dlg.max_c.GetValue(),
                    dlg.min_alpha.GetValue(), dlg.max_alpha.GetValue(),
                    dlg.min_beta.GetValue(),  dlg.max_beta.GetValue(),
                    dlg.min_gamma.GetValue(), dlg.max_gamma.GetValue(),
                    dlg.SG.GetSelection()]
            update = True
        dlg.Destroy()
        
        if update:
            for i,val in enumerate(vals):
                if val == '' or val == 0:
                    vals[i] = None
                elif val != 12:
                    vals[i] = '%0.3f' % float(val)
               
            self.srch.a.min, self.srch.a.max, self.srch.a.unit = vals[0],vals[1],'A'
            self.srch.b.min, self.srch.b.max, self.srch.b.unit = vals[2],vals[3],'A'
            self.srch.c.min, self.srch.c.max, self.srch.c.unit = vals[4],vals[5],'A'

            self.srch.alpha.min, self.srch.alpha.max, self.srch.alpha.unit = vals[6],vals[7],'deg'
            self.srch.beta.min,  self.srch.beta.max,  self.srch.beta.unit  = vals[8],vals[9],'deg'
            self.srch.gamma.min, self.srch.gamma.max, self.srch.gamma.unit = vals[10],vals[11],'deg'
            
            self.srch.sg = vals[12]

            self.Symmetry.SetValue(self.srch.print_geometry())
        
    def onReset(self,event=None):
        self.minerals = self.parent.owner.cifdatabase.return_mineral_names()
        self.Mineral.Set(self.minerals)
        self.Mineral.Select(0)
        self.Author.Clear()
        self.Chemistry.Clear()
        self.Symmetry.Clear()
        for i,n in enumerate(CATEGORIES):
            self.Category.Deselect(i)
        self.Keyword.Clear()
        self.srch.__init__()

        
#########################################################################            
class PeriodicTableSearch(wx.Dialog):

    def __init__(self, parent,include=[],exclude=[]):
        
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title='Periodic Table of Elements')
        
        ## this eventually to file header - do not belong here but works.
        ## mkak 2017.02.16
        from larch_plugins.wx import PeriodicTablePanel
        
        panel = wx.Panel(self)
        self.ptable = PeriodicTablePanel(panel,title='Select Element(s)',
                                         onselect=self.onSelectElement,
                                         highlight=True)

        okBtn  = wx.Button(panel, wx.ID_OK,     label='Search selected'    )
        exBtn  = wx.Button(panel,               label='Exclude all others' )
        rstBtn = wx.Button(panel,               label='Clear'              )
        canBtn = wx.Button(panel, wx.ID_CANCEL                             )

        ## Bind buttons for functionality
        exBtn.Bind(wx.EVT_BUTTON,  self.onExclude )
        rstBtn.Bind(wx.EVT_BUTTON, self.onClear )

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(self.ptable, flag=wx.ALL, border=20)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(okBtn,  flag=wx.RIGHT, border=5)
        btn_sizer.Add(exBtn,  flag=wx.RIGHT, border=5)
        btn_sizer.Add(rstBtn, flag=wx.RIGHT, border=5)
        btn_sizer.Add(canBtn, flag=wx.RIGHT, border=5)
        
        main_sizer.Add(btn_sizer, flag=wx.ALL, border=20)

        pack(panel, main_sizer)
        
        ix,iy = panel.GetBestSize()
        self.SetSize((ix+20, iy+20))
        
        self.element_include = include
        self.element_exclude = exclude
        self.setDefault()
        
        
        self.cnt_elem = len(self.ptable.syms)

    def setDefault(self):
    
        for name in self.ptable.ctrls:
            if name in self.element_include:
                textwid = self.ptable.ctrls[name]
                textwid.SetForegroundColour(self.ptable.SEL_FG)
                textwid.SetBackgroundColour(self.ptable.SEL_BG)
            elif name in self.element_exclude:
                textwid = self.ptable.ctrls[name]
                textwid.SetForegroundColour(self.ptable.NEG_FG)
                textwid.SetBackgroundColour(self.ptable.NEG_BG)            
            else:
                textwid = self.ptable.ctrls[name]
                textwid.SetForegroundColour(self.ptable.REG_FG)
                textwid.SetBackgroundColour(self.ptable.REG_BG) 
        
        #self.ptable.onexclude(selected=self.element_include)
        
    def onSelectElement(self,elem=None, event=None):
    
        if elem not in self.element_include and elem not in self.element_exclude:
            self.element_include += [elem]    
        elif elem in self.element_include:
            self.element_exclude += [elem]
            i = self.element_include.index(elem)
            self.element_include.pop(i)
        elif elem in self.element_exclude:
            i = self.element_exclude.index(elem)
            self.element_exclude.pop(i)
        
    def onClear(self,event=None):
    
        self.element_include = []
        self.element_exclude = []
        self.ptable.onclear()

    def onExclude(self,event=None):
    
        for elem in self.ptable.syms:
            if elem not in self.element_include and elem not in self.element_exclude:
                self.element_exclude += [elem]
        self.ptable.onexclude(selected=self.element_include)

#########################################################################            
class AuthorListTable(wx.Dialog):
    """"""

    def __init__(self,parent,authorlist,include=[]):
    
        ## Constructor
        dialog = wx.Dialog.__init__(self, parent, title='Cell Parameters and Symmetry')
        ## remember: size=(width,height)
        self.panel = wx.Panel(self)
        self.list = authorlist
        self.include = include

        sizer = wx.BoxSizer(wx.VERTICAL)
        ok_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.authlist = wx.ListBox(self.panel, size=(170, 130), style= wx.LB_MULTIPLE)
        self.authlist.Set(self.list)

        ## Define buttons
        self.rstBtn = wx.Button(self.panel, label='Reset' )
        hlpBtn = wx.Button(self.panel, wx.ID_HELP   )
        okBtn  = wx.Button(self.panel, wx.ID_OK     )
        canBtn = wx.Button(self.panel, wx.ID_CANCEL )

        ## Bind buttons for functionality
        ok_sizer.Add(hlpBtn,      flag=wx.ALL, border=8)
        ok_sizer.Add(canBtn,      flag=wx.ALL, border=8)
        ok_sizer.Add(self.rstBtn, flag=wx.ALL, border=8)
        ok_sizer.Add(okBtn,       flag=wx.ALL, border=8)      
        

        sizer.Add(self.authlist)
        sizer.AddSpacer(15)
        sizer.Add(ok_sizer)
        self.panel.SetSizer(sizer)
        
        ix,iy = self.panel.GetBestSize()
        self.SetSize((ix+40, iy+40))

        self.Show()
        self.onSet()

    def onReset(self,event=None):
        
        for i,n in enumerate(self.list):
            self.authlist.Deselect(i)
        
        
    def onSet(self,event=None):
        
        for i,n in enumerate(self.list):
            if n in self.include:
                self.authlist.Select(i)
            else:
                self.authlist.Deselect(i)
            


#########################################################################            
class XRDSymmetrySearch(wx.Dialog):
    '''
    GUI interface for specifying lattice parameters 
    '''

    def __init__(self,parent,search=None):
    
        ## Constructor
        dialog = wx.Dialog.__init__(self, parent, title='Cell Parameters and Symmetry')
        ## remember: size=(width,height)
        self.panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        grd_sizer = wx.GridBagSizer( 5, 6)
        ok_sizer = wx.BoxSizer(wx.HORIZONTAL)

        LEFT = wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL

        ## Lattice parameters
        lbl_a = wx.StaticText(self.panel,    label='a (A)' )
        self.min_a = wx.TextCtrl(self.panel, size=(100, -1), style = wx.TE_PROCESS_ENTER )
        self.max_a = wx.TextCtrl(self.panel, size=(100, -1), style = wx.TE_PROCESS_ENTER )

        lbl_b = wx.StaticText(self.panel,    label='b (A)' )
        self.min_b = wx.TextCtrl(self.panel, size=(100, -1), style = wx.TE_PROCESS_ENTER )
        self.max_b = wx.TextCtrl(self.panel, size=(100, -1), style = wx.TE_PROCESS_ENTER )

        lbl_c = wx.StaticText(self.panel,    label='c (A)' )
        self.min_c = wx.TextCtrl(self.panel, size=(100, -1), style = wx.TE_PROCESS_ENTER )
        self.max_c = wx.TextCtrl(self.panel, size=(100, -1), style = wx.TE_PROCESS_ENTER )

        lbl_alpha = wx.StaticText(self.panel,    label='alpha (deg)' )
        self.min_alpha = wx.TextCtrl(self.panel, size=(100, -1), style = wx.TE_PROCESS_ENTER )
        self.max_alpha = wx.TextCtrl(self.panel, size=(100, -1), style = wx.TE_PROCESS_ENTER )

        lbl_beta = wx.StaticText(self.panel,    label='beta (deg)' )
        self.min_beta = wx.TextCtrl(self.panel, size=(100, -1), style = wx.TE_PROCESS_ENTER )
        self.max_beta = wx.TextCtrl(self.panel, size=(100, -1), style = wx.TE_PROCESS_ENTER )

        lbl_gamma = wx.StaticText(self.panel,    label='gamma (deg)' )
        self.min_gamma = wx.TextCtrl(self.panel, size=(100, -1), style = wx.TE_PROCESS_ENTER )
        self.max_gamma = wx.TextCtrl(self.panel, size=(100, -1), style = wx.TE_PROCESS_ENTER )

        SG_list = ['']
        for sgno in np.arange(230):
            SG_list.append('%3d' % (sgno+1))

        hm_notations = ['']
        ## Displays all space groups
        for spgrp in SPACEGROUPS:
            iuc_id,name = spgrp
            hm = '%s: %s' % (str(iuc_id),name)
            hm_notations += [hm]

        lbl_SG    = wx.StaticText(self.panel, label='Space group:')
        self.SG   = wx.Choice(self.panel,     choices=SG_list)
        self.HMsg = wx.Choice(self.panel,     choices=hm_notations)
        
        self.HMsg.Bind(wx.EVT_CHOICE, self.onSpaceGroup)

        ## Define buttons
        self.rstBtn = wx.Button(self.panel, label='Reset' )
        hlpBtn = wx.Button(self.panel, wx.ID_HELP   )
        okBtn  = wx.Button(self.panel, wx.ID_OK     )
        canBtn = wx.Button(self.panel, wx.ID_CANCEL )

        ## Bind buttons for functionality
        self.rstBtn.Bind(wx.EVT_BUTTON,  self.onReset     )

        grd_sizer.Add(lbl_a,          pos = ( 1,1) )
        grd_sizer.Add(self.min_a,     pos = ( 1,2) )
        grd_sizer.Add(self.max_a,     pos = ( 1,3) )

        grd_sizer.Add(lbl_b,          pos = ( 2,1) )
        grd_sizer.Add(self.min_b,     pos = ( 2,2) )
        grd_sizer.Add(self.max_b,     pos = ( 2,3) )

        grd_sizer.Add(lbl_c,          pos = ( 3,1) )
        grd_sizer.Add(self.min_c,     pos = ( 3,2) )
        grd_sizer.Add(self.max_c,     pos = ( 3,3) )

        grd_sizer.Add(lbl_alpha,      pos = ( 4,1) )
        grd_sizer.Add(self.min_alpha, pos = ( 4,2) )
        grd_sizer.Add(self.max_alpha, pos = ( 4,3) )

        grd_sizer.Add(lbl_beta,       pos = ( 5,1) )
        grd_sizer.Add(self.min_beta,  pos = ( 5,2) )
        grd_sizer.Add(self.max_beta,  pos = ( 5,3) )

        grd_sizer.Add(lbl_gamma,      pos = ( 6,1) )
        grd_sizer.Add(self.min_gamma, pos = ( 6,2) )
        grd_sizer.Add(self.max_gamma, pos = ( 6,3) )

        grd_sizer.Add(lbl_SG,         pos = ( 7,1) )
        grd_sizer.Add(self.SG,        pos = ( 7,2) )
        grd_sizer.Add(self.HMsg,      pos = ( 7,3) )
        
        self.min_a.Bind(wx.EVT_TEXT_ENTER, self.formatFloat)
        self.max_a.Bind(wx.EVT_TEXT_ENTER, self.formatFloat)
        self.min_b.Bind(wx.EVT_TEXT_ENTER, self.formatFloat)
        self.max_b.Bind(wx.EVT_TEXT_ENTER, self.formatFloat)
        self.min_c.Bind(wx.EVT_TEXT_ENTER, self.formatFloat)
        self.max_c.Bind(wx.EVT_TEXT_ENTER, self.formatFloat)
        self.min_alpha.Bind(wx.EVT_TEXT_ENTER, self.formatFloat)
        self.max_alpha.Bind(wx.EVT_TEXT_ENTER, self.formatFloat)
        self.min_beta.Bind(wx.EVT_TEXT_ENTER, self.formatFloat)
        self.max_beta.Bind(wx.EVT_TEXT_ENTER, self.formatFloat)
        self.min_gamma.Bind(wx.EVT_TEXT_ENTER, self.formatFloat)
        self.max_gamma.Bind(wx.EVT_TEXT_ENTER, self.formatFloat)
        
        ok_sizer.Add(hlpBtn,      flag=wx.ALL, border=8)
        ok_sizer.Add(canBtn,      flag=wx.ALL, border=8)
        ok_sizer.Add(self.rstBtn, flag=wx.ALL, border=8)
        ok_sizer.Add(okBtn,       flag=wx.ALL, border=8)      
        

        sizer.Add(grd_sizer)
        sizer.AddSpacer(15)
        sizer.Add(ok_sizer)
        self.panel.SetSizer(sizer)
        
        ix,iy = self.panel.GetBestSize()
        self.SetSize((ix+40, iy+40))

        self.Show()
        
        if search is not None:
            self.srch = search
            self.SetSearch()
        
#########################################################################
    def onReset(self,event=None):
        self.min_a.Clear()
        self.max_a.Clear()
        self.min_b.Clear()
        self.max_b.Clear()
        self.min_c.Clear()
        self.max_c.Clear()
        self.min_alpha.Clear()
        self.max_alpha.Clear()
        self.min_beta.Clear()
        self.max_beta.Clear()
        self.min_gamma.Clear()
        self.max_gamma.Clear()
        self.SG.SetSelection(0)
        self.HMsg.SetSelection(0)

    def SetSearch(self):

        if self.srch.a.min is not None:
            self.min_a.SetValue(self.srch.a.min)
        if self.srch.a.max is not None:
            self.max_a.SetValue(self.srch.a.max)
        if self.srch.b.min is not None:
            self.min_b.SetValue(self.srch.b.min)
        if self.srch.b.max is not None:
            self.max_b.SetValue(self.srch.b.max)
        if self.srch.c.min is not None:
            self.min_c.SetValue(self.srch.c.min)
        if self.srch.c.max is not None:
            self.max_c.SetValue(self.srch.c.max)
        if self.srch.alpha.min is not None:
            self.min_alpha.SetValue(self.srch.alpha.min)
        if self.srch.alpha.max is not None:
            self.max_alpha.SetValue(self.srch.alpha.max)
        if self.srch.beta.min is not None:
            self.min_beta.SetValue(self.srch.beta.min)
        if self.srch.beta.max is not None:
            self.max_beta.SetValue(self.srch.beta.max)
        if self.srch.gamma.min is not None:
            self.min_gamma.SetValue(self.srch.gamma.min)
        if self.srch.gamma.max is not None:
            self.max_gamma.SetValue(self.srch.gamma.max)
        if self.srch.sg is not None:
            self.SG.SetSelection(int(self.srch.sg))

    def onSpaceGroup(self,event=None):

        i = self.HMsg.GetSelection()
        if i > 0:
            iuc_id, name = SPACEGROUPS[i-1]
            self.SG.SetSelection(int(iuc_id))
        else:
            self.SG.SetSelection(0)
        
    def formatFloat(self,event):
        event.GetEventObject().SetValue('%0.3f' % float(event.GetString()))

# class CIFDatabaseList(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
#     def __init__(self, parent, ID, pos=wx.DefaultPosition,
#                  size=wx.DefaultSize, style=0):
#         wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
#         listmix.ListCtrlAutoWidthMixin.__init__(self)

# class DatabaseXRD(wx.Panel, listmix.ColumnSorterMixin):
#     """
#     This will be the second notebook tab
#     """
#     #----------------------------------------------------------------------
#     def __init__(self,parent,owner=None,_larch=None):
#         """"""
#         wx.Panel.__init__(self, parent)
# 
#         self.parent = parent
#         self.owner = owner
# 
#         self.createAndLayout()
# 
#     def createAndLayout(self):
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         self.list = CIFDatabaseList(self, wx.ID_ANY, style=wx.LC_REPORT
#                                  | wx.BORDER_NONE
#                                  | wx.LC_EDIT_LABELS
#                                  | wx.LC_SORT_ASCENDING)
#         sizer.Add(self.list, 1, wx.EXPAND)
# 
#         #self.database_info = self.createDATABASEarray()
#         ## removed so database not loaded upon start up
#         self.database_info = {}
# 
#         self.populateList()
# 
#         self.itemDataMap = self.database_info
#         listmix.ColumnSorterMixin.__init__(self, 4)
#         self.SetSizer(sizer)
#         self.SetAutoLayout(True)
# 
#     def populateList(self):
#         self.list.InsertColumn(0, 'AMSCD ID', wx.LIST_FORMAT_RIGHT)
#         self.list.InsertColumn(1, 'Name')
#         self.list.InsertColumn(2, 'Space Group')
#         self.list.InsertColumn(3, 'Elements')
#         self.list.InsertColumn(4, 'Authors')
# 
#         for key, data in self.database_info.items():
#             index = self.list.InsertStringItem(sys.maxint, data[0])
#             self.list.SetStringItem(index, 1, data[1])
#             self.list.SetStringItem(index, 2, data[2])
#             self.list.SetStringItem(index, 3, data[3])
#             self.list.SetStringItem(index, 4, data[4])
#             self.list.SetItemData(index, key)
# 
#         self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
#         self.list.SetColumnWidth(1, 100)
#         self.list.SetColumnWidth(2, wx.LIST_AUTOSIZE)
#         self.list.SetColumnWidth(3, wx.LIST_AUTOSIZE)
#         self.list.SetColumnWidth(4, wx.LIST_AUTOSIZE)
# 
# #
# #         # show how to select an item
# #         self.list.SetItemState(5, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
# #
# #         # show how to change the colour of a couple items
# #         item = self.list.GetItem(1)
# #         item.SetTextColour(wx.BLUE)
# #         self.list.SetItem(item)
# #         item = self.list.GetItem(4)
# #         item.SetTextColour(wx.RED)
# #         self.list.SetItem(item)
# 
#         self.currentItem = 0
# 
#     # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
#     def GetListCtrl(self):
#         return self.list

class diFFit1D(wx.App):
    def __init__(self):
        wx.App.__init__(self)

    def run(self):
        self.MainLoop()

    def createApp(self):
        frame = diFFit1DFrame()
        #frame = Viewer1DXRD()
        frame.Show()
        self.SetTopWindow(frame)

    def OnInit(self):
        self.createApp()
        return True

def registerLarchPlugin():
    return ('_diFFit', {})

class DebugViewer(diFFit1D):
    def __init__(self, **kws):
        diFFit1D.__init__(self, **kws)

    def OnInit(self):
        #self.Init()
        self.createApp()
        #self.ShowInspectionTool()
        return True

if __name__ == '__main__':
    diFFit1D().run()
