import datetime

from khayyam import JalaliDate
from balebot.filters import *
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.base_models import UserPeer
from balebot.models.messages import *
from balebot.models.messages.banking.money_request_type import MoneyRequestType
from balebot.utils.logger import Logger
from balebot.utils.util_functions import generate_random_id, arabic_to_eng_number
from reminder.models.bot import Bot
from reminder.callbacks import *
from reminder.db_handler import generate_receipt_report, add_reminder_to_db, add_receipt, messages_tobe_sent
from reminder.models.constants import Command, ReadyText, SendingAttempt, ReminderType, \
    MimeType, TransferInfo, MsgUID, LogText, UserData, Step, Attr, Value, Pattern, DefaultPhoto

my_logger = Logger.get_logger()
reminder_bot = Bot()
loop = reminder_bot.loop
updater = reminder_bot.updater
dispatcher = reminder_bot.dispatcher

main_menu = [TemplateMessageButton(ReadyText.add_reminder, ReadyText.add_reminder, 0),
             TemplateMessageButton(ReadyText.show_receipts, ReadyText.show_receipts, 0),
             TemplateMessageButton(ReadyText.help_me, ReadyText.help_me, 0)]


######################### conversation ##############################
@dispatcher.command_handler([Command.start])
def start(bot, update):
    dispatcher.conversation_data.clear()
    general_message = TextMessage(ReadyText.service_selection)
    message = TemplateMessage(general_message=general_message, btn_list=main_menu)
    kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: Step.conversation_starter,
              UserData.message: message, UserData.attempt: SendingAttempt.first,
              UserData.logger: my_logger, UserData.bot: bot}
    bot.respond(update, message, success_callback=success_send_message, failure_callback=failure_send_message,
                kwargs=kwargs)
    dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[ReadyText.show_receipts]))
def receipts(bot, update):
    user = update.get_effective_user()
    generate_receipt_report(user.peer_id)
    upload_attempt = 1
    kwargs = {UserData.user_peer: update.get_effective_user(),
              UserData.attempt: upload_attempt, UserData.logger: my_logger, UserData.bot: bot}
    bot.upload_file(file="files/{}.csv".format(user.peer_id), file_type=FileType.file,
                    success_callback=file_upload_success, failure_callback=file_upload_failure, kwargs=kwargs)
    dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[ReadyText.help_me]))
def help_me(bot, update):
    message = TextMessage(ReadyText.help)
    kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: Step.showing_guide,
              UserData.message: message, UserData.attempt: SendingAttempt.first, UserData.logger: my_logger,
              UserData.bot: bot}
    bot.respond(update, message, success_callback=success_send_message, failure_callback=failure_send_message,
                kwargs=kwargs)
    dispatcher.finish_conversation(update)


def validate_time(input_time, input_date):
    try:
        time_format = '%H:%M'
        time = datetime.datetime.strptime(input_time, time_format)
        time = time.time().strftime(time_format)
        now_time = datetime.datetime.now().strftime(time_format)
        if input_date == JalaliDate().today() and time <= now_time:
            message = TextMessage(ReadyText.time_is_past)
            return False, message
        time = datetime.datetime.strptime(time, time_format)
        time = time.time()
        return time, None
    except:
        message = TextMessage(ReadyText.wrong_format)
        return False, message


def validate_date(input_date):
    try:
        input_date = arabic_to_eng_number(input_date)
        date = JalaliDate().strptime(input_date, "%Y%m%d")
        if date < JalaliDate().today():
            message = TextMessage(ReadyText.time_is_past)
            return False, message
        date = date.todate()
        return date, None
    except:
        message = TextMessage(ReadyText.wrong_format)
        return False, message


ADD_REMINDER, SET_TIME, SET_DATE, \
NUMBER_OF_REPETITIONS, REMINDER_TYPE, REMINDER_CARD_NUMBER, \
REMINDER_AMOUNT, REMINDER_PICTURE, REMINDER_TEXT, SKIP_PHOTO = range(10)

