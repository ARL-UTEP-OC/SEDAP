'''
Created on Dec 18, 2015

@author: epadilla2
'''
# import xml.etree.ElementTree as ET

#!/usr/bin/env python

import sys
from Attributes import Attributes
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

class AttributesInterface:
    """This is an Hello World GTK application"""
    def on_window1_delete_event(self, *args):
        print "quit"
        gtk.main_quit()

    def __init__(self):
        #Set the Glade file
        self.gladefile = "AttributesInterface.glade"  
        self.builder = gtk.Builder() 
        self.builder.add_from_file(self.gladefile) 
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.window.set_title("Flow Description Attributes - New")
        self.window.set_default_size(450, 500)
        #self.window.set_resizable(False)
        self.window.set_border_width(10)
        self.window.show()
        
        self.treeView = self.builder.get_object("treeview")
        self.create_columns(self.treeView)
        self.treeView.connect("cursor-changed", self.on_cursor_changed)
        #add new elements
        self.addBtn = self.builder.get_object("addBtn")
        self.addBtn.connect("clicked", self.on_add_clicked)
        self.nameTxt = self.builder.get_object("nameTxt")
        self.valueTxt = self.builder.get_object("valueTxt")
        #new
        self.newBtn = self.builder.get_object("newBtn")
        self.newBtn.connect("clicked", self.on_new_clicked)
        self.newFlowBtn = self.builder.get_object("newFlowBtn")
        self.newFlowBtn.connect("clicked", self.on_new_flow_clicked)
        #set up file chooser dialog open attribute
        self.openBtn = self.builder.get_object("openBtn")
        self.openBtn.connect("clicked", self.on_open_attribute_clicked)
        #set up file chooser dialog open attribute
        self.openModelBtn = self.builder.get_object("openModelBtn")
        self.openModelBtn.connect("clicked", self.on_open_model_clicked)
        #set up file chooser dialog
        self.saveAsBtn = self.builder.get_object("saveAsBtn")
        self.saveAsBtn.connect("clicked", self.on_save_as_clicked)        
        #save
        self.saveBtn = self.builder.get_object("saveBtn")
        self.saveBtn.connect("clicked", self.on_save_clicked)
        self.saveBtn.set_sensitive(False)
        #delete attribute
        self.deleteAttributeBtn = self.builder.get_object("deleteAttributeBtn")
        self.deleteAttributeBtn.connect("clicked", self.on_delete_attr_clicked)
        self.deleteAttributeBtn.set_sensitive(False)
         #delete flow
        self.deleteFlowBtn = self.builder.get_object("deleteFlowBtn")
        self.deleteFlowBtn.connect("clicked", self.on_delete_flow_clicked)
        self.deleteFlowBtn.set_sensitive(True)
        #previous
        self.previousBtn = self.builder.get_object("previousBtn")
        self.previousBtn.connect("clicked", self.on_previous_clicked)
        self.previousBtn.set_sensitive(False)
        #next
        self.nextBtn = self.builder.get_object("nextBtn")
        self.nextBtn.connect("clicked", self.on_next_clicked)
        self.nextBtn.set_sensitive(False)
        # status label
        self.statusLabel = self.builder.get_object("statusLabel")
        self.statusLabel.set_markup("<b></b>")
        
        #evaluate model
        self.evaluateBtn = self.builder.get_object("evaluateBtn")
        self.evaluateBtn.connect("clicked", self.on_evaluate_clicked)
        self.evaluateBtn.set_sensitive(False)
        #save as model result
        self.saveAsModelEvaluationBtn = self.builder.get_object("saveAsModelEvaluationBtn")
        self.saveAsModelEvaluationBtn.connect("clicked", self.on_save_as_evaluate_clicked)
        self.saveAsModelEvaluationBtn.set_sensitive(False)
        
        # Dialogs
        # Dialog Open
        self.dialogOpen = self.builder.get_object("fileChooserDialogOpen")
        self.dialogOpen.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("XML Files")
        filter.add_pattern("*.xml")
        self.dialogOpen.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("Python Files")
        filter.add_pattern("*.py")
        self.dialogOpen.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("Weka Files")
        filter.add_pattern("*.arff")
        self.dialogOpen.add_filter(filter)
        # Dialog Save As
        self.dialogSaveAs = self.builder.get_object("fileChooserDialogSaveAs")
        self.dialogSaveAs.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("XML Files")
        filter.add_pattern("*.xml")
        self.dialogSaveAs.add_filter(filter)
        #list store & tree
        self.liststoreAttributes = gtk.ListStore(str,str)
        self.treeView.set_model(self.liststoreAttributes)
        self.textViewXml  = self.builder.get_object("textViewXml")
        self.textViewModel  = self.builder.get_object("textViewModel")
        self.textViewModelOutput  = self.builder.get_object("textViewModelOutput")
        #attributes
        self.attr = Attributes(self)
        self.new()

    def on_cursor_changed(self, widget, *args):
        self.deleteAttributeBtn.set_sensitive(True)
        
    def update_status_label(self):
          self.statusLabel.set_markup(" <b> Total: </b>" + str(len(self.flowAttributesList)) + "<b> Index: </b>" + str(self.currentFlowAttrIndex))
        
    def text_edited(self, widget, path, text):
        self.liststoreAttributes[path][1] = str(text)
        self.update_attributes()
        print  self.liststoreAttributes[path][1]
    
    def on_add_clicked(self, widget):
        name = self.nameTxt.get_text().strip()
        value = self.valueTxt.get_text().strip()
        if name:
            self.liststoreAttributes.append([name,value])
            self.update_attributes()
            self.nameTxt.set_text('')
            self.valueTxt.set_text('')
    
    def update_attributes(self):
        flowAttributes = dict()
        for row in self.liststoreAttributes:
            flowAttributes[str(row[0])] = str(row[1])
        self.flowAttributesList[self.currentFlowAttrIndex]=flowAttributes
    
    def on_new_clicked(self, widget):
        self.liststoreAttributes.clear()
        self.xmlPath = "None"
        self.saveBtn.set_sensitive(False)
        self.deleteAttributeBtn.set_sensitive(False)
        self.previousBtn.set_sensitive(True)
        self.nextBtn.set_sensitive(False)
        self.deleteFlowBtn.set_sensitive(True)
        self.window.set_title("Flow Description Attributes - New")
        self.new()
        #update status label
        self.update_status_label()
        
    def on_new_flow_clicked(self, widget):
        self.liststoreAttributes.clear()
        self.new_flow();
        #update status label
        self.update_status_label()

    def new(self):
        self.flowAttributesList = list()
        self.new_flow();
        
    def new_flow(self):
        flowAttributes = dict()
        self.flowAttributesList.append(flowAttributes)
        self.currentFlowAttrIndex = len(self.flowAttributesList)-1
       
    def on_open_attribute_clicked(self, widget):
        response = self.dialogOpen.run()
        
        if response == 1:
            filename = self.dialogOpen.get_filename()
            print("Open clicked")
            self.currentFlowAttrIndex = 0
            if ".xml"  in filename: 
                self.xmlPath = filename
                self.flowAttributesList = self.attr.readXML(self.xmlPath)
            if ".arff"  in filename: 
                self.arffPath = filename
                self.flowAttributesList = self.attr.readARFF(self.arffPath)
            # enabling next button
            if len(self.flowAttributesList) > 1:
                self.nextBtn.set_sensitive(True)
            # loading attributes
            self.load_flow()
            #enabling delete flow button
            if len(self.flowAttributesList) > 1:
                self.deleteFlowBtn.set_sensitive(True)
            
            if ".xml"  in filename:
                self.textViewXml.get_buffer().set_text(self.attr.toXMLString(self.flowAttributesList))
                self.window.set_title("Flow Description Attributes - " + self.xmlPath)
            self.saveBtn.set_sensitive(True)
        #update status label
        self.update_status_label()
            
        self.dialogOpen.hide()
        
    def on_open_model_clicked(self, widget):
        response = self.dialogOpen.run()
        
        if response == 1:
            print("Open clicked")
            self.modelPath = self.dialogOpen.get_filename()
            file = open(self.modelPath, 'r')
            modelStr = file.read()
            self.textViewModel.get_buffer().set_text(modelStr)
            #write to file
            text_file = open("Model.py", "w")
            text_file.write(modelStr)
            self.evaluateBtn.set_sensitive(True)
        
        self.dialogOpen.hide()
        
    def on_save_as_clicked(self, widget):
        response = self.dialogSaveAs.run()
        path = "None"
        if response == 1:
            print("Save As Clicked")
            path = self.dialogSaveAs.get_filename()
        
        if path != "None":
                self.xmlPath = path
                self.on_save_clicked(widget)
                self.saveBtn.set_sensitive(True)
                self.window.set_title("Flow Description Attributes - " + self.xmlPath)
        
        self.dialogSaveAs.hide()
        
    def on_save_clicked(self, widget):
        self.attr.writeXML(self.xmlPath, self.flowAttributesList)
        self.textViewXml.get_buffer().set_text(self.attr.toXMLString(self.flowAttributesList))
        
    def on_delete_attr_clicked(self, widget):
        selection  = self.treeView.get_selection()
        model, paths = selection.get_selected_rows()
        for path in paths:
            myIter = model.get_iter(path)
        model.remove(myIter)
        self.deleteAttributeBtn.set_sensitive(False)
        
    def on_delete_flow_clicked(self, widget):
        del self.flowAttributesList[self.currentFlowAttrIndex]
        if len(self.flowAttributesList) == 0:
            self.new_flow();
        self.currentFlowAttrIndex=0
        self.load_flow()
        self.previousBtn.set_sensitive(False)
        if len(self.flowAttributesList)>1:
            self.nextBtn.set_sensitive(True)
        else:
            self.nextBtn.set_sensitive(False)
            
        #update status label
        self.update_status_label()
        
    def on_previous_clicked(self, widget):
        print "previous"
        self.currentFlowAttrIndex-=1
        self.load_flow()
        if self.currentFlowAttrIndex == 0:
            self.previousBtn.set_sensitive(False)
        self.nextBtn.set_sensitive(True)
        
        #update status label
        self.update_status_label()
         
    def on_next_clicked(self, widget):
        print "next"
        self.currentFlowAttrIndex+=1
        self.load_flow()
        if (self.currentFlowAttrIndex+1) >= len(self.flowAttributesList):
            self.nextBtn.set_sensitive(False)
        self.previousBtn.set_sensitive(True)
        
        #update status label
        self.update_status_label()
        
    def load_flow(self):
        self.liststoreAttributes.clear()
        for key, value in self.flowAttributesList[self.currentFlowAttrIndex].iteritems():
                self.liststoreAttributes.append([key,str(value)])
        
    def on_evaluate_clicked(self, widget):
        mod = __import__('Model', fromlist=['Model'])
        ModelClass = getattr(mod, 'Model')
        instance = ModelClass()
        
        self.evaluationResults = list()
        for flowAttributes in self.flowAttributesList:
            results = instance.evaluate(flowAttributes)
            self.evaluationResults.append(results)
        self.textViewModelOutput.get_buffer().set_text(str('\n'.join(map(str, self.evaluationResults))))
        self.saveAsModelEvaluationBtn.set_sensitive(True)
        
    def on_save_as_evaluate_clicked(self, widget):
        response = self.dialogSaveAs.run()
        path = "None"
        if response == 1:
            print("Save as clicked")
            path = self.dialogSaveAs.get_filename()
        
        if path != "None":
                 self.attr.writeModelEvaluationXML(path,self.flowAttributesList,self.evaluationResults)

        self.dialogSaveAs.hide()
             
    def create_columns(self, treeView):
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Attribute", rendererText, text=0)
        column.set_sort_column_id(0)    
        treeView.append_column(column)
            
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Value", rendererText, text=1)
        column.set_sort_column_id(1)
        rendererText.set_property("editable", True)
        treeView.append_column(column)
        rendererText.connect("edited", self.text_edited)

if __name__ == "__main__":
    hwg = AttributesInterface()
    gtk.main()