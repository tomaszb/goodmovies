from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class dbMan:
	def dbConnect(self):
		engine = create_engine("postgresql+psycopg2://tomaszb:deadbeef5@/goodmovies")
		connection = engine.connect()
		Session = sessionmaker(bind = engine)
		self.session = Session()

	def saveMovie(self, title, imdb = 0, meta = 0, rotten = 0):
		movie = Movie(name=title, imdbrating=imdb, metacritic=meta, rottentomatoes=rotten)
		self.session.add(movie)
		self.session.commit()

	def returnMovie(self, title):
		movie = self.session.query(Movie).filter_by(name=title).first()
		return movie

class Movie(Base):
	__tablename__ = 'movies'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	imdbrating = Column(Integer)
	metacritic = Column(Integer)
	rottentomatoes = Column(Integer)

	def __repr__(self):
		return "<Movie(name='%s', imdbrating='%i', metacritic='%i')>" % (self.name,
			self.imdbrating,self.metacritic)



def createDatabase(engine):
	Base.metadata.create_all(engine) 