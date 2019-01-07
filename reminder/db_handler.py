import csv
import datetime
import os

import jdatetime
from khayyam import JalaliDate
from reminder.models.base import Session
from reminder.models.constants import Attr, ReadyText, MessageStatus
from reminder.models.message import Message
from reminder.models.reminder import Reminder
from reminder.models.receipt import Receipt

session = Session()


def add_reminder_to_db(reminder):
    print(reminder)
    reminder_obj = Reminder(reminder.get(Attr.peer_id), reminder.get(Attr.peer_access_hash),
                            reminder.get(Attr.type), reminder.get(Attr.card_number),
                            reminder.get(Attr.money_amount),
                            reminder.get(Attr.text), reminder.get(Attr.file_id),
                            reminder.get(Attr.file_access_hash),
                            reminder.get(Attr.file_size))
    session.add(reminder_obj)

    date = reminder.get(Attr.date)
    time = reminder.get(Attr.time)
    print(type(date), date)
    print(type(time), time)
    remind_datetime = datetime.datetime.combine(date, time)
    if reminder.get(Attr.periodic_type) != ReadyText.monthly:
        time_delta = time_delta_func(reminder.get(Attr.periodic_type))
        for i in range(reminder[Attr.iterate_number] + 1):
            message = Message(reminder_obj, sending_time=(remind_datetime + time_delta * i))
            session.add(message)
    else:
        time_delta = time_delta_func(reminder.get(Attr.periodic_type))
        for i in range(reminder[Attr.iterate_number] + 1):
            s_date = remind_datetime + time_delta * i
            day = remind_datetime.day
            sending_time = None
            is_valid_date = False
            while is_valid_date is False:
                is_valid_date = True
                try:
                    sending_time = JalaliDate(s_date.year, s_date.month, day)
                except ValueError:
                    is_valid_date = False
                day -= 1
            message = Message(reminder_obj, sending_time=sending_time.todate())
            session.add(message)
    session.commit()


def time_delta_func(date_type):
    return {
        ReadyText.daily: datetime.timedelta(days=1),
        ReadyText.weekly: datetime.timedelta(weeks=1),
        ReadyText.monthly: datetime.timedelta(days=30),
        None: datetime.timedelta(days=0)
    }[date_type]


def generate_receipt_report(peer_id):
    if not os.path.exists("files"):
        os.mkdir("files")
    with open('files/{}.csv'.format(peer_id), 'w') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        records = session.query(Receipt).join(Message).join(Reminder).filter(
            Reminder.peer_id == peer_id
        ).all()
        rs = []
        for record in records:
            rs.append((record.payer, record.receiver, record.message.notification.text,
                       record.message.notification.card_number, record.message.notification.money_amount,
                       jdatetime.datetime.fromgregorian(datetime=record.purchasing_time),
                       jdatetime.datetime.fromgregorian(datetime=record.message.sent_time),
                       record.is_expenditure, record.description, record.status, record.traceNo))
        header = (
            "نام واریز کننده", "شماره رسید", "متن", "شماره کارت مقصد", "مبلغ", "زمان پرداخت", "purchaseMessageTime",
            "isExpenditure", "توضیحات", "وضعیت", "شماره پیگیری")
        writer.writerow(header)
        for r in rs:
            writer.writerow(r)


def add_receipt(purchase_message_date, payer, receiver, is_expenditure, status, trace_no, description, random_id):
    purchased_message = session.query(Message).filter(
        Message.response_date == purchase_message_date).filter(
        Message.random_id == random_id).one()
    current_time = datetime.datetime.today()
    receipt = Receipt(purchased_message, payer, receiver, is_expenditure, current_time, status, trace_no, description)
    session.add(receipt)
    session.commit()


def messages_tobe_sent():
    result = session.query(Message).filter(Message.sent != MessageStatus.sent).filter(
        Message.sending_time == datetime.datetime.now().strftime("%Y-%m-%d %H:%M")).all()
    return result


def make_message_sent(message, random_id, response_date):
    message.random_id = random_id
    message.response_date = response_date
    message.sent_time = datetime.datetime.now()
    message.sent = MessageStatus.sent
    session.commit()


def make_message_failed_sent(message):
    message.sent = MessageStatus.failed
    session.commit()