current_state = "current_state"


@dispatcher.message_handler(TemplateResponseFilter(keywords=[ReadyText.add_reminder]))
def add_reminder(bot, update):
    state = dispatcher.get_conversation_data(update, current_state)
    if state == ADD_REMINDER:
        message = TextMessage(ReadyText.wrong_format)
    else:
        message = TextMessage(ReadyText.enter_reminder_date)
    kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: Step.ask_time,
              UserData.message: message, UserData.attempt: SendingAttempt.first,
              UserData.logger: my_logger, UserData.bot: bot}
    bot.respond(update, message, success_send_message, failure_send_message, kwargs=kwargs)
    dispatcher.set_conversation_data(update, current_state, ADD_REMINDER)
    dispatcher.register_conversation_next_step_handler(update, common_handlers + [
        MessageHandler(TextFilter(), set_time),
        MessageHandler(DefaultFilter(), add_reminder)])


def set_time(bot, update):
    state = dispatcher.get_conversation_data(update, current_state)
    if state == ADD_REMINDER:
        input_date = update.get_effective_message().text
        result, message = validate_date(input_date)
        if result:
            dispatcher.set_conversation_data(update, Attr.date, result)
            general_message = TextMessage(ReadyText.enter_reminder_time)
            btn_list = [TemplateMessageButton(ReadyText.default_time, ReadyText.default_time_value, 0)]
            message = TemplateMessage(general_message=general_message, btn_list=btn_list)
            kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: Step.period_type,
                      UserData.message: message, UserData.attempt: SendingAttempt.first, UserData.logger: my_logger,
                      UserData.bot: bot}
            bot.respond(update, message, success_send_message, failure_send_message, kwargs=kwargs)
            dispatcher.set_conversation_data(update, current_state, SET_TIME)
            dispatcher.register_conversation_next_step_handler(update, common_handlers + [
                MessageHandler(TextFilter(), set_date),
                MessageHandler(TemplateResponseFilter(keywords=[ReadyText.default_time_value]), set_date),
                MessageHandler(DefaultFilter(), set_time)])
        else:
            kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: Step.ask_time,
                      UserData.message: message, UserData.attempt: SendingAttempt.first,
                      UserData.logger: my_logger, UserData.bot: bot}
            bot.respond(update, message, success_send_message, failure_send_message, kwargs=kwargs)
            dispatcher.set_conversation_data(update, current_state, ADD_REMINDER)
            dispatcher.register_conversation_next_step_handler(update, common_handlers + [
                MessageHandler(TextFilter(), set_time),
                MessageHandler(DefaultFilter(), add_reminder)])
    else:
        message = TextMessage(ReadyText.wrong_format)
        kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: Step.ask_time,
                  UserData.message: message, UserData.attempt: SendingAttempt.first,
                  UserData.logger: my_logger, UserData.bot: bot}
        bot.respond(update, message, success_send_message, failure_send_message, kwargs=kwargs)
        dispatcher.set_conversation_data(update, current_state, SET_TIME)
        dispatcher.register_conversation_next_step_handler(update, common_handlers + [
            MessageHandler(TextFilter(), set_date),
            MessageHandler(DefaultFilter(), set_time)])


