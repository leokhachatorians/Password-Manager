from db_init import session, Accounts
import classes.account_viewer_class #No idea why 'from classes.account_viewer_class import AccountViewer doesnt work'
import sys
from PyQt4 import QtCore, QtGui, uic

new_account_page = uic.loadUiType("pages/new_account_page.ui")[0]

class NewAccount(QtGui.QMainWindow, new_account_page):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self,parent)
		self.setupUi(self)

		# Button Actions
		self.exit_button.clicked.connect(self.exit)
		self.save_button.clicked.connect(self.add)

		# Re-open account viewer check
		self.account_viewer_window = None

	def check_if_empty_string(self, account='null',password='null'):
		if not account or not account.strip() or not password or not password.strip():
			return True

	def add(self):
		add_account = self.account_input.text()
		add_password = self.password_input.text()

		if self.check_if_empty_string(add_account, add_password):
			QtGui.QMessageBox.warning(
				self, "Invalid Entry", "Make sure you did not leave any field blank")
		elif session.query(Accounts).filter_by(account=add_account).count() >= 1:
			QtGui.QMessageBox.warning(
				self, "Invalid Entry", " ACCOUNT:[{}] \n Already Exists!".format(add_account))
		else:
			session.add(Accounts(account=add_account,
								 password=add_password))
			session.commit()
			QtGui.QMessageBox.information(self, "Completed", "Succesfully Saved \n ACCOUNT:[{}] \n PASSWORD:[{}]".format(add_account, (len(add_password) * '*')))

			self.reload_account_viewer()
			self.exit()

	def reload_account_viewer(self):
		if self.account_viewer_window is None:
			self.account_viewer_window = classes.account_viewer_class.AccountViewer()

		self.account_viewer_window.populate_manager()
		self.account_viewer_window.show()

	def exit(self):
		self.account_input.clear()
		self.password_input.clear()
		self.reload_account_viewer()
		self.close()