import sys
from PyQt4 import QtCore, QtGui, uic
from db_init import session, Locker
import time

main_page = uic.loadUiType("password_main_page.ui")[0]
add_page = uic.loadUiType("password_add_page.ui")[0]
password_modify_page = uic.loadUiType("password_modify_page.ui")[0]
delete_page = uic.loadUiType("password_delete_page.ui")[0]
about_page = uic.loadUiType("about_page.ui")[0]


class MainWindow(QtGui.QMainWindow, main_page):
	"""Defines the main window and various attributes/functions it holds"""

	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)

		# File menu actions
		self.action_add_new.triggered.connect(self.open_add_window)
		self.action_exit.triggered.connect(self.exit)
		self.action_show_all.triggered.connect(self.show_passwords)
		self.action_about.triggered.connect(self.open_about_window)

		# Button actions
		self.add_button.clicked.connect(self.open_add_window)
		self.test_button.clicked.connect(self.refresh)

		# Sets the custom contect menu for the table
		self.manager.customContextMenuRequested.connect(
			self.context_menu_for_manager)

		# Default window states; not currently open
		self.add_window = None
		self.modify_window = None
		self.delete_window = None
		self.about_window = None
		self.modify_password_window = None

	def show_passwords(self):
		row = 0

		# Item set to two since passwords will always be in column two;
		# (0,     1,      2)
		# (url, user, PASSWORD)
		item = 2

		for instance in session.query(Locker):
			self.manager.setItem(
				row, item, QtGui.QTableWidgetItem(instance.password))
			row += 1

	def refresh(self):
		row = 0
		item = 0
		limit = session.query(Locker).count()
		self.clear(1)
		for instance in session.query(Locker):
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
		self.open_modify_password_window(url, user)

	def delete_selection(self):
		row = self.manager.currentRow()

		# 0 and 1 are the respective columns for url and user
		url = self.manager.item(row, 0).text()
		user = self.manager.item(row, 1).text()
		self.open_delete_window(url, user)

	def show_specific_password(self):
		row = self.manager.currentRow()

		# 0 and 1 are the respective columns for url and user
		url = self.manager.item(row, 0).text()
		user = self.manager.item(row, 1).text()

		for instance in session.query(Locker).filter_by(url=url,user=user):
			self.manager.setItem(row, 2, QtGui.QTableWidgetItem(instance.password))

	def clear(self, amount=0):
		# Always sets the rowcount to zero first, otherwise first row acts weird
		self.manager.setRowCount(0)
		self.manager.setRowCount(amount)

	def exit(self):
		exit()

	def open_add_window(self):
		if self.add_window is None:
			self.add_window = AddPage()
		self.add_window.show()

	def open_modify_password_window(self, url, user):
		# If window has not been opened since start of application
		if self.modify_password_window is None:
			self.modify_password_window = ModifyPasswordPage(url, user)

		# If it has been opened prior
		else:
			self.modify_password_window = None
			self.modify_password_window = ModifyPasswordPage(url, user)

		self.modify_password_window.show()	

	def open_delete_window(self, url, user):
		# If window has not been opened since start of application
		if self.delete_window is None:
			self.delete_window = DeletePage(url, user)

		# If it has been opened prior, zero's it out so it can actually work again.
		else:
			self.delete_window = None
			self.delete_window = DeletePage(url, user)

		self.delete_window.show()

	def open_about_window(self):
		if self.about_window is None:
			self.about_window = AboutPage()

		self.about_window.show()

