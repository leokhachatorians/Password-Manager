from db_init import Accounts, session
import sys
from PyQt4 import QtCore, QtGui, uic
from classes.entry_viewer_class import EntryViewer
from classes.new_account_class import NewAccount
from classes.account_login_class import AccountLogin
from classes.delete_account_class import DeleteAccount
from classes.about_class import AboutPage

account_viewer_page = uic.loadUiType("pages/account_viewer_page.ui")[0]

class AccountViewer(QtGui.QMainWindow, account_viewer_page):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self,parent)
		self.setupUi(self)

		# Default window states; not currently open
		self.entry_viewer = None
		self.new_account_window = None
		self.account_login_window = None
		self.delete_account_window = None
		self.about_window = None

		# File Menu Actiosn
		self.action_new_account.triggered.connect(self.open_new_account_window)
		self.action_exit.triggered.connect(self.close)
		self.action_about.triggered.connect(self.open_about_window)

		# Set the context menu for the account viewer
		self.manager.customContextMenuRequested.connect(
			self.context_menu_for_manager)

		# Double click setup
		self.manager.doubleClicked.connect(self.login_selection)

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
		limit = session.query(Accounts).count()
		self.set_manager_count(1)

		for instance in session.query(Accounts):
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
		self.close()

	def login_selection(self):
		row = self.manager.currentRow()
		account = self.manager.item(row, 0).text()

		self.open_account_login_window(account)
		self.close()

	def delete_selection(self):
		"""
		Description:
			When a user tries to delete an account
			via right clicking on the cell, this function
			is called.
			Grabs the account name via the cell location
			and calls the delete function.
		"""
		row = self.manager.currentRow()
		account = self.manager.item(row, 0).text()

		self.open_delete_account_window(account)

	def open_delete_account_window(self, account):
		"""
		Arguments:
			account - The account name of which the user would like
			to delete
		Description:
			When a user attempts to delete a specific account,
			this funciton is called. Determines if the window 
			is opened, and if not, opens the window.
		"""
		if self.delete_account_window is None:
			self.delete_account_window = DeleteAccount(account)
		else:
			# Set to None to clear out previous form
			self.delete_account_window = None
			self.delete_account_window = DeleteAccount(account)

		self.delete_account_window.show()
		self.close()

	def open_account_login_window(self, account):
		"""
		Description:
			When a user attempts to login into a specific account,
			this function is called and determines whether the window
			has been opened or not. End goal is to open the window
			as ordered.
		"""
		if self.account_login_window is None:
			self.account_login_window = AccountLogin(account)
		else:
			# Set to None to clear out previous form
			self.account_login_window = None
			self.account_login_window = AccountLogin(account)

		self.account_login_window.show()

	def open_about_window(self):
		"""
		Description:
			When called the funciton checks to see
			if the about window has been opened, if not,
			the window is opened.
		"""
		if self.about_window is None:
			self.about_window = AboutPage()

		self.about_window.show()
