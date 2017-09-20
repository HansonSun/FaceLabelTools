from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os
import init

class TipWidget(QDockWidget):
	def __init__(self,parent=None):
		super(TipWidget,self).__init__(parent)

		content=QWidget()
		label_1=QLabel("7p Warning")
		self.warn7p_choose=QCheckBox()
		self.warn7p_choose.clicked.connect(self.warn7p_save_change)

		label_2=QLabel("auto put 7p")
		self.put7p_choose=QCheckBox()
		self.put7p_choose.clicked.connect(self.put7p_save_change)


		layout=QVBoxLayout()
		layout.addWidget(label_1)
		layout.addWidget(self.warn7p_choose)
		layout.addWidget(label_2)
		layout.addWidget(self.put7p_choose)
		layout.addStretch()
		content.setLayout(layout)

		self.setWidget(content)

	def warn7p_save_change(self):
		box_status=self.warn7p_choose.isChecked() 

		if(box_status==True):
			print "Enable 7 point warning"
		else:
			print "Disable 7 point warning"


		init.glb_7p_warning=box_status


	def put7p_save_change(self):
		box_status=self.put7p_choose.isChecked()

		if(box_status==True):
			print "Enable auto put 7 p"
		else:
			print "Disable auto put 7 p"

		init.glb_auto_put_7p=box_status

if __name__=="__main__":
	app=QApplication(sys.argv)
	win=TipWidget()
	win.show()
	app.exec_()