def set_date(bot, update):
    state = dispatcher.get_conversation_data(update, current_state)
    if state == SET_TIME:
        input_time = update.get_effective_message().text
        input_date = dispatcher.get_conversation_data(update, Attr.date)
        result, message = validate_time(input_time, input_date)
        if result:
            dispatcher.set_conversation_data(update, Attr.time, result)
            general_message = TextMessage(ReadyText.periodic_type_selection)
            btn_list = [TemplateMessageButton(ReadyText.only_once, ReadyText.only_once, 0),
                        TemplateMessageButton(ReadyText.daily, ReadyText.daily, 0),
                        TemplateMessageButton(ReadyText.weekly, ReadyText.weekly, 0),
                        TemplateMessageButton(ReadyText.monthly, ReadyText.monthly, 0)]
            message = TemplateMessage(general_message=general_message, btn_list=btn_list)
            kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: Step.period_type,
                      UserData.message: message, UserData.attempt: SendingAttempt.first, UserData.logger: my_logger,
                      UserData.bot: bot}
            bot.respond(update, message, success_send_message, failure_send_message, kwargs=kwargs)
            dispatcher.set_conversation_data(update, current_state, SET_DATE)
            dispatcher.register_conversation_next_step_handler(update, common_handlers + [
                MessageHandler(TemplateResponseFilter(keywords=[ReadyText.only_once]), reminder_type),
                MessageHandler(TemplateResponseFilter(keywords=[ReadyText.daily, ReadyText.weekly, ReadyText.monthly]),
                               number_of_repetitions),
                MessageHandler(DefaultFilter(), set_date)])
        else:
            kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: Step.ask_time,
                      UserData.message: message, UserData.attempt: SendingAttempt.first,
                      UserData.logger: my_logger, UserData.bot: bot}
            bot.respond(update, message, success_send_message, failure_send_message, kwargs=kwargs)
            dispatcher.set_conversation_data(update, current_state, SET_TIME)
            dispatcher.register_conversation_next_step_handler(update, common_handlers + [
                MessageHandler(TextFilter(), set_date),
                MessageHandler(TemplateResponseFilter(keywords=[ReadyText.default_time_value]), set_date),
                MessageHandler(DefaultFilter(), set_time)])
    else:
        message = TextMessage(ReadyText.wrong_answer)
        kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: Step.period_type,
                  UserData.message: message, UserData.attempt: SendingAttempt.first, UserData.logger: my_logger,
                  UserData.bot: bot}
        bot.respond(update, message, success_send_message, failure_send_message, kwargs=kwargs)
        dispatcher.set_conversation_data(update, current_state, SET_DATE)
        dispatcher.register_conversation_next_step_handler(update, common_handlers + [
            MessageHandler(TemplateResponseFilter(keywords=[ReadyText.only_once]), reminder_type),
            MessageHandler(TemplateResponseFilter(keywords=[ReadyText.daily, ReadyText.weekly, ReadyText.monthly]),
                           number_of_repetitions),
            MessageHandler(DefaultFilter(), set_date)])


def number_of_repetitions(bot, update):
    state = dispatcher.get_conversation_data(update, current_state)
    if state == SET_DATE:
        message = update.get_effective_message()
        dispatcher.set_conversation_data(update, Attr.periodic_type, message.text)
        message = TextMessage(ReadyText.iterate_number_selection)
    else:
        message = TextMessage(ReadyText.wrong_answer_pls_enter_number)
    kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: Step.ask_iterate_number,
              UserData.message: message, UserData.attempt: SendingAttempt.first, UserData.logger: my_logger,
              UserData.bot: bot}
    bot.respond(update, message, success_send_message, failure_send_message, kwargs=kwargs)
    dispatcher.set_conversation_data(update, current_state, NUMBER_OF_REPETITIONS)
    dispatcher.register_conversation_next_step_handler(update, common_handlers + [
        MessageHandler(TextFilter(pattern=Pattern.number), reminder_type),
        MessageHandler(DefaultFilter(), number_of_repetitions)])


