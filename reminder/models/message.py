from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Date
from sqlalchemy.orm import relationship, backref

from reminder.models.base import Base


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    reminder_id = Column(Integer, ForeignKey("reminder.id"))
    sending_time = Column(DateTime, nullable=False)
    sent_time = Column(DateTime)
    random_id = Column(String)
    response_date = Column(String)
    sent = Column(Integer)
    reminder = relationship("Reminder", backref=backref("messages", cascade="all, delete-orphan"))

    def __init__(self, reminder, sending_time, sent_time=None, random_id=None, response_date=None, sent=0):
        self.reminder = reminder
        self.sending_time = sending_time
        self.sent_time = sent_time
        self.random_id = random_id
        self.response_date = response_date
        self.sent = sent
