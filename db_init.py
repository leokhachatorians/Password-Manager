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

	def __repr__(self):
		return "<Website(url={}, user={}, password={}>".format(url,user,password)

Base.metadata.create_all(engine)