def reminder_type(bot, update):
    state = dispatcher.get_conversation_data(update, current_state)
    if state == NUMBER_OF_REPETITIONS or state == SET_DATE:
        if not dispatcher.conversation_data.get(Attr.periodic_type):
            dispatcher.set_conversation_data(update, Attr.iterate_number, 0)
        else:
            message = update.get_effective_message()
            dispatcher.set_conversation_data(update, Attr.iterate_number, int(message.text))
        general_message = TextMessage(ReadyText.notification_type_selection)
        btn_list = [TemplateMessageButton(ReadyText.debt, ReadyText.debt, 0),
                    TemplateMessageButton(ReadyText.normal, ReadyText.normal, 0)]
        message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    else:
        message = TextMessage(ReadyText.wrong_answer)
    kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: Step.ask_type,
              UserData.message: message, UserData.attempt: SendingAttempt.first, UserData.logger: my_logger,
              UserData.bot: bot}
    bot.respond(update, message, success_callback=success_send_message, failure_callback=failure_send_message,
                kwargs=kwargs)
    dispatcher.set_conversation_data(update, current_state, REMINDER_TYPE)
    dispatcher.register_conversation_next_step_handler(update, common_handlers + [
        MessageHandler(TemplateResponseFilter(keywords=[ReadyText.normal]), reminder_picture),
        MessageHandler(TemplateResponseFilter(keywords=[ReadyText.debt]), reminder_card_number),
        MessageHandler(DefaultFilter(), reminder_type)])


def reminder_card_number(bot, update):
    state = dispatcher.get_conversation_data(update, current_state)
    if state == REMINDER_TYPE:
        dispatcher.set_conversation_data(update, Attr.type, ReminderType.debt)
        message = TextMessage(ReadyText.card_number_entering)
    else:
        message = TextMessage(ReadyText.wrong_card_number)
    kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: Step.ask_card_number,
              UserData.message: message, UserData.attempt: SendingAttempt.first, UserData.logger: my_logger,
              UserData.bot: bot}
    bot.respond(update, message, success_send_message, failure_send_message, kwargs=kwargs)
    dispatcher.set_conversation_data(update, current_state, REMINDER_CARD_NUMBER)
    dispatcher.register_conversation_next_step_handler(update, common_handlers + [
        MessageHandler(TextFilter(pattern=Pattern.card_number), reminder_amount),
        MessageHandler(DefaultFilter(), reminder_card_number)])


def reminder_amount(bot, update):
    state = dispatcher.get_conversation_data(update, current_state)
    if state == REMINDER_CARD_NUMBER:
        dispatcher.set_conversation_data(update, Attr.card_number, update.get_effective_message().text)
        message = TextMessage(ReadyText.amount_entering)
    else:
        message = TextMessage(ReadyText.wrong_answer_pls_enter_number)
    kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: Step.ask_amount,
              UserData.message: message, UserData.attempt: SendingAttempt.first, UserData.logger: my_logger,
              UserData.bot: bot}
    bot.respond(update, message, success_send_message, failure_send_message, kwargs=kwargs)
    dispatcher.set_conversation_data(update, current_state, REMINDER_AMOUNT)
    dispatcher.register_conversation_next_step_handler(update, common_handlers + [
        MessageHandler(TextFilter(pattern=Pattern.money_amount), reminder_picture),
        MessageHandler(DefaultFilter(), reminder_amount)])


def reminder_picture(bot, update):
    state = dispatcher.get_conversation_data(update, current_state)
    if state == REMINDER_AMOUNT or state == REMINDER_TYPE:
        if ReminderType.debt == dispatcher.get_conversation_data(update, Attr.type):
            dispatcher.set_conversation_data(update, Attr.money_amount, update.get_effective_message().text)
        else:
            dispatcher.set_conversation_data(update, Attr.type, ReminderType.normal)
        message = TemplateMessage(TextMessage(ReadyText.picture_request),
                                  [TemplateMessageButton(ReadyText.no_picture_needed, ReadyText.no_picture_needed, 0)])
    else:
        message = TemplateMessage(TextMessage(ReadyText.wrong_answer),
                                  [TemplateMessageButton(ReadyText.no_picture_needed, ReadyText.no_picture_needed, 0)])
    kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: UserData.ask_picture,
              UserData.message: message, UserData.attempt: SendingAttempt.first, UserData.logger: my_logger,
              UserData.bot: bot}
    bot.respond(update, message, success_send_message, failure_send_message, kwargs=kwargs)
    dispatcher.set_conversation_data(update, current_state, REMINDER_PICTURE)
    dispatcher.register_conversation_next_step_handler(update, common_handlers + [
        MessageHandler(TemplateResponseFilter(keywords=[ReadyText.no_picture_needed]), reminder_text_without_photo),
        MessageHandler(PhotoFilter(), reminder_text),
        MessageHandler(DefaultFilter(), reminder_picture)])


