from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os

class ruleWidget(QDockWidget):
	def __init__(self,parent=None):
		super(ruleWidget,self).__init__(parent) 
		
		rule_list=os.listdir("input_rules")
		rule_list= [ i.split('.')[0] for i in rule_list ] 
	
		showWidget=QWidget()

		view_mode_lables=QLabel("choose view mode:")
		view_mode_box=QComboBox()
		view_mode_box.addItems(["MODE_ALL","MODE_UNLABELED","MODE_LABELED","VIEW_MODE_RANDOM"])

		ruleinput_label=QLabel("input rule:")
		ruleoutput_label=QLabel("ouput rule:")
		
		input_rulebox=QComboBox()
		input_rulebox.addItems(rule_list)
		output_rulebox=QComboBox()
		output_rulebox.addItems(rule_list)

		input_rulebox.setEnabled(0)
		output_rulebox.setEnabled(0)

		verticle_layout=QVBoxLayout()
		verticle_layout.addWidget(view_mode_lables)
		verticle_layout.addWidget(view_mode_box)

		verticle_layout.addWidget(ruleinput_label)

		verticle_layout.addWidget(input_rulebox)

		verticle_layout.addWidget(ruleoutput_label)

		verticle_layout.addWidget(output_rulebox)

		showWidget.setLayout(verticle_layout)
		self.setWidget(showWidget)

