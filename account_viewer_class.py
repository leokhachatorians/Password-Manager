from account_db_init import Accounts
from account_db_init import session as acnt_session
import sys
from PyQt4 import QtCore, QtGui, uic
from main_page_class import MainWindow
from new_account_class import NewAccount
from account_login_class import AccountLogin
from delete_account_class import DeleteAccount

account_viewer_page = uic.loadUiType("account_viewer_page.ui")[0]

class AccountViewer(QtGui.QMainWindow, account_viewer_page):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self,parent)
		self.setupUi(self)

		# Default window states; not currently open
		self.main_window = None
		self.new_account_window = None
		self.account_login_window = None
		self.delete_account_window = None

		# Button Actions
		self.new_account_button.clicked.connect(self.open_new_account_window)

		# Set the context menu for the account viewer
		self.manager.customContextMenuRequested.connect(
			self.context_menu_for_manager)

	def context_menu_for_manager(self, event):
		self.menu = QtGui.QMenu(self)

		# Login Selection
		action_login_selection = QtGui.QAction('Login', self)
		action_login_selection.triggered.connect(self.login_selection)
		self.menu.addAction(action_login_selection)

		# Delete Selection
		action_delete_selection = QtGui.QAction('Delete', self)
		action_delete_selection.triggered.connect(self.delete_selection)
		self.menu.addAction(action_delete_selection)

		self.menu.popup(QtGui.QCursor.pos())

	def populate_manager(self):
		row = 0
		item = 0
		limit = acnt_session.query(Accounts).count()
		self.set_manager_count(1)

		for instance in acnt_session.query(Accounts):
			self.manager.setItem(row, item, QtGui.QTableWidgetItem(instance.account))

			# Do this to prevent an additional row to be added
			if row < limit - 1:
				row += 1
				self.manager.insertRow(row)

	def set_manager_count(self, amount=0):
		# Always set the rowcount to zero first, otherwise first row acts weird
		self.manager.setRowCount(0)
		self.manager.setRowCount(amount)

	def open_new_account_window(self):
		if self.new_account_window is None:
			self.new_account_window = NewAccount()
		self.new_account_window.show()

	def login_selection(self):
		row = self.manager.currentRow()
		account = self.manager.item(row, 0).text()

		self.open_account_login_window(account)

	def delete_selection(self):
		row = self.manager.currentRow()
		account = self.manager.item(row, 0).text()

		self.open_delete_account_window(account)

	def open_delete_account_window(self, account):
		if self.delete_account_window is None:
			self.delete_account_window = DeleteAccount(account)
		else:
			# Set to None to clear out previous form
			self.delete_account_window = None
			self.delete_account_window = DeleteAccount(account)

		self.delete_account_window.show()

	def open_account_login_window(self, account):
		if self.account_login_window is None:
			self.account_login_window = AccountLogin(account)
		else:
			# Set to None to clear out previous form
			self.account_login_window = None
			self.account_login_window = AccountLogin(account)

		self.account_login_window.show()

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	gui = AccountViewer()
	gui.populate_manager()
	gui.show()
	app.exec_()