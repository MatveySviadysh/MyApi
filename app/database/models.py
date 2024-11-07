import datetime
from sqlalchemy import Column, Date, DateTime, Float, Integer, String, ForeignKey, Text  
from sqlalchemy.orm import relationship
from database.connect import Base 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)

    posts = relationship("Post", back_populates="author") 
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    

class Travel(Base):
    __tablename__ = 'travels'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    duration = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    image_url = Column(String, nullable=True)
    
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    city = relationship("City", back_populates="travels")

    guide_id = Column(Integer, ForeignKey('tour_guides.id'), nullable=True)
    guide = relationship("TourGuide", back_populates="travels")

    orders = relationship("Order", back_populates="travel")
    reviews = relationship("Review", back_populates="travel")

class TourGuide(Base):
    __tablename__ = 'tour_guides'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    experience_years = Column(Integer, nullable=True)
    bio = Column(Text, nullable=True)
    contact_info = Column(String, nullable=True)
    
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    city = relationship("City", back_populates="tour_guides")
    
    travels = relationship("Travel", back_populates="guide")

class City(Base):
    __tablename__ = 'cities'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)

    travels = relationship("Travel", back_populates="city")
    tour_guides = relationship("TourGuide", back_populates="city")  



class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    travel_id = Column(Integer, ForeignKey('travels.id'), nullable=False)
    order_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    status = Column(String, default="в ожидании", nullable=False)
    
    user = relationship("User", back_populates="orders")
    travel = relationship("Travel", back_populates="orders")

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    travel_id = Column(Integer, ForeignKey('travels.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    
    user = relationship("User", back_populates="reviews")
    travel = relationship("Travel", back_populates="reviews")

    
# class Post(Base):
#     __tablename__ = "posts"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     text = Column(String)
#     author_id = Column(Integer, ForeignKey("users.id"))

#     author = relationship("User", back_populates="posts")