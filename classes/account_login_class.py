from db_init import session, Accounts
from classes.entry_viewer_class import EntryViewer
import classes.account_viewer_class #No idea why 'from classes.account_viewer_class import AccountViewer doesnt work'
import sys
from PyQt4 import QtCore, QtGui, uic

account_login_page = uic.loadUiType("pages/account_login_page.ui")[0]

class AccountLogin(QtGui.QMainWindow, account_login_page):

	def __init__(self, account, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.account = account

		# Button actions
		self.save_button.clicked.connect(self.login_check)
		self.exit_button.clicked.connect(self.exit)

		# Display account variable, make sure to set to read only
		self.account_display.setText(account)
		self.account_display.setReadOnly(True)

		# Open entry viewer check
		self.entry_viewer = None

		# Re-open account viewer check
		self.account_viewer_window = None

	def login_check(self):
		account = self.account_display.text()
		password = self.password_input.text()
		if session.query(Accounts).filter_by(account=account, password=password).count() == 1:
			if self.entry_viewer is None:
				self.entry_viewer = EntryViewer(account)
			self.entry_viewer.show()
			self.entry_viewer.refresh()
			self.close()
		else:
			QtGui.QMessageBox.information(self, "Invalid","You entered the wrong password")
			self.reload_account_viewer()
			self.close()

	def reload_account_viewer(self):
		if self.account_viewer_window is None:
			self.account_viewer_window = classes.account_viewer_class.AccountViewer()

		self.account_viewer_window.populate_manager()
		self.account_viewer_window.show()

	def exit(self):
		self.reload_account_viewer()
		self.close()