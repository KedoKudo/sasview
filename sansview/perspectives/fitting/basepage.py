
import sys, os
import wx
import numpy
import time
import copy 
from sans.guiframe.utils import format_number,check_float
from sans.guicomm.events import StatusEvent   
import pagestate
from pagestate import PageState
(PageInfoEvent, EVT_PAGE_INFO)   = wx.lib.newevent.NewEvent()
_BOX_WIDTH = 80

class BasicPage(wx.ScrolledWindow):
    """
        This class provide general structure of  fitpanel page
    """
     ## Internal name for the AUI manager
    window_name = "Basic Page"
    ## Title to appear on top of the window
    window_caption = "Basic page "
    
    def __init__(self,parent, page_info):
        wx.ScrolledWindow.__init__(self, parent)
        ##window_name
        self.window_name = page_info.window_name
        ##window_caption
        self.window_caption = page_info.window_caption
        ## parent of the page
        self.parent = parent
        ## manager is the fitting plugin
        self.manager= page_info.manager
        ## owner of the page (fitting plugin)
        self.event_owner= page_info.event_owner
         ## current model
        self.model = page_info.model
        ## data
        self.data = page_info.data
        ## dictionary containing list of models
        self.model_list_box = page_info.model_list_box
        ## Data member to store the dispersion object created
        self._disp_obj_dict = {}
        ## selected parameters to apply dispersion
        self.disp_cb_dict ={}
        ## smearer object
        self.smearer = None
        ##list of model parameters. each item must have same length
        ## each item related to a given parameters
        ##[cb state, name, value, "+/-", error of fit, min, max , units]
        self.parameters=[]
        ## list of parameters to fit , must be like self.parameters
        self.param_toFit=[]
        ## list of looking like parameters but with non fittable parameters info
        self.fixed_param=[]
        ## list of looking like parameters but with  fittable parameters info
        self.fittable_param=[]
        ##list of dispersion parameters
        self.disp_list=[]
        ## list of orientation parameters
        self.orientation_params=[]
        self.orientation_params_disp=[]
        if self.model !=None:
            self.disp_list= self.model.getDispParamList()
        ##enable model 2D draw
        self.enable2D= False
        ## check that the fit range is correct to plot the model again
        self.fitrange= True
        ## Q range
        self.qmin_x= 0.0001
        self.qmax_x= 0.13
        self.num_points= 100
        ## Create memento to save the current state
        
        self.state= PageState(parent= self.parent,model=self.model, data=self.data)
        
        ## retrieve saved state
        self.number_saved_state= 0
        ## dictionary of saved state
        self.saved_states={}
        self.slicerpop = wx.Menu()
        ## Default locations
        self._default_save_location = os.getcwd()     
        ## save initial state on context menu
        self.onSave(event=None)
        self.Bind(wx.EVT_CONTEXT_MENU, self.onContextMenu)
        
        ## create the basic structure of the panel with empty sizer
        self.define_page_structure()
        ## drawing Initial dispersion parameters sizer 
        self.set_dispers_sizer()
        self._fill_save_sizer()
        ## layout
        self.set_layout()
       
       
    def onContextMenu(self, event): 
        """
            Retrieve the state selected state
        """
        # Skipping the save state functionality for release 0.9.0
        return
    
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        #TODO: why is the state menu called "slicerpop"?
        self.PopupMenu(self.slicerpop, pos) 
        
        
        
    def define_page_structure(self):
        """
            Create empty sizer for a panel
        """
        self.vbox  = wx.BoxSizer(wx.VERTICAL)
        self.sizer0 = wx.BoxSizer(wx.VERTICAL)
        self.sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer2 = wx.BoxSizer(wx.VERTICAL)
        self.sizer3 = wx.BoxSizer(wx.VERTICAL)
        self.sizer4 = wx.BoxSizer(wx.VERTICAL)
        self.sizer5 = wx.BoxSizer(wx.VERTICAL)
        self.sizer6 = wx.BoxSizer(wx.VERTICAL)
        
        self.sizer0.SetMinSize((375,-1))
        self.sizer1.SetMinSize((375,-1))
        self.sizer2.SetMinSize((375,-1))
        self.sizer3.SetMinSize((375,-1))
        self.sizer4.SetMinSize((375,-1))
        self.sizer5.SetMinSize((375,-1))
        self.sizer6.SetMinSize((375,-1))
        
        self.vbox.Add(self.sizer0)
        self.vbox.Add(self.sizer1)
        self.vbox.Add(self.sizer2)
        self.vbox.Add(self.sizer3)
        self.vbox.Add(self.sizer4)
        self.vbox.Add(self.sizer5)
        self.vbox.Add(self.sizer6)
        
        
    def set_layout(self):
        """
             layout
        """
        self.vbox.Layout()
        self.vbox.Fit(self) 
        self.SetSizer(self.vbox)
       
        self.set_scroll()
        self.Centre()
        
        
    def set_scroll(self):
        self.SetScrollbars(20,20,200,100)
        self.Layout()   
        self.SetAutoLayout(True)
         
         
    def set_owner(self,owner):
        """ 
            set owner of fitpage
            @param owner: the class responsible of plotting
        """
        self.event_owner = owner    
        self.state.event_owner = owner
  
    def set_manager(self, manager):
        """
             set panel manager
             @param manager: instance of plugin fitting
        """
        self.manager = manager  
        self.state.manager = manager
        
    def populate_box(self, dict):
        """
             Store list of model
             @param dict: dictionary containing list of models
        """
        self.model_list_box = dict
        self.state.model_list_box = self.model_list_box
            
    
        
    def set_dispers_sizer(self):
        """
            fill sizer containing dispersity info
        """
        self.sizer4.Clear(True)
        name="Polydispersity and Orientational Distribution"
        box_description= wx.StaticBox(self, -1,name)
        boxsizer1 = wx.StaticBoxSizer(box_description, wx.VERTICAL)
        #----------------------------------------------------
        self.disable_disp = wx.RadioButton(self, -1, 'Off', (10, 10), style=wx.RB_GROUP)
        self.enable_disp = wx.RadioButton(self, -1, 'On', (10, 30))
        ## saving the state of enable dispersity button
        self.state.enable_disp= self.enable_disp.GetValue()
        
        self.Bind(wx.EVT_RADIOBUTTON, self._set_dipers_Param, id=self.disable_disp.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self._set_dipers_Param, id=self.enable_disp.GetId())
        
        sizer_dispersion = wx.BoxSizer(wx.HORIZONTAL)
        sizer_dispersion.Add((20,20))
        name=""#Polydispersity and \nOrientational Distribution "
        sizer_dispersion.Add(wx.StaticText(self,-1,name))
        sizer_dispersion.Add(self.enable_disp )
        sizer_dispersion.Add((20,20))
        sizer_dispersion.Add(self.disable_disp )
        sizer_dispersion.Add((10,10))
        
        ## fill a sizer with the combobox to select dispersion type
        sizer_select_dispers = wx.BoxSizer(wx.HORIZONTAL)  
        self.model_disp = wx.StaticText(self, -1, 'Distribution Function ')
            
        import sans.models.dispersion_models 
        self.polydisp= sans.models.dispersion_models.models
        self.disp_box = wx.ComboBox(self, -1)
       
        for key in self.polydisp.iterkeys():
            name = str(key.__name__)
            if name=="ArrayDispersion":
                # Remove the option until the rest of the code is ready for it
                self.disp_box.Append("Select customized Model",key)
                
            else:
                self.disp_box.Append(name,key)
        self.disp_box.SetSelection(0) 
        
        wx.EVT_COMBOBOX(self.disp_box,-1, self._on_select_Disp) 
             
        sizer_select_dispers.Add((10,10)) 
        sizer_select_dispers.Add(self.model_disp) 
        sizer_select_dispers.Add(self.disp_box,0,
                wx.TOP|wx.BOTTOM|wx.LEFT|wx.EXPAND|wx.ADJUST_MINSIZE,border=5)
        #sizer_select_dispers.Add((10,10)) 
        self.model_disp.Hide()
        self.disp_box.Hide()
        
        boxsizer1.Add( sizer_dispersion,0,
                wx.TOP|wx.BOTTOM|wx.LEFT|wx.EXPAND|wx.ADJUST_MINSIZE,border=5)
        #boxsizer1.Add( (10,10) )
        boxsizer1.Add( sizer_select_dispers )
        self.sizer4_4 = wx.GridBagSizer(5,5)
        boxsizer1.Add( self.sizer4_4  )
        #-----------------------------------------------------
        self.sizer4.Add(boxsizer1,0, wx.EXPAND | wx.ALL, 10)
        self.sizer4_4.Layout()
        self.sizer4.Layout()
        self.Layout()
        self.SetScrollbars(20,20,200,100)
        self.Refresh()
        
    
    def select_disp_angle(self, event): 
        """
            Event for when a user select a parameter to average over.
            @param event: check box event
        """
        
        
        # Go through the list of dispersion check boxes to identify which one has changed 
        for p in self.disp_cb_dict:
            # Catch which one of the box was just checked or unchecked.
            if event.GetEventObject() == self.disp_cb_dict[p]:              

                
                if self.disp_cb_dict[p].GetValue() == True:
                    # The user wants this parameter to be averaged. 
                    # Pop up the file selection dialog.
                    path = self._selectDlg()
                    
                    # If nothing was selected, just return
                    if path is None:
                        self.disp_cb_dict[p].SetValue(False)
                        return
                    try:
                        self._default_save_location = os.path.dirname(path)
                    except:
                        pass 
                    try:
                        values,weights = self.read_file(path)
                    except:
                        msg="Could not read input file"
                        wx.PostEvent(self.parent.parent, StatusEvent(status= msg))
                        return
                    
                    # If any of the two arrays is empty, notify the user that we won't
                    # proceed 
                    if values is None or weights is None:
                        wx.PostEvent(self.parent.parent, StatusEvent(status=\
                            "The loaded %s distrubtion is corrupted or empty" % p))
                        return
                        
                    # Tell the user that we are about to apply the distribution
                    wx.PostEvent(self.parent.parent, StatusEvent(status=\
                            "Applying loaded %s distribution: %s" % (p, path)))  
                    
                    # Create the dispersion objects
                    from sans.models.dispersion_models import ArrayDispersion
                    disp_model = ArrayDispersion()
                    disp_model.set_weights(values, weights)
                    # Store the object to make it persist outside the scope of this method
                    #TODO: refactor model to clean this up?
                    self._disp_obj_dict[p] = disp_model
                    # Set the new model as the dispersion object for the selected parameter
                    self.model.set_dispersion(p, disp_model)
                    # Store a reference to the weights in the model object so that
                    # it's not lost when we use the model within another thread.
                    #TODO: total hack - fix this
                    if not hasattr(self.model, "_persistency_dict"):
                        self.model._persistency_dict = {}
                    self.model._persistency_dict[p] = [values, weights]
                else:
                    # The parameter was un-selected. Go back to Gaussian model (with 0 pts)
                    self._reset_dispersity()
                    
                ## Redraw the model
                self._draw_model()
        return
    
    
    def onResetModel(self, event):
        """
            Reset model state
        """
        ## post help message for the selected model 
        msg = self.slicerpop.GetHelpString(event.GetId())
        msg +=" reloaded"
        wx.PostEvent(self.parent.parent, StatusEvent(status = msg ))
        
        name= self.slicerpop.GetLabel(event.GetId())
        if name in self.saved_states.keys():
            previous_state = self.saved_states[name]
            self.reset_page(previous_state)
            
   
    def onSave(self, event):
        """
            save history of the data and model
        """
        # Skipping the save state functionality for release 0.9.0
        return
    
        if self.model==None:
            return 
        if hasattr(self,"enable_disp"):
            self.state.enable_disp = copy.deepcopy(self.enable_disp.GetValue())
        if hasattr(self, "disp_box"):
            self.state.disp_box = copy.deepcopy(self.disp_box.GetSelection())
        
        self.state.model = self.model.clone()
        new_state = self.state.clone()
        new_state.enable2D = copy.deepcopy(self.enable2D)
        ##Add model state on context menu
        self.number_saved_state += 1
        name= self.model.name+"[%g]"%self.number_saved_state 
        self.saved_states[name]= new_state
        
        ## Add item in the context menu
        
        year, month, day,hour,minute,second,tda,ty,tm_isdst= time.localtime()
        my_time= str(hour)+" : "+str(minute)+" : "+str(second)+" "
        date= str( month)+"|"+str(day)+"|"+str(year)
        msg=  "Model saved at %s on %s"%(my_time, date)
         ## post help message for the selected model 
        msg +=" Saved! right click on this page to retrieve this model"
        wx.PostEvent(self.parent.parent, StatusEvent(status = msg ))
        
        id = wx.NewId()
        self.slicerpop.Append(id,name,str(msg))
        wx.EVT_MENU(self, id, self.onResetModel)
        
    def onSetFocus(self, evt):
        """
            highlight the current textcrtl and hide the error text control shown 
            after fitting
        """
        
        if hasattr(self,"text2_3"):
            self.text2_3.Hide()
        if len(self.parameters)>0:
            for item in self.parameters:
                ## hide statictext +/-    
                if item[3]!=None:
                    item[3].Hide()
                ## hide textcrtl  for error after fit
                if item[4]!=None:
                    item[4].Clear()
                    item[4].Hide()
        if len(self.fittable_param)>0:
            for item in self.fittable_param:
                ## hide statictext +/-    
                if item[3]!=None:
                    item[3].Hide()
                ## hide textcrtl  for error after fit
                if item[4]!=None:
                    item[4].Clear()
                    item[4].Hide()
        self.Layout()
        # Get a handle to the TextCtrl
        widget = evt.GetEventObject()
        # Select the whole control, after this event resolves
        wx.CallAfter(widget.SetSelection, -1,-1)
        return
    
    
    def read_file(self, path):
        """
            Read two columns file
            @param path: the path to the file to read
        """
        try:
            if path==None:
                wx.PostEvent(self.parent.parent, StatusEvent(status=\
                            " Selected Distribution was not loaded: %s"%path))
                return None, None
            input_f = open(path, 'r')
            buff = input_f.read()
            lines = buff.split('\n')
            
            angles = []
            weights=[]
            for line in lines:
                toks = line.split()
                try:
                    angle = float(toks[0])
                    weight = float(toks[1])
                except:
                    # Skip non-data lines
                    pass
                angles.append(angle)
                weights.append(weight)
            return numpy.array(angles), numpy.array(weights)
        except:
            raise 
    
    
    def createMemento(self):
        """
            return the current state of the page
        """
        return self.state.clone()
    
    
    def save_current_state(self):
        """
            Store current state
        """
        if self.model!= None:
            self.state.model = self.model.clone()
        self.state.save_data(self.data)
        
        self.state.enable2D = copy.deepcopy(self.enable2D)
        
        if hasattr(self,"cb1"):
            self.state.cb1= self.cb1.GetValue()
           
        if hasattr(self,"enable_disp"):
            self.state.enable_disp= self.enable_disp.GetValue()
            self.state.disable_disp = self.disable_disp.GetValue()
            
        self.state.smearer = copy.deepcopy(self.smearer)
        if hasattr(self,"enable_smearer"):
            self.state.enable_smearer = copy.deepcopy(self.enable_smearer.GetValue())
            self.state.disable_smearer = copy.deepcopy(self.disable_smearer.GetValue())
            
            
        if hasattr(self,"disp_box"):
            self.state.disp_box = self.disp_box.GetCurrentSelection()
            if len(self.disp_cb_dict)>0:
                for k , v in self.disp_cb_dict.iteritems():
                    if v ==None :
                        self.state.disp_cb_dict[k]= v
                    else:
                        try:
                            self.state.disp_cb_dict[k]=v.GetValue()
                        except:
                            self.state.disp_cb_dict[k]= None
           
            if len(self._disp_obj_dict)>0:
                for k , v in self._disp_obj_dict.iteritems():
                    self.state._disp_obj_dict[k]= v
           
        self._save_plotting_range()
        
        self.state.orientation_params =[]
        self.state.orientation_params_disp =[]
        self.state.parameters =[]
        self.state.fittable_param =[]
        self.state.fixed_param =[]
        
        ## save checkbutton state and txtcrtl values
        self._copy_parameters_state(self.orientation_params,
                                     self.state.orientation_params)
        self._copy_parameters_state(self.orientation_params_disp,
                                     self.state.orientation_params_disp)
        self._copy_parameters_state(self.parameters, self.state.parameters)
       
        self._copy_parameters_state(self.fittable_param, self.state.fittable_param)
        self._copy_parameters_state(self.fixed_param, self.state.fixed_param)
        
        ## post state to fit panel
        event = PageInfoEvent(page = self)
        wx.PostEvent(self.parent, event)
    
    
    def reset_page_helper(self, state):
        """
            Use page_state and change the state of existing page
        """
        self.state = state.clone()
        self.model= self.state.model
        self.data = self.state.data
        self.smearer= self.state.smearer
        self.state.enable_smearer=state.enable_smearer
       
        ##model parameter values restore
        self._set_model_sizer_selection( self.model )
        self.set_model_param_sizer(self.model)
      
        self.enable2D= state.enable2D
        self.state.enable2D= state.enable2D
       
        if hasattr(self,"model_view"):
            if not self.enable2D:
                self.model_view.Enable()
            else:
                self.model_view.Disable()
            
        if hasattr(self, "cb1"):   
            self.cb1.SetValue(self.state.cb1)
        ## display dispersion info layer
        self.enable_disp.SetValue(self.state.enable_disp)
        self.disable_disp.SetValue(self.state.disable_disp)
        if hasattr(self, "disp_box"):
            self.disp_box.SetSelection(self.state.disp_box)  
            
            self.disp_cb_dict = {}
            for k,v in self.state.disp_cb_dict.iteritems():
                self.disp_cb_dict = copy.deepcopy(state.disp_cb_dict) 
                self.state.disp_cb_dict = copy.deepcopy(state.disp_cb_dict) 
                
            self._disp_obj_dict={}
            for k , v in self.state._disp_obj_dict.iteritems():
                self._disp_obj_dict[k]=v
      
        self._set_dipers_Param(event=None)
        ##plotting range restore    
        self._reset_plotting_range()
        ## smearing info  restore
        if hasattr(self,"enable_smearer"):
            ## set smearing value whether or not the data contain the smearing info
            self.enable_smearer.SetValue(state.enable_smearer)
            self.disable_smearer.SetValue(state.disable_smearer)
            self.compute_chisqr(smearer= self.smearer)  
            
       
        ## reset state of checkbox,textcrtl  and parameters value
        self._reset_parameters_state(self.orientation_params_disp,
                                     state.orientation_params_disp)
        self._reset_parameters_state(self.orientation_params,
                                     state.orientation_params)
        self._reset_parameters_state(self.parameters,state.parameters)
        self._reset_parameters_state(self.fittable_param,state.fittable_param)
        self._reset_parameters_state(self.fixed_param,state.fixed_param)
        self._onparamEnter_helper()
        ## reset context menu items
        self._reset_context_menu()
        ## draw the model with previous parameters value
        #self._draw_model()
        
   
   
         
        
    def _selectDlg(self):
        """
            open a dialog file to selected the customized dispersity 
        """
        import os
        dlg = wx.FileDialog(self, "Choose a weight file",
                                self._default_save_location , "", "*.*", wx.OPEN)
        path = None
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        return path
    
    
    def _reset_context_menu(self):
        """
            reset the context menu
        """
        for name, state in self.state.saved_states.iteritems():
            self.number_saved_state += 1
            ## Add item in the context menu
            id = wx.NewId()
            self.slicerpop.Append(id,name, 'Save model and state %g'%self.number_saved_state)
            wx.EVT_MENU(self, id, self.onResetModel)
    
    def _reset_plotting_range(self):
        """
            Reset the plotting range to a given state
        """
        
        #self.qmin.SetValue(format_number(self.state.qmin))
        #self.qmax.SetValue(format_number(self.state.qmax)) 
        self.qmin.SetValue(str(self.state.qmin))
        self.qmax.SetValue(str(self.state.qmax)) 
        if self.state.npts!=None:
            self.npts.SetValue(format_number(self.state.npts)) 
            self.num_points = float(self.state.npts)
            
        self.qmin_x = float(self.qmin.GetValue())
        self.qmax_x = float(self.qmax.GetValue())
        
        
    def _save_plotting_range(self ):
        """
            save the state of plotting range 
        """
        self.state.qmin = self.qmin_x
        self.state.qmax = self.qmax_x 
        if self.npts!=None:
            self.state.npts= self.num_points
            
            
    def _onparamEnter_helper(self):
        """
             check if values entered by the user are changed and valid to replot 
             model
             use : _check_value_enter 
        """
        if self.model !=None:
            ## save current state
            self.save_current_state()
            # Flag to register when a parameter has changed.
            is_modified = False
            is_modified =self._check_value_enter( self.fittable_param ,is_modified)
            is_modified =self._check_value_enter( self.fixed_param ,is_modified)
            is_modified =self._check_value_enter( self.parameters ,is_modified)        
           
            self.Layout()
            # Here we should check whether the boundaries have been modified.
            # If qmin and qmax have been modified, update qmin and qmax and 
            # set the is_modified flag to True
            from sans.guiframe.utils import check_value 
            if check_value( self.qmin, self.qmax):
                if float(self.qmin.GetValue()) != self.qmin_x:
                    self.qmin_x = float(self.qmin.GetValue())
                    is_modified = True
                if float(self.qmax.GetValue()) != self.qmax_x:
                    self.qmax_x = float(self.qmax.GetValue())
                    is_modified = True
                self.fitrange = True
            else:
                self.fitrange = False
            if self.npts != None:
                if check_float(self.npts):
                    if float(self.npts.GetValue()) !=  self.num_points:
                        self.num_points = float(self.npts.GetValue())
                        is_modified = True
                else:
                    msg= "Cannot Plot :Must enter a number!!!  "
                    wx.PostEvent(self.parent.parent, StatusEvent(status = msg ))
                    
            
            ## if any value is modify draw model with new value
            if is_modified:
                self._draw_model() 
                self.save_current_state()
                
                
    def _reset_parameters_state(self, listtorestore,statelist):
        """
            Reset the parameters at the given state
        """
        if len(statelist)==0 or  len(listtorestore)==0 :
            return
        if len(statelist)!=  len(listtorestore) :
            return
        for j in range(len(listtorestore)):
            item_page = listtorestore[j]
            item_page_info = statelist[j]
            ##change the state of the check box for simple parameters
            if item_page[0]!=None:
                item_page[0].SetValue(item_page_info[0])
    
            if item_page[2]!=None:
                item_page[2].SetValue(item_page_info[2])
                
            if item_page[3]!=None:
                ## show or hide text +/-
                if item_page_info[2]:
                    item_page[3].Show(True)
                else:
                    item_page[3].Hide()
            if item_page[4]!=None:
                ## show of hide the text crtl for fitting error
                if item_page_info[4][0]:
                    item_page[4].Show(True)
                    item_page[4].SetValue(item_page_info[4][1])
                else:
                    item_page[3].Hide()
            if item_page[5]!=None:
                ## show of hide the text crtl for fitting error
                if item_page_info[5][0]:
                    item_page[5].Show(True)
                    item_page[5].SetValue(item_page_info[4][1])
                else:
                    item_page[5].Hide()
                    
            if item_page[6]!=None:
                ## show of hide the text crtl for fitting error
                if item_page_info[6][0]:
                    item_page[6].Show(True)
                    item_page[6].SetValue(item_page_info[6][1])
                else:
                    item_page[6].Hide()
                            
                            
    def _copy_parameters_state(self, listtocopy, statelist):
        """
            copy the state of button 
            @param listtocopy: the list of check button to copy
            @param statelist: list of state object to store the current state
        """
        
        if len(listtocopy)==0:
            return
       
        for item in listtocopy:
            checkbox_state = None
            if item[0]!= None:
                checkbox_state= item[0].GetValue()
            parameter_name = item[1]
            parameter_value = None
            if item[2]!=None:
                parameter_value = item[2].GetValue()
            static_text = None
            if item[3]!=None:
                static_text = item[3].IsShown()
            error_value = None
            error_state = None
            if item[4]!= None:
                error_value = item[4].GetValue()
                error_state = item[4].IsShown()
                
            min_value = None
            min_state = None
            if item[5]!= None:
                min_value = item[5].GetValue()
                min_state = item[5].IsShown()
                
            max_value = None
            max_state = None
            if item[6]!= None:
                max_value = item[6].GetValue()
                max_state = item[6].IsShown()
               
            statelist.append([checkbox_state, parameter_name, parameter_value,
                              static_text ,[error_state,error_value],
                                [min_state,min_value],[max_state , max_value],None])
           
        
   
    def _set_model_sizer_selection(self, model):
        """
            Display the sizer according to the type of the current model
        """
        if hasattr(model ,"model2"):
            
            class_name= model.model2.__class__
            name= model.model2.name
            flag= name != "NoStructure"
            if flag and (class_name in self.model_list_box["Structure Factors"]):
                self.structurebox.Enable()
                items = self.structurebox.GetItems()
                self.sizer1.Layout()
                self.SetScrollbars(20,20,200,100)
                for i in range(len(items)):
                    if items[i]== str(name):
                        self.structurebox.SetSelection(i)
                        break
                    
        if hasattr(model ,"model1"):
            class_name = model.model1.__class__
            name = model.model1.name
            self.formfactorbox.Clear()
            
            for k, list in self.model_list_box.iteritems():
                if k in["P(Q)*S(Q)","Shapes" ] and class_name in self.model_list_box["Shapes"]:
                    self.shape_rbutton.SetValue(True)
                    ## fill the form factor list with new model
                    self._populate_box(self.formfactorbox,self.model_list_box["Shapes"])
                    items = self.formfactorbox.GetItems()
                    ## set comboxbox to the selected item
                    for i in range(len(items)):
                        if items[i]== str(name):
                            self.formfactorbox.SetSelection(i)
                            break
                    return
                elif k == "Shape-Independent":
                    self.shape_indep_rbutton.SetValue(True)
                elif k == "Structure Factors":
                     self.struct_rbutton.SetValue(True)
                else:
                    self.plugin_rbutton.SetValue(True)
               
                if class_name in list:
                    ## fill the form factor list with new model
                    self._populate_box(self.formfactorbox, list)
                    items = self.formfactorbox.GetItems()
                    ## set comboxbox to the selected item
                    for i in range(len(items)):
                        if items[i]== str(name):
                            self.formfactorbox.SetSelection(i)
                            break
                    break
        else:

            ## Select the model from the menu
            class_name = model.__class__
            name = model.name
            self.formfactorbox.Clear()
            items = self.formfactorbox.GetItems()
    
            for k, list in self.model_list_box.iteritems():          
                if k in["P(Q)*S(Q)","Shapes" ] and class_name in self.model_list_box["Shapes"]:
                    if class_name in self.model_list_box["P(Q)*S(Q)"]:
                        self.structurebox.Enable()
                        self.structurebox.SetSelection(0)
                    else:
                        self.structurebox.Disable()
                        self.structurebox.SetSelection(0)
                        
                    self.shape_rbutton.SetValue(True)
                    ## fill the form factor list with new model
                    self._populate_box(self.formfactorbox,self.model_list_box["Shapes"])
                    items = self.formfactorbox.GetItems()
                    ## set comboxbox to the selected item
                    for i in range(len(items)):
                        if items[i]== str(name):
                            self.formfactorbox.SetSelection(i)
                            break
                    return
                elif k == "Shape-Independent":
                    self.shape_indep_rbutton.SetValue(True)
                elif k == "Structure Factors":
                    self.struct_rbutton.SetValue(True)
                else:
                    self.plugin_rbutton.SetValue(True)
                if class_name in list:
                    self.structurebox.SetSelection(0)
                    self.structurebox.Disable()
                    ## fill the form factor list with new model
                    self._populate_box(self.formfactorbox, list)
                    items = self.formfactorbox.GetItems()
                    ## set comboxbox to the selected item
                    for i in range(len(items)):
                        if items[i]== str(name):
                            self.formfactorbox.SetSelection(i)
                            break
                    break
                    
        
    def _draw_model(self):
        """
            Method to draw or refresh a plotted model.
            The method will use the data member from the model page
            to build a call to the fitting perspective manager.
            
            [Note to coder: This way future changes will be done in only one place.] 
        """
        if self.model !=None:
            temp_smear=None
            if hasattr(self, "enable_smearer"):
                if self.enable_smearer.GetValue():
                    temp_smear= self.smearer
            self.manager.draw_model(self.model, data=self.data,
                                    smearer= temp_smear,
                                    qmin=float(self.qmin_x), qmax=float(self.qmax_x),
                                    qstep= float(self.num_points),
                                    enable2D=self.enable2D) 
        
    def _set_model_sizer(self, sizer, title="", object=None):
        """
            Use lists to fill a sizer for model info
        """
       
        sizer.Clear(True)
        box_description= wx.StaticBox(self, -1,str(title))
        boxsizer1 = wx.StaticBoxSizer(box_description, wx.VERTICAL)
        #--------------------------------------------------------
        self.shape_rbutton = wx.RadioButton(self, -1, 'Shapes', style=wx.RB_GROUP)
        self.shape_indep_rbutton = wx.RadioButton(self, -1, "Shape-Independent")
        self.struct_rbutton = wx.RadioButton(self, -1, "Structure Factor ")
        self.plugin_rbutton = wx.RadioButton(self, -1, "Customized Models")
        
        self.Bind( wx.EVT_RADIOBUTTON, self._show_combox,
                            id= self.shape_rbutton.GetId() ) 
        self.Bind( wx.EVT_RADIOBUTTON, self._show_combox,
                            id= self.shape_indep_rbutton.GetId() ) 
        self.Bind( wx.EVT_RADIOBUTTON, self._show_combox,
                            id= self.struct_rbutton.GetId() ) 
        self.Bind( wx.EVT_RADIOBUTTON, self._show_combox,
                            id= self.plugin_rbutton.GetId() )  
       
      
        sizer_radiobutton = wx.GridSizer(2, 2,5, 5)
        sizer_radiobutton.Add(self.shape_rbutton)
        sizer_radiobutton.Add(self.shape_indep_rbutton)
        sizer_radiobutton.Add(self.plugin_rbutton)
        sizer_radiobutton.Add(self.struct_rbutton)
        
        sizer_selection = wx.BoxSizer(wx.HORIZONTAL)
        
        self.text1 = wx.StaticText( self,-1,"" )
        self.text2 = wx.StaticText( self,-1,"P(Q)*S(Q)" )
        
        
        self.formfactorbox = wx.ComboBox(self, -1,style=wx.CB_READONLY)
        if self.model!=None:
            self.formfactorbox.SetValue(self.model.name)
           
            
        self.structurebox = wx.ComboBox(self, -1,style=wx.CB_READONLY)
        wx.EVT_COMBOBOX(self.formfactorbox,-1, self._on_select_model)
        wx.EVT_COMBOBOX(self.structurebox,-1, self._on_select_model)
        
        
        
        ## fill combox box
        if len(self.model_list_box)>0:
            self._populate_box( self.formfactorbox,self.model_list_box["Shapes"])
       
        if len(self.model_list_box)>0:
            self._populate_box( self.structurebox,
                                self.model_list_box["Structure Factors"])
            self.structurebox.Insert("None", 0,None)
            self.structurebox.SetSelection(0)
            self.structurebox.Disable()
 
            if self.model.__class__ in self.model_list_box["P(Q)*S(Q)"]:
                self.structurebox.Enable()
            
        
        ## check model type to show sizer
        if self.model !=None:
            self._set_model_sizer_selection( self.model )
        
        sizer_selection.Add(self.text1)
        sizer_selection.Add((5,5))
        sizer_selection.Add(self.formfactorbox)
        sizer_selection.Add((5,5))
        sizer_selection.Add(self.text2)
        sizer_selection.Add((5,5))
        sizer_selection.Add(self.structurebox)
        sizer_selection.Add((5,5))
        
        boxsizer1.Add( sizer_radiobutton )
        boxsizer1.Add( (20,20))
        boxsizer1.Add( sizer_selection )
        if object !=None:
            boxsizer1.Add( (-72,-72))
            boxsizer1.Add( object,  0, wx.ALIGN_RIGHT| wx.RIGHT, 10)
            boxsizer1.Add( (60,60))
        #--------------------------------------------------------
        sizer.Add(boxsizer1,0, wx.EXPAND | wx.ALL, 10)
        sizer.Layout()
        self.SetScrollbars(20,20,200,100)
        
        
    def _show_combox(self, event):
        """
            Show combox box associate with type of model selected
        """
        ## Don't want to populate combo box again if the event comes from check box
        if self.shape_rbutton.GetValue()and\
             event.GetEventObject()==self.shape_rbutton:
            ##fill the combobox with form factor list
            self.structurebox.SetSelection(0)
            self.structurebox.Disable()
            self.formfactorbox.Clear()
            self._populate_box( self.formfactorbox,self.model_list_box["Shapes"])
            
        if self.shape_indep_rbutton.GetValue()and\
             event.GetEventObject()==self.shape_indep_rbutton:
            ##fill the combobox with shape independent  factor list
            self.structurebox.SetSelection(0)
            self.structurebox.Disable()
            self.formfactorbox.Clear()
            self._populate_box( self.formfactorbox,
                                self.model_list_box["Shape-Independent"])
            
        if self.struct_rbutton.GetValue() and\
             event.GetEventObject()==self.struct_rbutton:
            ##fill the combobox with structure factor list
            self.structurebox.SetSelection(0)
            self.structurebox.Disable()
            self.formfactorbox.Clear()
            self._populate_box( self.formfactorbox,
                                self.model_list_box["Structure Factors"])
           
        if self.plugin_rbutton.GetValue()and\
             event.GetEventObject()==self.plugin_rbutton:
           
            ##fill the combobox with form factor list
            self.structurebox.Disable()
            self.formfactorbox.Clear()
            self._populate_box( self.formfactorbox,
                                self.model_list_box["Customized Models"])
        
        self._on_select_model(event=None)
        self.sizer4_4.Layout()
        self.sizer4.Layout()
        self.Layout()
        self.Refresh()
        self.SetScrollbars(20,20,200,100)
            
    def _populate_box(self, combobox, list):
        """
            fill combox box with dict item
            @param list: contains item to fill the combox
            item must model class
        """
        for models in list:
            model= models()
            name = model.__class__.__name__
            if models.__name__!="NoStructure":
                if hasattr(model, "name"):
                    name = model.name
                combobox.Append(name,models)
        try:

            combobox.SetSelection(0)
            
        except:
            pass
    
        return 0
   
   
    def _on_select_model_helper(self): 
        """
             call back for model selection
        """
        ## reset dictionary containing reference to dispersion
        self._disp_obj_dict = {}
        self.disp_cb_dict ={}
        f_id = self.formfactorbox.GetCurrentSelection()
        form_factor = self.formfactorbox.GetClientData( f_id )
        if not form_factor in  self.model_list_box["multiplication"]:
            self.structurebox.Disable()
            self.structurebox.SetSelection(0)
        else:
            self.structurebox.Enable()
           
        s_id = self.structurebox.GetCurrentSelection()
        struct_factor = self.structurebox.GetClientData( s_id )
       
        if  struct_factor !=None:
            from sans.models.MultiplicationModel import MultiplicationModel
            self.model= MultiplicationModel(form_factor(),struct_factor())
        else:
            self.model= form_factor()
        
        ## post state to fit panel
        self.state.model =self.model
        ## post state to fit panel
        event = PageInfoEvent(page = self)
        wx.PostEvent(self.parent, event)
        
        self.sizer4_4.Layout()
        self.sizer4.Layout()
        self.Layout()
        self.SetScrollbars(20,20,200,100)
        self.Refresh()
        
       
        
    def _onparamEnter(self,event):
        """ 
            when enter value on panel redraw model according to changed
        """
        tcrtl= event.GetEventObject()
        if check_float(tcrtl):
            self._onparamEnter_helper()
        else:
            msg= "Cannot Plot :Must enter a number!!!  "
            wx.PostEvent(self.parent.parent, StatusEvent(status = msg ))
            return 
        
        
    def _check_value_enter(self, list, modified):
        """
            @param list: model parameter and panel info
            each item of the list should be as follow:
            item=[cb state, name, value, "+/-", error of fit, min, max , units]
        """  
        is_modified =  modified
        if len(list)==0:
            return is_modified
        for item in list:
            try:
                name = str(item[1])
                if hasattr(self,"text2_3"):
                    self.text2_3.Hide()
                ## check model parameters range
                ## check minimun value
                param_min= None
                param_max= None
                if item[5]!= None:
                    if item[5].GetValue().lstrip().rstrip()!="":
                        param_min = float(item[5].GetValue())
                    
                ## check maximum value
                if item[6]!= None:
                    if item[6].GetValue().lstrip().rstrip()!="":
                        param_max = float(item[6].GetValue())
                        
                from sans.guiframe.utils import check_value
                if param_min != None and param_max !=None:
                    if not check_value(item[5], item[6]):
                        msg= "Wrong Fit range entered for parameter "
                        msg+= "name %s of model %s "%(name, self.model.name)
                        wx.PostEvent(self.parent.parent, StatusEvent(status = msg ))
                if name in self.model.details.keys():   
                    self.model.details[name][1:]= param_min,param_max
                
                ## hide statictext +/-    
                if item[3]!=None:
                    item[3].Hide()
                ## hide textcrtl  for error after fit
                if item[4]!=None:
                    item[4].Clear()
                    item[4].Hide()
                    
           
                value= float(item[2].GetValue())
                
                # If the value of the parameter has changed,
                # +update the model and set the is_modified flag
                if value != self.model.getParam(name):
                    self.model.setParam(name,value)
                    is_modified = True   
            
            except:
                msg= "Model Drawing  Error:wrong value entered : %s"% sys.exc_value
                wx.PostEvent(self.parent.parent, StatusEvent(status = msg ))
                return 
        
        return is_modified 
        
 
    def _set_dipers_Param(self, event):
        """
            Add more item to select user dispersity
        """
        self._reset_dispersity()
       
        if self.enable_disp.GetValue():
            self.model_disp.Show(True)
            self.disp_box.Show(True)
            ## layout for model containing no dispersity parameters
            if len(self.disp_list)==0:
                self._layout_sizer_noDipers()  
            else:
                ## set gaussian sizer 
                self._on_select_Disp(event=None)
        else:
            self.model_disp.Hide()
            self.disp_box.Hide()
            self.sizer4_4.Clear(True)
            self._reset_dispersity()
            
      
        ## post state to fit panel
        self.save_current_state()
            
          
            
        
    def _layout_sizer_noDipers(self):
        """
            Draw a sizer with no dispersity info
        """
        ix=0
        iy=1
        self.fittable_param=[]
        self.fixed_param=[]
        self.orientation_params_disp=[]
        
        self.model_disp.Hide()
        self.disp_box.Hide()
        self.sizer4_4.Clear(True)
        model_disp = wx.StaticText(self, -1, 'No PolyDispersity for this model')
        self.sizer4_4.Add(model_disp,( iy, ix),(1,1),  wx.LEFT|wx.EXPAND|wx.ADJUST_MINSIZE, 15)
        self.sizer4_4.Layout()
        self.sizer4.Layout()
        self.SetScrollbars(20,20,200,100)
      
            
    def _reset_dispersity(self):
        """
             put gaussian dispersity into current model
        """
        if len(self.param_toFit)>0:
            for item in self.fittable_param:
                if item in self.param_toFit:
                    self.param_toFit.remove(item)
            for item in self.orientation_params_disp:
                if item in self.param_toFit:
                    self.param_toFit.remove(item)
         
        self.fittable_param=[]
        self.fixed_param=[]
        self.orientation_params_disp=[]
       
        from sans.models.dispersion_models import GaussianDispersion
        if len(self.disp_cb_dict)==0:
            self.sizer4_4.Clear(True)
            self.sizer4_4.Layout()
            self.sizer4.Layout()
            self.Layout()
            self.Refresh()
            self.SetScrollbars(20,20,200,100)   
            return 
        
        for p in self.disp_cb_dict:
            # The parameter was un-selected. Go back to Gaussian model (with 0 pts)
            disp_model = GaussianDispersion()
            # Store the object to make it persist outside the scope of this method
            #TODO: refactor model to clean this up?
            self._disp_obj_dict[p] = disp_model
            # Set the new model as the dispersion object for the selected parameter
            self.model.set_dispersion(p, disp_model)
            # Redraw the model
            self._draw_model()
            
        self.sizer4_4.Layout()
        self.sizer4.Layout()
        self.Layout()
        self.SetScrollbars(20,20,200,100)    
        self.Refresh()
        
            
            
    def _on_select_Disp(self,event):
        """
             allow selecting different dispersion
             self.disp_list should change type later .now only gaussian
        """
        
        n = self.disp_box.GetCurrentSelection()
        dispersity= self.disp_box.GetClientData(n)
        name= dispersity.__name__
        if name == "GaussianDispersion":
            self._set_sizer_gaussian()
            
        if  name=="ArrayDispersion":
            self._set_sizer_arraydispersion()
            
        self.state.disp_box= n
        ## post state to fit panel
        event = PageInfoEvent(page = self)
        wx.PostEvent(self.parent, event)
        
        self.sizer4_4.Layout()
        self.sizer4.Layout()
        self.Layout()
        self.SetScrollbars(20,20,200,100)
        self.Refresh()
        
       
       
        
    def _set_sizer_arraydispersion(self):
        """
            draw sizer with array dispersity  parameters
        """
        if len(self.param_toFit)>0:
            for item in self.fittable_param:
                if item in self.param_toFit:
                    self.param_toFit.remove(item)
            for item in self.orientation_params_disp:
                if item in self.param_toFit:
                    self.param_toFit.remove(item)
        self.fittable_param=[]
        self.fixed_param=[]
        self.orientation_params_disp=[]
        self.sizer4_4.Clear(True) 
        ix=0
        iy=1     
        disp1 = wx.StaticText(self, -1, 'Array Dispersion')
        self.sizer4_4.Add(disp1,( iy, ix),(1,1),  wx.LEFT|wx.EXPAND|wx.ADJUST_MINSIZE, 15)
        
        # Look for model parameters to which we can apply an ArrayDispersion model
        # Add a check box for each parameter.
        self.disp_cb_dict = {}
        for p in self.model.dispersion.keys():
            ix+=1 
            self.disp_cb_dict[p] = wx.CheckBox(self, -1, p, (10, 10))
            
            wx.EVT_CHECKBOX(self, self.disp_cb_dict[p].GetId(), self.select_disp_angle)
            self.sizer4_4.Add(self.disp_cb_dict[p], (iy, ix), (1,1), wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        
        ix =0
        iy +=1 
        self.sizer4_4.Add((20,20),(iy,ix),(1,1), wx.LEFT|wx.EXPAND|wx.ADJUST_MINSIZE, 15)        
        self.sizer4_4.Layout()
        self.sizer4.Layout()
        self.SetScrollbars(20,20,200,100)
        
        
    def _set_range_sizer(self, title, object1=None,object=None):
        """
            Fill the 
        """
        self.sizer5.Clear(True)
        box_description= wx.StaticBox(self, -1,str(title))
        boxsizer1 = wx.StaticBoxSizer(box_description, wx.VERTICAL)
        #--------------------------------------------------------------
        self.qmin    = wx.TextCtrl(self, -1,size=(_BOX_WIDTH,20))
        #For qmin and qmax, do not use format_number.(If do, qmin and max could be different from what is in the data.)
        #self.qmin.SetValue(format_number(self.qmin_x))
        self.qmin.SetValue(str(self.qmin_x))
        self.qmin.SetToolTipString("Minimun value of Q in linear scale.")
        self.qmin.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)
        self.qmin.Bind(wx.EVT_KILL_FOCUS, self._onparamEnter)
        self.qmin.Bind(wx.EVT_TEXT_ENTER, self._onparamEnter)
     
        self.qmax    = wx.TextCtrl(self, -1,size=(_BOX_WIDTH,20))
        #For qmin and qmax, do not use format_number.(If do, qmin and max could be different from what is in the data.)
        #self.qmax.SetValue(format_number(self.qmax_x))
        self.qmax.SetValue(str(self.qmax_x))
        self.qmax.SetToolTipString("Maximum value of Q in linear scale.")
        self.qmax.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)
        self.qmax.Bind(wx.EVT_KILL_FOCUS, self._onparamEnter)
        self.qmax.Bind(wx.EVT_TEXT_ENTER, self._onparamEnter)
     
        sizer_horizontal=wx.BoxSizer(wx.HORIZONTAL)
        sizer= wx.GridSizer(3, 3,5, 5)
        
        sizer.Add((5,5))
        sizer.Add(wx.StaticText(self, -1, 'Min'))
        sizer.Add(wx.StaticText(self, -1, 'Max'))
        sizer.Add(wx.StaticText(self, -1, 'Q range'))
             
        sizer.Add(self.qmin)
        sizer.Add(self.qmax)
        sizer_horizontal.Add(sizer)
        if object!=None:
            sizer_horizontal.Add(object)
        
        if object1!=None:
           boxsizer1.Add(object1) 
           boxsizer1.Add((10,10))
        boxsizer1.Add(sizer_horizontal)
        ## save state
        self.save_current_state()
        #----------------------------------------------------------------
        self.sizer5.Add(boxsizer1,0, wx.EXPAND | wx.ALL, 10)
        self.sizer5.Layout()
        self.Layout()
        self.SetScrollbars(20,20,200,100)
    
    
    def _fill_save_sizer(self):
        """
            Draw the layout for saving option
        """
        # Skipping save state functionality for release 0.9.0
        return
    
        self.sizer6.Clear(True)
        box_description= wx.StaticBox(self, -1,"Save Status")
        boxsizer1 = wx.StaticBoxSizer(box_description, wx.VERTICAL)
        sizer_save = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btSave_title = wx.StaticText(self, -1, 'Save the current panel status')
        self.btSave = wx.Button(self,wx.NewId(),'Save')
        self.btSave.Bind(wx.EVT_BUTTON, self.onSave,id= self.btSave.GetId())
        self.btSave.SetToolTipString("Save current panel status")
        
        sizer_save.Add(self.btSave_title)  
        sizer_save.Add((20,20),0, wx.LEFT|wx.RIGHT|wx.EXPAND,45)  
             
        sizer_save.Add(self.btSave)     
        
        boxsizer1.Add(sizer_save)
        self.sizer6.Add(boxsizer1,0, wx.EXPAND | wx.ALL, 10)
        self.sizer6.Layout()
        self.SetScrollbars(20,20,200,100)
        
        
                