class AddPage(QtGui.QDialog, add_page):
	"""Window for whenever the user wishes to add something to the database"""

	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)

		# Button Actions
		self.save_button.clicked.connect(self.add)
		self.exit_button.clicked.connect(self.exit)

	def check_if_empty_string(self, url='null', user='null', password='null'):
		if not url or not url.strip() or not user or not user.strip() or not password or not password.strip():
			return True

	def add(self):
		add_url = self.website_input.text()
		add_user = self.account_input.text()
		add_password = self.password_input.text()

		if self.check_if_empty_string(add_url, add_user, add_password):
			QtGui.QMessageBox.warning(
				self, "Invalid Entry", "Make sure you did not leave any field blank")
		elif session.query(Locker).filter_by(url=add_url, user=add_user).count() >= 1:
			QtGui.QMessageBox.warning(
				self, "Invalid Entry", " URL:[{}] \n USER:[{}] \n Already exists!".format(add_url, add_user))
		else:
			session.add(Locker(url=add_url,
							   user=add_user,
							   password=add_password))
			session.commit()
			QtGui.QMessageBox.information(self, "Completed", "Succesfully Saved \n URL:[{}] \n USER:[{}] \n PASSWORD:[{}]".format(
				add_url, add_user, (len(add_password) * '*')))

			self.exit()

	def exit(self):
		#Run clear input prior to exiting ensure clean window
		self.website_input.clear()
		self.account_input.clear()
		self.password_input.clear()
		self.close()

class ModifyPasswordPage(QtGui.QDialog, password_modify_page):
	"""Window for when the user determines to modify their prior password"""

	def __init__(self, url, user, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)

		# Button Actions
		self.save_button.clicked.connect(self.modify)
		self.exit_button.clicked.connect(self.exit)

		self.url = url
		self.user = user

		# Set UserName and Password displays
		self.url_display.setText(url)
		self.url_display.setReadOnly(True)

		self.user_display.setText(user)
		self.user_display.setReadOnly(True)


	def check_if_empty_string(self, url='null', user='null', password='null'):
		if not url or not url.strip() or not user or not user.strip() or not password or not password.strip():
			return True


	def modify(self):
		modify_url = str(self.url_display.text())
		modify_user = str(self.user_display.text())
		modify_password = str(self.password_input.text())

		if self.check_if_empty_string(modify_url, modify_user, modify_password):
			QtGui.QMessageBox.warning(
				self, "Invalid Entry", "Make sure you input a password.")
		else:
			new = session.query(Locker).filter_by(url=self.url,user=self.user).one()
			new.url = modify_url
			new.user = modify_user
			new.password = modify_password
			session.commit()
			QtGui.QMessageBox.information(self, "Completed", "Succesfully Updated \n URL:[{}] \n USER:[{}] \n PASSWORD:[{}]".format(modify_url, modify_user, (len(modify_password) * '*')))
			self.exit()

	def clear_input(self):
		#Clears input text area
		self.url_display.clear()
		self.user_display.clear()

	def exit(self):
		#Set displays to editable so when window reopens the displays are accurate
		self.clear_input()
		self.url_display.setReadOnly(False)
		self.user_display.setReadOnly(False)
		self.close()

class DeletePage(QtGui.QDialog, delete_page):
	"""Window for whenever the user wishes to delete an existing entry"""

	def __init__(self, url, user, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)

		# Button Actions
		self.delete_button.clicked.connect(self.delete)
		self.exit_button.clicked.connect(self.exit)

		self.url = url
		self.user = user

		#Display URL and USER selections and set to readonly
		self.url_delete_display.setText(url)
		self.url_delete_display.setReadOnly(True)

		self.user_delete_display.setText(user)
		self.user_delete_display.setReadOnly(True)

	def delete(self):
		session.query(Locker).filter_by(url=self.url,user=self.user).delete()
		session.commit()
		QtGui.QMessageBox.information(self,"Deleted","Sucessfully Deleted \n URL:[{}] \n USER:[{}]".format(self.url,self.user))
		self.close()

	def clear_input(self):
		#Clears input text area
		self.url_delete_display.clear()
		self.user_delete_display.clear()

	def exit(self):
		#Set displays to editable so when window reopens the displays are accurate
		self.clear_input()
		self.url_delete_display.setReadOnly(False)
		self.user_delete_display.setReadOnly(False)
		self.close()

class AboutPage(QtGui.QDialog, about_page):
	"""The 'about' window"""

	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	gui = MainWindow()
	gui.show()
	gui.refresh()
	app.exec_()
