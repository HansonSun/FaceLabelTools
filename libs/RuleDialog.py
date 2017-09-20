from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os
import init


class RuleDialog(QDialog):
	def __init__(self,mode,parent=None):
		super(RuleDialog,self).__init__(parent) 
		self.mode=mode
		if(self.mode==0):
			self.openLabelfileUI()
		else:
			self.openPictureUI()

	def openLabelfileUI(self):

		labelfile_label=QLabel("label file")
		self.labelfile_textedit=QTextEdit("")
		labelfile_btn=QPushButton(".")
		self.labelfile_textedit.setFixedHeight(50)

		rule_list=os.listdir("input_rules")
		rule_list= [ i.split('.')[0] for i in rule_list ] 
	
		view_mode_lables=QLabel("choose view mode:")
		self.view_mode_box=QComboBox()
		self.view_mode_box.addItems(["MODE_ALL","MODE_UNLABELED","MODE_LABELED","VIEW_MODE_RANDOM"])

		ruleinput_label=QLabel("input rule:")
		self.input_rulebox=QComboBox()
		self.input_rulebox.addItems(rule_list)

		ruleoutput_label=QLabel("ouput rule:")
		self.output_rulebox=QComboBox()
		self.output_rulebox.addItems(rule_list)


		yes_btn=QPushButton("yes")
		no_btn=QPushButton("no")

		verticle_layout=QGridLayout()
		verticle_layout.addWidget(labelfile_label,0,0)
		verticle_layout.addWidget(self.labelfile_textedit,1,0,1,2)
		verticle_layout.addWidget(labelfile_btn,1,4,1,2)

		verticle_layout.addWidget(view_mode_lables,2,0)
		verticle_layout.addWidget(self.view_mode_box,3,0)

		verticle_layout.addWidget(ruleinput_label,4,0)
		verticle_layout.addWidget(self.input_rulebox,5,0)

		verticle_layout.addWidget(ruleoutput_label,6,0)
		verticle_layout.addWidget(self.output_rulebox,7,0)

		verticle_layout.addWidget(yes_btn,8,0,1,3, Qt.AlignLeft | Qt.AlignVCenter)
		verticle_layout.addWidget(no_btn,8,3,1,3, Qt.AlignRight | Qt.AlignVCenter)

		verticle_layout.setHorizontalSpacing(10)
		verticle_layout.setVerticalSpacing(10)
		verticle_layout.setContentsMargins(10, 10, 10, 10)

		self.setLayout(verticle_layout)
		
		yes_btn.clicked.connect( self.save_config )
		no_btn.clicked.connect( self.dont_save_config )
		labelfile_btn.clicked.connect( self.get_label_file_path )

	def openPictureUI(self):

		imgfile_label=QLabel("picture file")
		self.imgfile_textedit=QTextEdit("")
		imgfile_btn=QPushButton(".")
		self.imgfile_textedit.setFixedHeight(50)

		rule_list=os.listdir("input_rules")
		rule_list= [ i.split('.')[0] for i in rule_list ] 
	

		ruleoutput_label=QLabel("ouput rule:")
		self.output_rulebox=QComboBox()
		self.output_rulebox.addItems(rule_list)

		yes_btn=QPushButton("yes")
		no_btn=QPushButton("no")

		verticle_layout=QGridLayout()
		verticle_layout.addWidget(imgfile_label,0,0)
		verticle_layout.addWidget(self.imgfile_textedit,1,0,1,2)
		verticle_layout.addWidget(imgfile_btn,1,4,1,2)

		verticle_layout.addWidget(ruleoutput_label,2,0)
		verticle_layout.addWidget(self.output_rulebox,3,0)

		verticle_layout.addWidget(yes_btn,4,0,1,3, Qt.AlignLeft | Qt.AlignVCenter)
		verticle_layout.addWidget(no_btn,4,3,1,3, Qt.AlignRight | Qt.AlignVCenter)

		verticle_layout.setHorizontalSpacing(10)
		verticle_layout.setVerticalSpacing(10)
		verticle_layout.setContentsMargins(10, 10, 10, 10)

		self.setLayout(verticle_layout)
		
		yes_btn.clicked.connect( self.save_config )
		no_btn.clicked.connect( self.dont_save_config )
		imgfile_btn.clicked.connect( self.get_img_file_path )


	def save_config(self):
		if(self.mode==0):
			self.load_inputrule_file(os.path.join("input_rules",str(self.input_rulebox.currentText())+".txt" ) )
			self.load_outputrule_file(os.path.join("input_rules",str(self.output_rulebox.currentText())+".txt") )
			init.glb_view_mode=self.view_mode_box.currentIndex()
			init.glb_save_change=1
			self.close()
		else :
			with open("result/tmp/~imgfile.txt","w") as f:
				f.write("%s %d"%(init.glb_imgfile_path,-1) )

			self.load_inputrule_file(os.path.join("input_rules",str(self.output_rulebox.currentText())+".txt") )
			self.load_outputrule_file(os.path.join("input_rules",str(self.output_rulebox.currentText())+".txt") )
			init.glb_view_mode=0
			init.glb_save_change=1
			self.close()


	def dont_save_config(self):
		init.glb_save_change=0
		self.close()	

	def get_img_file_path(self):
		filename=QFileDialog.getOpenFileName(self,"sss","./","image file (*.png *.jpg)")
		self.imgfile_textedit.setText(filename)
		init.glb_imgfile_path=str(filename)
		init.glb_labelfile_path="result/tmp/~imgfile.txt"

	def get_label_file_path(self):
		filename=QFileDialog.getOpenFileName(self,"sss","./","image file (*.txt)")
		self.labelfile_textedit.setText(filename)
		init.glb_labelfile_path=str(filename)

	def load_inputrule_file(self,file_path):
		if file_path!="":
			with open(file_path,"r")as f:
				rules=f.read()
				rules=rules.strip()
				init.glb_input_rule_list=rules.split(",")
				print "input rule:",init.glb_input_rule_list

	def load_outputrule_file(self,file_path):
		if file_path!="":
			with open(file_path,"r")as f:
				rules=f.read()
				rules=rules.strip()
				init.glb_output_rule_list=rules.split(",")	
				print "output rule",init.glb_output_rule_list

if __name__ == "__main__":

	app=QApplication(sys.argv)
	win=RuleDialog(1)
	win.show()
	app.exec_()

