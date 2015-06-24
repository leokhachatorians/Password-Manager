from db_init import Locker, Accounts, session
import sys
from PyQt4 import QtCore, QtGui, uic
import classes.account_viewer_class #No idea why 'from classes.account_viewer_class import AccountViewer doesnt work'

delete_account_page = uic.loadUiType("pages/delete_account_page.ui")[0]

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

		self.account_viewer_window = None

	def delete(self):
		password_input = self.password_verify_input.text()
		account_name = self.account_display.text()

		if session.query(Accounts).filter_by(account=account_name, password=password_input).count() == 1:
			session.query(Locker).filter_by(account=account_name).delete()
			session.query(Accounts).filter_by(account=account_name).delete()
			session.commit()
			QtGui.QMessageBox.information(self,"Deleted","Succesfully deleted account:[{}]".format(account_name))
		else:
			QtGui.QMessageBox.information(self,"Error","Incorrect Match, Deletion Aborted")

		self.exit()

	def exit(self):
		self.reload_account_viewer()
		self.close()

	def reload_account_viewer(self):
		if self.account_viewer_window is None:
			self.account_viewer_window = classes.account_viewer_class.AccountViewer()

		self.account_viewer_window.populate_manager()
		self.account_viewer_window.show()