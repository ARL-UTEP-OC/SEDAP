'''
Created on Dec 18, 2015

@author: epadilla2
'''
# import xml.etree.ElementTree as ET

#!/usr/bin/env python

import sys
from AttributeConverter import AttributeConverter
from RuleConverter import RuleConverter
from RouteConverter import RouteConverter
from ModelEvaluator import ModelEvaluator
from PConverter import PConverter

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
        
        # Routes
        self.openRoutesBtn = self.builder.get_object("openRoutesBtn")
        self.openRoutesBtn.connect("clicked", self.on_open_routes_clicked)
        self.convertRoutesBtn = self.builder.get_object("convertRoutesBtn")
        self.convertRoutesBtn.connect("clicked", self.on_convert_routes_clicked)
        self.saveAsConvertedRoutesBtn = self.builder.get_object("saveAsConvertedRoutesBtn")
        self.saveAsConvertedRoutesBtn.connect("clicked", self.on_save_as_conv_routes_clicked)
        # add new elements
        self.addBtn = self.builder.get_object("addBtn")
        self.addBtn.connect("clicked", self.on_add_clicked)
        self.nameTxt = self.builder.get_object("nameTxt")
        self.valueTxt = self.builder.get_object("valueTxt")
        # new
        self.newBtn = self.builder.get_object("newBtn")
        self.newBtn.connect("clicked", self.on_new_clicked)
        self.newFlowBtn = self.builder.get_object("newFlowBtn")
        self.newFlowBtn.connect("clicked", self.on_new_flow_clicked)
        # set up file chooser dialog open attribute
        self.openBtn = self.builder.get_object("openBtn")
        self.openBtn.connect("clicked", self.on_open_attribute_clicked)
        # set up file chooser dialog open attribute
        self.openModelBtn = self.builder.get_object("openModelBtn")
        self.openModelBtn.connect("clicked", self.on_open_model_clicked)
        # set up file chooser dialog
        self.saveAsBtn = self.builder.get_object("saveAsBtn")
        self.saveAsBtn.connect("clicked", self.on_save_as_clicked)        
        # save
        self.saveBtn = self.builder.get_object("saveBtn")
        self.saveBtn.connect("clicked", self.on_save_clicked)
        self.saveBtn.set_sensitive(False)
        # delete attribute
        self.deleteAttributeBtn = self.builder.get_object("deleteAttributeBtn")
        self.deleteAttributeBtn.connect("clicked", self.on_delete_attr_clicked)
        self.deleteAttributeBtn.set_sensitive(False)
        # delete flow
        self.deleteFlowBtn = self.builder.get_object("deleteFlowBtn")
        self.deleteFlowBtn.connect("clicked", self.on_delete_flow_clicked)
        self.deleteFlowBtn.set_sensitive(True)
        # previous
        self.previousBtn = self.builder.get_object("previousBtn")
        self.previousBtn.connect("clicked", self.on_previous_clicked)
        self.previousBtn.set_sensitive(False)
        # next
        self.nextBtn = self.builder.get_object("nextBtn")
        self.nextBtn.connect("clicked", self.on_next_clicked)
        self.nextBtn.set_sensitive(False)
        # status label
        self.statusLabel = self.builder.get_object("statusLabel")
        self.statusLabel.set_markup("<b></b>")
        # evaluate model
        self.evaluateBtn = self.builder.get_object("evaluateBtn")
        self.evaluateBtn.connect("clicked", self.on_evaluate_clicked)
        self.evaluateBtn.set_sensitive(False)
        # save as model result
        self.saveAsModelEvaluationBtn = self.builder.get_object("saveAsModelEvaluationBtn")
        self.saveAsModelEvaluationBtn.connect("clicked", self.on_save_as_flow_evaluated_clicked)
        self.saveAsModelEvaluationBtn.set_sensitive(False)
        # open weka rules
        self.openRulesBtn = self.builder.get_object("openRulesBtn")
        self.openRulesBtn.connect("clicked", self.on_open_rules_clicked)
        # convert weka rules to python
        self.convertToPyBtn = self.builder.get_object("convertToPyBtn")
        self.convertToPyBtn.connect("clicked", self.on_convert_to_py_clicked)
        # save as python model
        self.saveAsPyBtn = self.builder.get_object("saveAsPyBtn")
        self.saveAsPyBtn.connect("clicked", self.on_save_as_py_clicked)
        ## convert to P
        self.openHaclBtn = self.builder.get_object("openHaclBtn")
        self.openHaclBtn.connect("clicked", self.on_open_hacl_clicked)
        
        self.openEvaluatedFlowBtn = self.builder.get_object("openEvaluatedFlowBtn")
        self.openEvaluatedFlowBtn.connect("clicked", self.on_open_evaluated_flow_clicked)
        
        self.convertToPBtn = self.builder.get_object("convertToPBtn")
        self.convertToPBtn.connect("clicked", self.on_convert_to_P_clicked)
        self.convertToPBtn.set_sensitive(False)
        
        self.saveAsPBtn = self.builder.get_object("saveAsPBtn")
        self.saveAsPBtn.connect("clicked", self.on_save_as_P_clicked)
        self.saveAsPBtn.set_sensitive(False)
               
        #list store & tree
        self.liststoreAttributes = gtk.ListStore(str,str)
        self.treeView.set_model(self.liststoreAttributes)
        
        self.textViewRoutes  = self.builder.get_object("textViewRoutes")
        self.textViewConvertedRoutes  = self.builder.get_object("textViewConvertedRoutes")
        self.textViewXml  = self.builder.get_object("textViewXml")
        self.textViewModel  = self.builder.get_object("textViewModel")
        self.textViewModelOutput  = self.builder.get_object("textViewModelOutput")
        self.textViewWekaRules  = self.builder.get_object("textViewWekaRules")
        self.textViewPyRules  = self.builder.get_object("textViewPyRules")
        self.textViewHacl  = self.builder.get_object("textViewHacl")
        self.textViewEvaluatedFlowAttributes  = self.builder.get_object("textViewEvaluatedFlowAttributes")
        self.textViewP  = self.builder.get_object("textViewP")
        #data converter
        self.routes = RouteConverter()
        self.attr = AttributeConverter()
        self.new()
        self.rules = RuleConverter()
        self.model = ModelEvaluator()
        self.pConverter = PConverter()

    def on_open_routes_clicked(self, widget):
        dialog = self.open_dialog(["xml"])
        response = dialog.run()
        
        if response == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
            self.textViewRoutes.get_buffer().set_text(self.routes.readRoutes(filename))
            self.convertRoutesBtn.set_sensitive(True)
            #rules.convert(rulesStr)
        dialog.destroy()
        
    def on_convert_routes_clicked(self, widget):
        try: 
            self.textViewConvertedRoutes.get_buffer().set_text(self.routes.convert())
            self.saveAsConvertedRoutesBtn.set_sensitive(True)
        except Exception, Argument:
            # Display error
            self.error_dialog("Error", "Could not convert Routes",str(Argument))
            
    def on_save_as_conv_routes_clicked(self, widget):
        chooser = self.save_dialog("xml")
        response = chooser.run()
        
        path = "None"
        if response == gtk.RESPONSE_OK:
            print("Save as clicked")
            path = chooser.get_filename()
        
        if path != "None":
            self.routes.writeOutput(path)# self.routes.convert(), 

        chooser.destroy()

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
        #creating dialog
        dialog = self.open_dialog(["xml","wekadata"])
        response = dialog.run()

        if response == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
            dialog.destroy()
            self.currentFlowAttrIndex = 0
            if ".xml"  in filename: 
                self.xmlPath = filename
                self.flowAttributesList = self.attr.readXML(self.xmlPath)
            elif ".arff"  in filename: 
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
          
    def on_save_as_clicked(self, widget):
        chooser = self.save_dialog("xml")
        response = chooser.run()
        
        path = "None"
        if response == gtk.RESPONSE_OK:
            print("Save As Clicked")
            path = chooser.get_filename()
        
        if path != "None":
                self.xmlPath = path
                self.on_save_clicked(widget)
                self.saveBtn.set_sensitive(True)
                self.window.set_title("Flow Description Attributes - " + self.xmlPath)
                
        chooser.destroy()
        
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
                         
    def on_open_rules_clicked(self, widget):
        
        dialog = self.open_dialog(["rules"])
        response = dialog.run()
        
        if response == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
            self.textViewWekaRules.get_buffer().set_text(self.rules.readFromFile(filename))
            self.convertToPyBtn.set_sensitive(True)
            #rules.convert(rulesStr)
        dialog.destroy()

    def on_convert_to_py_clicked(self, widget):
        try: 
            self.textViewPyRules.get_buffer().set_text(self.rules.convert())
            self.saveAsPyBtn.set_sensitive(True)
        except Exception, Argument:
            # Display error
            self.error_dialog("Error", "Could not convert Weka rules to Python",str(Argument))
        
    def on_save_as_py_clicked(self, widget):
        chooser = self.save_dialog("py")
        response = chooser.run()
        
        path = "None"
        if response == gtk.RESPONSE_OK:
            print("Save as clicked")
            path = chooser.get_filename()
        
        if path != "None":
            self.rules.writeOutput(path) # self.rules.outputStr,

        chooser.destroy()
        
    def on_open_model_clicked(self, widget):
        dialog = self.open_dialog(["py"])
        response = dialog.run()
        
        if response == gtk.RESPONSE_OK:
            print("Open clicked")
            filePath = dialog.get_filename()
            dialog.destroy()
            self.textViewModel.get_buffer().set_text(self.model.readFromFile(filePath))
            self.evaluateBtn.set_sensitive(True)   
        
    def on_evaluate_clicked(self, widget):
        
        try: 
            # Display warning before overriding model 
            warningDialog = gtk.MessageDialog(self.window, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_NONE, "Do you want to continue?")
            warningDialog.set_title("Warning")
            warningDialog.add_buttons(gtk.STOCK_OK, gtk.RESPONSE_OK,gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
            warningDialog.set_default_response(gtk.RESPONSE_OK)
            warningDialog.set_resizable(False)
            warningDialog.format_secondary_text("Current Model.py will be overridden by: \n\n"+ self.model.filePath)
            #warningDialog.set_property("secondary-text",("All unsaved changes will be lost."))
            result = warningDialog.run ()
            warningDialog.destroy()

            #check if they are OK to continue after warning
            if  result == gtk.RESPONSE_OK:
                self.textViewModelOutput.get_buffer().set_text(str('\n'.join(map(str, self.model.evaluate(self.flowAttributesList)))))
                self.saveAsModelEvaluationBtn.set_sensitive(True)
        except Exception, Argument:
            self.error_dialog("Error", "Could not load model",str(Argument))
            
    def on_save_as_flow_evaluated_clicked(self, widget):
        chooser = self.save_dialog("xml")
        response = chooser.run()
        
        path = "None"
        if response == gtk.RESPONSE_OK:
            print("Save as clicked")
            path = chooser.get_filename()
        
        if path != "None":
                self.model.writeModelEvaluationXML(path,self.flowAttributesList,self.model.evaluationResults)
        chooser.destroy()
    
    def on_open_hacl_clicked(self, widget):
               
        dialog = self.open_dialog(["txt"])
        response = dialog.run()
        
        if response == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
            self.textViewHacl.get_buffer().set_text(self.pConverter.readHacl(filename))
            
            if self.textViewEvaluatedFlowAttributes.get_buffer().get_char_count()>0:
                self.convertToPBtn.set_sensitive(True)
                
        dialog.destroy()
        
    def on_open_evaluated_flow_clicked(self, widget):
              
        dialog = self.open_dialog(["xml"])
        response = dialog.run()
        
        if response == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
            self.textViewEvaluatedFlowAttributes.get_buffer().set_text(self.pConverter.readEvaluatedFlow(filename))
                      
            if self.textViewHacl.get_buffer().get_char_count()>0:
                self.convertToPBtn.set_sensitive(True)
        
        dialog.destroy()    
        
    def on_convert_to_P_clicked(self, widget):
        # textViewP
        try: 
            self.textViewP.get_buffer().set_text(self.pConverter.convert())
            self.saveAsPBtn.set_sensitive(True)
        except Exception, Argument:
            self.error_dialog("Error", "Could convert to P format",str(Argument))
        
    def on_save_as_P_clicked(self, widget):  
        chooser = self.save_dialog("p")
        response = chooser.run()
        
        path = "None"
        if response == gtk.RESPONSE_OK:
            print("Save as clicked")
            path = chooser.get_filename()
        
        if path != "None":
            self.pConverter.writeOutput(path)
                 
        chooser.destroy()
             
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
        
    def open_dialog(self,extensions):
        
        dialog = gtk.FileChooserDialog("Please choose a file", self.window,
            gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
             gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        
        for ext in extensions:
            if ext == "py":
                name = "Python Files"
                pattern = "*.py"
            elif ext == "xml":
                name = "XML Files"
                pattern = "*.xml"
            elif ext == "rules":
                name = "Weka Rules"
                pattern = "*.rules"
            elif ext == "wekadata":
                name = "Weka Files"
                pattern = "*.arff"
            elif ext == "txt":
                name = "Text Files"
                pattern = "*.txt"
            elif ext == "p":
                name = "P Files"
                pattern = "*.P"
                    
            filter = gtk.FileFilter()
            filter.set_name(name)
            filter.add_pattern(pattern)
            dialog.add_filter(filter)
    
        return dialog
    
    def save_dialog(self,extensions):
        
        chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OK,gtk.RESPONSE_OK))
        
        for ext in extensions:
            if ext == "py":
                name = "Python Files"
                pattern = "*.py"
            elif ext == "xml":
                name = "XML Files"
                pattern = "*.xml"
            elif ext == "rules":
                name = "Weka Rules"
                pattern = "*.rules"
            elif ext == "wekadata":
                name = "Weka Files"
                pattern = "*.arff"
            elif ext == "txt":
                name = "Text Files"
                pattern = "*.txt"
            elif ext == "p":
                name = "P Files"
                pattern = "*.P"
                    
            filter = gtk.FileFilter()
            filter.set_name(name)
            filter.add_pattern(pattern)
            chooser.add_filter(filter)
            chooser.set_default_response(gtk.RESPONSE_OK)
    
        return chooser
        
    def error_dialog(self, title, message,secondary_message):
            # Display error
            warningDialog = gtk.MessageDialog(self.window, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_NONE, message)
            warningDialog.set_title(title)
            warningDialog.add_buttons(gtk.STOCK_OK, gtk.RESPONSE_OK)
            warningDialog.set_default_response(gtk.RESPONSE_OK)
            warningDialog.set_resizable(False)
            warningDialog.format_secondary_text("The following error was caught:\n\n"+ secondary_message)
            result = warningDialog.run ()
            warningDialog.destroy()

if __name__ == "__main__":
    hwg = AttributesInterface()
    gtk.main()