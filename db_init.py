from sqlalchemy import create_engine, Column, Integer, String, Sequence, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///passwords.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Locker(Base):
	__tablename__ = 'locker'

	id = Column(Integer, Sequence('website_id_seq'), primary_key=True)
	url = Column(String(60))
	user = Column(String(60))
	password = Column(String(60))
	account = Column(String(60))

	def __repr__(self):
		return "<Website(url={}, user={}, password={}, account={}>".format(url, user, password, account)

class Accounts(Base):
	__tablename__ = 'accounts'

	id = Column(Integer, Sequence('account_id_seq'), primary_key=True)
	account = Column(String(60))
	password = Column(String(60))

	def __repr__(self):
		return "<Accounts(account={}, password={}>".format(account,password)

Base.metadata.create_all(engine)