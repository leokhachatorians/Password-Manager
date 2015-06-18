from sqlalchemy import create_engine, Column, Integer, String, Sequence, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///user_accounts.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Accounts(Base):
	__tablename__ = 'accounts'

	id = Column(Integer, Sequence('account_id_seq'), primary_key=True)
	account = Column(String(60))
	password = Column(String(60))

	def __repr__(self):
		return "<Accounts(account={}, password={}>".format(account,password)

Base.metadata.create_all(engine)
