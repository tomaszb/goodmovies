from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

class dbMan:
	def dbConnect(self):
		database_url = os.environ["DATABASE_URL"]
		engine = create_engine(database_url, echo=True)
		connection = engine.connect()
		Session = sessionmaker(bind = engine)
		self.session = Session()

	def saveMovie(self, title, imdbfloat = 0, meta = 0, rotten = 0):
		imdb = int(imdbfloat*10)
		movie = Movie(name=title, imdbrating=imdb, metacritic=meta, rottentomatoes=rotten)
		self.session.add(movie)
		self.session.commit()

	def returnMovie(self, title):
		movie = self.session.query(Movie).filter_by(name=title).first()
		return movie

	def deleteMovies(self):
		for item in db.session.query(Movie).order_by(Movie.id):
			self.session.delete(item)

		self.session.commit()

	def returnAll(self):
		self.session.query(Movie).all()

	def dbDC(self):
		self.session.close()

class Movie(Base):
	__tablename__ = 'movies'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	imdbrating = Column(Integer)
	metacritic = Column(Integer)
	rottentomatoes = Column(Integer)

	def __repr__(self):
		return "<Movie(name=u'%s', imdbrating='%i', metacritic='%i')>" % (self.name,
			self.imdbrating,self.metacritic)



def createDatabase(engine):
	Base.metadata.create_all(engine) 