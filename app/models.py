from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    sent_messages = relationship("Message", foreign_keys="[Message.sender_id]", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="[Message.recipient_id]", back_populates="recipient")
    group_memberships = relationship("GroupMembership", back_populates="user")

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    messages = relationship("GroupMessage", back_populates="group")
    members = relationship("GroupMembership", back_populates="group")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    recipient_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    recipient = relationship("User", foreign_keys=[recipient_id], back_populates="received_messages")

class GroupMessage(Base):
    __tablename__ = "group_messages"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    group = relationship("Group", back_populates="messages")
    sender = relationship("User")

class GroupMembership(Base):
    __tablename__ = "group_memberships"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    is_admin = Column(Boolean, default=False)

    group = relationship("Group", back_populates="members")
    user = relationship("User", back_populates="group_memberships")
