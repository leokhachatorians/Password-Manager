from account_db_init import Accounts
from account_db_init import session as session_acnt
from db_init import Locker
from db_init import session as session_pw
import sys
from PyQt4 import QtCore, QtGui, uic

delete_account_page = uic.loadUiType("delete_account_page.ui")[0]

class DeleteAccount(QtGui.QMainWindow, delete_account_page):
	def __init__(self, account, parent=None):
		QtGui.QMainWindow.__init__(self,parent)
		self.setupUi(self)
		self.account = account

		# Button Actions
		self.delete_button.clicked.connect(self.delete)
		self.exit_button.clicked.connect(self.exit)

		# Set to display the account
		self.account_display.setText(account)
		self.account_display.setReadOnly(True)


	def delete(self):
		delete_account = self.account_verify_input.text()

		if delete_account == self.account_display.text():
			session_pw.query(Locker).filter_by(account=delete_account).delete()
			session_acnt.query(Accounts).filter_by(account=delete_account).delete()
			session_acnt.commit()
			session_pw.commit()

		QtGui.QMessageBox.information(self,"Deleted","Succesfully deleted account:[{}]".format(delete_account))

		self.exit()

	def exit(self):
		self.close()