def reminder_text(bot, update):
    state = dispatcher.get_conversation_data(update, current_state)
    if state == REMINDER_PICTURE:
        message = update.get_effective_message()
        dispatcher.set_conversation_data(update, Attr.file_id, message.file_id)
        dispatcher.set_conversation_data(update, Attr.file_access_hash, message.access_hash)
        dispatcher.set_conversation_data(update, Attr.file_size, message.file_size)
        message = TextMessage(ReadyText.enter_reminder_text)
    else:
        message = TextMessage(ReadyText.wrong_answer_pls_text)
    kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: Step.getting_picture,
              UserData.message: message, UserData.attempt: SendingAttempt.first, UserData.logger: my_logger,
              UserData.bot: bot}
    bot.respond(update, message, success_send_message, failure_send_message, kwargs=kwargs)
    dispatcher.set_conversation_data(update, current_state, REMINDER_TEXT)
    dispatcher.register_conversation_next_step_handler(update,
                                                       [MessageHandler(TextFilter(), reminder_finished),
                                                        MessageHandler(DefaultFilter(), reminder_text)])


def reminder_text_without_photo(bot, update):
    state = dispatcher.get_conversation_data(update, current_state)
    if state == REMINDER_PICTURE:
        message = TextMessage(ReadyText.enter_reminder_text)
    else:
        message = TextMessage(ReadyText.wrong_answer_pls_text)
    kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: Step.ask_text,
              UserData.message: message,
              UserData.attempt: SendingAttempt.first, UserData.logger: my_logger, UserData.bot: bot}
    bot.respond(update, message, success_send_message, failure_send_message, kwargs=kwargs)
    dispatcher.set_conversation_data(update, current_state, SKIP_PHOTO)
    dispatcher.register_conversation_next_step_handler(update,
                                                       [MessageHandler(TextFilter(), reminder_finished),
                                                        MessageHandler(DefaultFilter(), reminder_text_without_photo)])


def reminder_finished(bot, update):
    message = update.get_effective_message()
    user = update.get_effective_user()
    dispatcher.set_conversation_data(update, Attr.peer_id, user.peer_id)
    dispatcher.set_conversation_data(update, Attr.peer_access_hash, user.access_hash)
    dispatcher.set_conversation_data(update, Attr.text, message.text)
    add_reminder_to_db(dispatcher.conversation_data[user.peer_id])
    dispatcher.get_conversation_data(update, Attr.peer_id)
    my_logger.info(LogText.notification_registering,
                   extra={UserData.user_id: dispatcher.get_conversation_data(update, Attr.peer_id),
                          Attr.text: dispatcher.get_conversation_data(update, Attr.text),
                          Attr.type: dispatcher.get_conversation_data(update, Attr.type)})
    general_message = TextMessage(ReadyText.reminder_set_successfully)
    template_message = TemplateMessage(general_message=general_message, btn_list=main_menu)
    kwargs = {UserData.user_peer: update.get_effective_user(), UserData.step_name: Step.finnish_notification_register,
              UserData.message: template_message, UserData.attempt: SendingAttempt.first, UserData.logger: my_logger,
              UserData.bot: bot}
    bot.respond(update, general_message, success_send_message, failure_send_message, kwargs=kwargs)
    dispatcher.finish_conversation(update)


