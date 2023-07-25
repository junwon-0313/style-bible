from passlib.context import CryptContext
from sqlalchemy import (ARRAY, CHAR, Boolean, Column, DateTime, ForeignKey,
                        Integer, String)
from sqlalchemy.orm import relationship

from .database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    user_pwd = Column(String)
    signup_time = Column(DateTime)

    likes = relationship("Like", back_populates="user")
    clicks = relationship("Click", back_populates="user")
    session = relationship("UserSession", back_populates="user")


class Outfit(Base):
    __tablename__ = "outfit"

    outfit_id = Column(Integer, primary_key=True, index=True)
    img_url = Column(String)
    gender = Column(CHAR)
    age = Column(Integer)
    origin_url = Column(String)
    reporter = Column(String)
    tags = Column(ARRAY(String))
    brands = Column(ARRAY(String))
    region = Column(String)
    occupation = Column(String)
    style = Column(String)
    date = Column(DateTime, nullable=False)
    # for style category 
    default = Column(Integer)
    season_1 = Column(Integer)
    season_2 = Column(Integer)

    likes = relationship("Like", back_populates="outfit")
    clicks = relationship("Click", back_populates="outfit")
    similars = relationship("Similar", back_populates="outfit")


class Like(Base):
    __tablename__ = "like"

    like_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("session.session_id"))
    user_id = Column(Integer, ForeignKey("user.user_id"), default=None)
    outfit_id = Column(Integer, ForeignKey("outfit.outfit_id"))
    timestamp = Column(DateTime, nullable=False)
    like_type = Column(String, default="unknown")
    is_deleted = Column(Boolean, default=False)
    as_login = Column(Boolean)

    user = relationship("User", back_populates="likes")
    outfit = relationship("Outfit", back_populates="likes")
    session = relationship("UserSession", back_populates="likes")


# Not using
class Click(Base):
    __tablename__ = "click"

    click_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("session.session_id"))
    user_id = Column(Integer, ForeignKey("user.user_id"))
    outfit_id = Column(Integer, ForeignKey("outfit.outfit_id"))
    click_type = Column(String)
    timestamp = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="clicks")
    outfit = relationship("Outfit", back_populates="clicks")
    session = relationship("UserSession", back_populates="clicks")


class Similar(Base):
    __tablename__ = "similar"

    outfit_id = Column(
        Integer, ForeignKey("outfit.outfit_id"), primary_key=True, index=True
    )
    similar_outfits = Column(ARRAY(Integer))

    outfit = relationship("Outfit", back_populates="similars")


class UserSession(Base):
    __tablename__ = "session"

    # user_session_pk = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), default=None)
    created_at = Column(DateTime)
    login_at = Column(DateTime, default=None)
    expired_at = Column(DateTime, default=None)

    user = relationship("User", back_populates="session")
    likes = relationship("Like", back_populates="session")
    clicks = relationship("Click", back_populates="session")
