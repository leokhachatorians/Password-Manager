# Password-Manager
A simple password manager backed by SQLite and PyQt4

Allows the creation and storage of user logins according to three parameters: [WEBSITE] [ACCOUNT] [PASSWORD].

##Features:           			
* User is unable to add information wherin the [Website] and the [Account] already exist in the database
* Right clicking on an existing cell will allow the option to [Modify], [Delete], or [View Password] that respective
  row.
* Allows the ability to [Add New] and [View All Passwords] in the dropdown menu.
  
##Things to do:
* Allow the implementation of modifying individual components of a selected login.
* Some form of security implementation, such as access only through an encrypted master password.
  
  
##Notes:
* Please note that there is absolutely no security yet implemented, don't use this in place of an actually secure password manager.
* Pressing refresh will hide any and all passwords shown. 
