from db_init import session, Locker
import sys
from PyQt4 import QtCore, QtGui, uic
import classes.entry_viewer_class

add_page = uic.loadUiType("pages/password_add_page.ui")[0]

class AddEntry(QtGui.QDialog, add_page):
	"""Window for whenever the user wishes to add something to the database"""

	def __init__(self, account, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)

		# Button Actions
		self.save_button.clicked.connect(self.add)
		self.exit_button.clicked.connect(self.exit)

		# Account holder
		self.account = account

		# Window state for entry viewer
		self.entry_viewer_window = None

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
		elif session.query(Locker).filter_by(url=add_url, user=add_user, account=self.account).count() >= 1:
			QtGui.QMessageBox.warning(
				self, "Invalid Entry", " URL:[{}] \n USER:[{}] \n Already exists!".format(add_url, add_user))
		else:
			session.add(Locker(url=add_url,
							   user=add_user,
							   password=add_password,
							   account=self.account))
			session.commit()
			QtGui.QMessageBox.information(self, "Completed", "Succesfully Saved \n URL:[{}] \n USER:[{}] \n PASSWORD:[{}]".format(
				add_url, add_user, (len(add_password) * '*')))

			self.exit()

	def exit(self):
		#Run clear input prior to exiting ensure clean window
		self.website_input.clear()
		self.account_input.clear()
		self.password_input.clear()
		self.reload_viewer()
		self.close()

	def reload_viewer(self):
		if self.entry_viewer_window is None:
			self.entry_viewer_window = classes.entry_viewer_class.EntryViewer(self.account)
		self.entry_viewer_window.refresh()
		self.entry_viewer_window.show()