import os

from balebot.models.constants.file_type import FileType
from balebot.models.messages import DocumentMessage, TextMessage
from reminder.db_handler import make_message_sent, make_message_failed_sent
from reminder.models.constants import UserData, LogText, Attr, ReadyText, MimeType, SendingAttempt, Step
from main_config import BotConfig


def success_send_message(response, user_data):
    user_data = user_data[UserData.kwargs]
    user_peer = user_data[UserData.user_peer]
    step_name = user_data[UserData.step_name]
    my_logger = user_data[UserData.logger]
    my_logger.info(LogText.successful_step_message_sending,
                   extra={UserData.user_id: user_peer.peer_id, UserData.step_name: step_name, "tag": "info"})


def failure_send_message(response, user_data):
    user_data = user_data[UserData.kwargs]
    user_peer = user_data[UserData.user_peer]
    step_name = user_data[UserData.step_name]
    my_logger = user_data[UserData.logger]
    bot = user_data[UserData.bot]
    message = user_data[UserData.message]
    user_data[UserData.attempt] += 1
    if user_data[UserData.attempt] < BotConfig.resending_max_try:
        bot.send_message(message, user_peer, success_send_message, failure_send_message)
        return
    my_logger.error(LogText.failed_step_message_sending,
                    extra={UserData.user_id: user_peer.peer_id, UserData.step_name: step_name, "tag": "info"})


def receipt_report_success(response, user_data):
    user_data = user_data[UserData.kwargs]
    my_logger = user_data[UserData.logger]
    my_logger.info(LogText.successful_report_sending,
                   extra={UserData.user_id: user_data[UserData.user_peer].peer_id, "tag": "info"})


def receipt_report_failure(response, user_data):
    user_data = user_data[UserData.kwargs]
    my_logger = user_data[UserData.logger]
    bot = user_data[UserData.bot]
    user_data[UserData.report_attempt] += 1
    if user_data[UserData.report_attempt] <= BotConfig.resending_max_try:
        bot.send_message(user_data[UserData.doc_message], user_data[UserData.user_peer],
                         success_callback=receipt_report_success,
                         failure_callback=receipt_report_failure, kwargs=user_data)
        return
    my_logger.error(LogText.failed_report_sending,
                    extra={UserData.user_id: user_data[UserData.user_peer].peer_id, "tag": "info"})


def file_upload_success(result, user_data):
    file_id = str(user_data.get(Attr.file_id, None))
    file_url = str(user_data.get(Attr.url))
    access_hash = str(user_data.get(Attr.user_id, None))
    user_data = user_data[UserData.kwargs]
    user_peer = user_data[UserData.user_peer]
    my_logger = user_data[UserData.logger]
    bot = user_data[UserData.bot]

    my_logger.info(LogText.successful_report_upload,
                   extra={UserData.user_id: user_peer.peer_id, UserData.file_url: file_url})
    file_size = os.path.getsize('files/{}.csv'.format(user_peer.peer_id))
    doc_message = DocumentMessage(file_id=file_id, access_hash=access_hash, name=BotConfig.receipts_report_name,
                                  file_size=file_size, mime_type=MimeType.csv,
                                  caption_text=TextMessage(text=ReadyText.receipts_report))
    kwargs = {UserData.user_peer: user_peer, UserData.doc_message: doc_message,
              UserData.report_attempt: SendingAttempt.first, UserData.logger: my_logger, UserData.bot: bot}
    bot.send_message(doc_message, user_peer, success_callback=receipt_report_success,
                     failure_callback=receipt_report_failure, kwargs=kwargs)


def file_upload_failure(result, user_data):
    user_data = user_data[UserData.kwargs]
    user_peer = user_data[UserData.user_peer]
    my_logger = user_data[UserData.logger]
    bot = user_data[UserData.bot]
    upload_attempt = user_data[UserData.attempt]
    upload_attempt += 1
    if upload_attempt <= BotConfig.re_uploading_max_try:
        kwargs = {UserData.user_peer: user_peer,
                  UserData.attempt: upload_attempt, UserData.logger: my_logger, UserData.bot: bot}
        bot.upload_file(file="files/{}.csv".format(user_peer.peer_id), file_type=FileType.file,
                        success_callback=file_upload_success,
                        failure_callback=file_upload_failure, kwargs=kwargs)
        return
    message = TextMessage(ReadyText.upload_failed)
    kwargs = {UserData.user_peer: user_peer, UserData.message: message, UserData.step_name: Step.upload_fail,
              UserData.attempt: SendingAttempt.first, UserData.logger: my_logger, UserData.bot: bot}
    bot.send_message(message, user_peer, success_send_message, failure_send_message, kwargs=kwargs)
    my_logger.error(LogText.failed_report_upload,
                    extra={UserData.user_id: user_peer.peer_id})


def reminder_success(response, user_data):
    user_data = user_data[UserData.kwargs]
    msg = user_data[UserData.db_msg]
    msg_sending_time = msg.sending_time
    my_logger = user_data[UserData.logger]
    user_id = user_data[UserData.user_peer].peer_id
    sending_attempt = user_data[UserData.sending_attempt]
    make_message_sent(msg, user_data[UserData.random_id], response.body.date)
    my_logger.info(LogText.successful_sending,
                   extra={UserData.user_id: user_id, UserData.sending_attempt: sending_attempt,
                          UserData.sending_set_time: msg_sending_time, "tag": "info"})


def reminder_failure(response, user_data):
    user_data = user_data[UserData.kwargs]
    user_peer = user_data[UserData.user_peer]
    my_logger = user_data[UserData.logger]
    send_message = user_data[UserData.send_message]
    base_message = user_data[UserData.base_message]
    sending_attempt = user_data[UserData.sending_attempt] + 1
    msg = user_data[UserData.db_msg]
    msg_sending_time = msg.sending_time
    msg_notification_type = msg.notification.type
    if sending_attempt <= BotConfig.resending_max_try:
        send_message(base_message, user_peer, msg, sending_attempt)
        return
    make_message_failed_sent(msg)
    my_logger.error(LogText.failed_sending,
                    extra={UserData.user_peer: user_peer.peer_id, UserData.message_id: msg.id,
                           UserData.message_type: msg_notification_type,
                           UserData.sending_set_time: msg_sending_time, "tag": "info"})
