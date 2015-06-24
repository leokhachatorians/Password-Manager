from db_init import session, Locker
import sys
from PyQt4 import QtCore, QtGui, uic
from classes.add_entry_class import AddEntry
from classes.modify_password_class import ModifyPassword
from classes.delete_entry_class import DeleteEntry
from classes.about_class import AboutPage
import classes.account_viewer_class #No idea why 'from classes.account_viewer_class import AccountViewer doesnt work'

main_page = uic.loadUiType("pages/password_main_page.ui")[0]

class EntryViewer(QtGui.QMainWindow, main_page):
	"""Defines the main window and various attributes/functions it holds"""

	def __init__(self, account, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		
		# The account is the master account which holds that groups password stuff
		self.account = account

		# Default window states; not currently open
		self.add_window = None
		self.modify_window = None
		self.delete_window = None
		self.about_window = None
		self.modify_password_window = None
		self.account_viewer_window = None

		# File menu actions
		self.action_add_new.triggered.connect(self.open_add_window)
		self.action_exit.triggered.connect(self.exit)
		self.action_show_all.triggered.connect(self.show_passwords)
		self.action_switch_user.triggered.connect(self.switch_user)

		# Button actions
		self.add_button.clicked.connect(self.open_add_window)
		self.test_button.clicked.connect(self.refresh)

		# Sets the custom contect menu for the table
		self.manager.customContextMenuRequested.connect(
			self.context_menu_for_manager)

		# Double Click Setup
		self.manager.doubleClicked.connect(self.show_specific_password)

	def switch_user(self):
		if self.account_viewer_window is None:
			self.account_viewer_window = classes.account_viewer_class.AccountViewer()

		self.account_viewer_window.populate_manager()
		self.account_viewer_window.show()
		self.close()

	def show_passwords(self):
		row = 0
		account = self.account

		# Item set to two since passwords will always be in column two;
		# (0,     1,      2)
		# (url, user, PASSWORD)
		item = 2
		for instance in session.query(Locker).filter_by(account=self.account):
			self.manager.setItem(
				row, item, QtGui.QTableWidgetItem(instance.password))
			row += 1

	def refresh(self):
		row = 0
		item = 0
		limit = session.query(Locker).filter_by(account=self.account).count()
		self.clear(1)
		for instance in session.query(Locker).filter_by(account=self.account):
			self.manager.setItem(
				row, item, QtGui.QTableWidgetItem(instance.url))
			item += 1
			self.manager.setItem(
				row, item, QtGui.QTableWidgetItem(instance.user))
			item = 0

			# Do this so an extra row isn't appended
			if row < limit - 1:
				row += 1
				self.manager.insertRow(row)

	def context_menu_for_manager(self, event):
		self.menu = QtGui.QMenu(self)

		# Modify Password Selection
		action_modify_password = QtGui.QAction('Change Password', self)
		action_modify_password.triggered.connect(self.modify_password)
		self.menu.addAction(action_modify_password)

		# Delete Selection Creation
		action_delete = QtGui.QAction('Delete', self)
		action_delete.triggered.connect(self.delete_selection)
		self.menu.addAction(action_delete)

		# Show Specific Password
		action_show_specific = QtGui.QAction('View Password', self)
		action_show_specific.triggered.connect(self.show_specific_password)
		self.menu.addAction(action_show_specific)

		self.menu.popup(QtGui.QCursor.pos())

	def modify_password(self):
		row = self.manager.currentRow()

		# 0 and 1 are the respective columns for url and user
		url = self.manager.item(row, 0). text()
		user = self.manager.item(row, 1).text()
		self.open_modify_password_window(url, user, self.account)

	def delete_selection(self):
		row = self.manager.currentRow()

		# 0 and 1 are the respective columns for url and user
		url = self.manager.item(row, 0).text()
		user = self.manager.item(row, 1).text()
		self.open_delete_window(url, user, self.account)

	def show_specific_password(self):
		row = self.manager.currentRow()

		# 0 and 1 are the respective columns for url and user
		url = self.manager.item(row, 0).text()
		user = self.manager.item(row, 1).text()

		for instance in session.query(Locker).filter_by(url=url,user=user,account=self.account):
			self.manager.setItem(row, 2, QtGui.QTableWidgetItem(instance.password))

	def clear(self, amount=0):
		# Always sets the rowcount to zero first, otherwise first row acts weird
		self.manager.setRowCount(0)
		self.manager.setRowCount(amount)

	def exit(self):
		exit()

	def open_add_window(self):
		if self.add_window is None:
			self.add_window = AddEntry(self.account)
		self.add_window.show()
		self.close()

	def open_modify_password_window(self, url, user, account):
		# If window has not been opened since start of application
		if self.modify_password_window is None:
			self.modify_password_window = ModifyPassword(url, user, account)

		# If it has been opened prior
		else:
			self.modify_password_window = None
			self.modify_password_window = ModifyPassword(url, user, account)

		self.modify_password_window.show()
		self.close()	

	def open_delete_window(self, url, user, account):
		# If window has not been opened since start of application
		if self.delete_window is None:
			self.delete_window = DeleteEntry(url, user, account)

		# If it has been opened prior, zero's it out so it can actually work again.
		else:
			self.delete_window = None
			self.delete_window = DeleteEntry(url, user, account)

		self.delete_window.show()
		self.close()