################################ BankMessage handling ###########################
@dispatcher.message_handler([BankMessageFilter()])
def handling_bank_message(bot, update):
    if len(update.get_effective_user().peer_id) < 3:  # bot id 2digit
        return
    transfer_info = update.get_effective_message().bank_ext_message.transfer_info.items
    is_expenditure = transfer_info[TransferInfo.isExpenditure].value.get_json_object()[Value.value]
    payer = transfer_info[TransferInfo.payer].value.get_json_object()[Value.value]
    receiver = transfer_info[TransferInfo.receiver].value.get_json_object()[Value.value]
    description = transfer_info[TransferInfo.description].value.get_json_object()[Value.text]
    status = transfer_info[TransferInfo.status].value.get_json_object()[Value.text]
    msgUID = transfer_info[TransferInfo.msgUID].value.get_json_object()[Value.text]
    random_id = str(msgUID).split("-")[MsgUID.random_id]
    trace_no = None
    if status == TransferInfo.success_status:
        trace_no = transfer_info[TransferInfo.traceNo].value.get_json_object()[Value.value]
    purchase_message_date = str(msgUID).split("-")[MsgUID.date]
    add_receipt(purchase_message_date, payer, receiver, is_expenditure, status, trace_no, description, random_id)
    my_logger.info(LogText.registering_receipt,
                   extra={Attr.payer: payer, Attr.receiver: receiver, Attr.description: description})


########################### message sending part #########################
def check_for_sending_message():
    my_logger.info(LogText.reading_message_db)
    messages = messages_tobe_sent()
    for msg in messages:
        my_logger.info(LogText.db_has_message_to_send)
        msg_reminder = msg.reminder
        reminder_text_str = "*" + msg_reminder.text + "*"
        user_peer = UserPeer(msg_reminder.peer_id, msg_reminder.peer_access_hash)
        if msg_reminder.file_id:
            message = PhotoMessage(file_id=msg_reminder.file_id, access_hash=msg_reminder.file_access_hash,
                                   name=ReadyText.photo_name,
                                   file_size=msg_reminder.file_size,
                                   mime_type=MimeType.image, caption_text=TextMessage(reminder_text_str),
                                   file_storage_version=1, thumb=None)
        else:
            message = TextMessage(reminder_text_str)
        if msg_reminder.type == ReminderType.debt:
            if isinstance(message, TextMessage):
                message = PhotoMessage(file_id=DefaultPhoto.file_id, access_hash=DefaultPhoto.access_hash,
                                       name=ReadyText.photo_name,
                                       file_size=DefaultPhoto.file_size,
                                       mime_type=MimeType.image, caption_text=TextMessage(reminder_text_str),
                                       file_storage_version=1, thumb=DefaultPhoto.thumb)
            final_message = PurchaseMessage(msg=message, account_number=msg_reminder.card_number,
                                            amount=msg_reminder.money_amount,
                                            money_request_type=MoneyRequestType.normal)

        else:
            final_message = message
        loop.call_soon(send_message, final_message, user_peer, msg, SendingAttempt.first)
    # db_checking_interval = BotConfig.db_message_checking_interval - datetime.datetime.now().second + 1
    loop.call_later(2, check_for_sending_message)


def send_message(message, user_peer, msg, sending_attempt):
    random_id = generate_random_id()
    kwargs = {UserData.random_id: random_id, UserData.db_msg: msg, UserData.base_message: message,
              UserData.user_peer: user_peer, UserData.sending_attempt: sending_attempt,
              UserData.logger: my_logger, UserData.send_message: send_message}
    updater.dispatcher.bot.send_message(message, user_peer, random_id=random_id, success_callback=reminder_success,
                                        failure_callback=reminder_failure, kwargs=kwargs)


common_handlers = [
    CommandHandler([Command.start], start, include_template_response=True),
    MessageHandler(TemplateResponseFilter(keywords=[ReadyText.add_reminder]), add_reminder),
    MessageHandler(TemplateResponseFilter(keywords=[ReadyText.show_receipts]), receipts),
    MessageHandler(TemplateResponseFilter(keywords=[ReadyText.help_me]), help_me),
]
