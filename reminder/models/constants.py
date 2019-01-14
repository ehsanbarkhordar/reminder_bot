class Command:
    start = "/start"


class MimeType:
    image = "image/jpeg"
    csv = "text/csv"
    xlsx = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


class Attr:
    peer_id = "peer_id"
    user_id = "user_id"
    peer_access_hash = "peer_access_hash"
    file_id = "file_id"
    file_access_hash = "file_access_hash"
    file_size = "file_size"
    date = "date"
    time = "time"
    iterate_number = "iterate_number"
    periodic_type = "periodic_type"
    type = "type"
    card_number = "card_number"
    money_amount = "money_amount"
    text = "text"
    value = "value"
    url = "url"
    payer = "payer"
    receiver = "receiver"
    description = "description"


class ReadyText:
    upload_failed = "آپلود ناموفق بود"
    help_me = "راهنما"
    help = "این بات به منظور ایجاد یادآوری با ۲نوع عادی و یادآوری پرداخت استفاده میشود.\nهمچنین کاربر میتواند " \
           "بعد از انتخاب تاریخ و زمان شروع این" \
           " یادآوری تعداد دفعات تکرار آن و نوع تکرار آن که در چه بازه هایی " \
           "باشد را انتخاب نماید.\nیادآوری های پرداخت کاربر که پرداخت شده و رسید گرفته اند به صورت گزارشی در " \
           "فایل اکسل در قسمت مشاهده پرداخت ها قابل دسترسی خواهند بود. "
    command_not_found = "دستور مورد نظر یافت نشد"
    start = "شروع"
    pls_use_start = "برای شروع مجدد از کلید زیر استفاده نمایید"
    service_selection = "سرویس را انتخاب کنید"
    add_reminder = "افزودن یادآوری"
    show_receipts = "مشاهده رسید ها"
    receipts_report = "گزارش پرداخت های شما"
    enter_reminder_date = "روز شروع یادآوری خود را اعلام کنید. " \
                          "مثلا تاریخ 7 آذر سال 1397 را به صورت *13970907* وارد کنید.\n" \
                          "*نکته:* تاریخ وارد شده باید جلوتر از امروز باشد."
    enter_reminder_time = "ساعت یادآوری را وارد کنید. مثلا ساعت هشت و سی دقیقه را به صورت *8:30* وارد کنید.\n" \
                          "*نکته:* ساعت پیش فرض ساعت ۹ صبح است."
    wrong_format = "فرمت وارد شده صحیح نیست مجدد وارد کنید"
    time_is_past = "این زمان گذشته است مجدد وارد کنید"
    periodic_state_selection = "نوع اعلان یادآوری را انتخاب کنید"
    only_once = "فقط یکبار"
    default_time = "ساعت پیش فرض"
    default_time_value = "09:00"
    iterative = "تکرار شونده"
    wrong_answer = "جواب نامناسب"
    periodic_type_selection = "نوع تکرار را انتخاب کنید"
    daily = "روزانه"
    weekly = "هفتگی"
    monthly = "ماهانه"
    iterate_number_selection = "تعداد دفعات تکرار را وارد کنید:"
    wrong_answer_pls_enter_number = "جواب نامناسب (لطفا عدد وارد کنید)"
    notification_type_selection = "نوع یادآوری خود را انتخاب کنید"
    normal = "عادی"
    debt = "پرداختنی"
    card_number_entering = "شماره کارت مورد نظر را جهت واریز وارد کنید:\n (به صورت یک عدد ۱۶ رقمی)"
    wrong_card_number = "فرمت شماره کارت صحیح نمیباشد:"
    amount_entering = "مبلغ را به ریال وارد کنید:"
    picture_request = "تصویر مورد نظر خود را ارسال کنید(اختیاری)"
    enter_reminder_text = "متن یادآوری را وارد کنید:"
    wrong_answer_pls_text = "جواب نامناسب. لطفا متن وارد کنید"
    no_picture_needed = "بدون عکس"
    reminder_set_successfully = "یادآوری با موفقیت ثبت شد"
    photo_name = "یادآوری"


class ReminderType:
    normal = 'normal'
    debt = 'debt'


class Pattern:
    money_amount = None
    persian_datetime = \
        "^((139[7-9]|140[0-9])-(0[1-9]|[1-9]|1[0-2])-(0[1-9]|[1-9]|[1-2][0-9]|3[0-1])" \
        " ([0-1][0-9]|2[0-3]):[0-5][0-9])|" + \
        "((۱۳۹[۷-۹]|۱۴۰[۰-۹])-(۰[۱-۹]|[۱-۹]|۱[۰-۲])-(۰[۱-۹]|[۱-۹]|[۱-۲][۰-۹]|۳[۰-۱]) ([۰-۱][۰-۹]|۲[۰-۳]):[۰-۵][۰-۹])$"
    persian_date = ""
    card_number = "^[0-9 ۰-۹]{16}$"
    number = '^([0-9]+|[۰-۹]+)$'
    weekday = "^[0-6]$"
    month_day = "^[1-2][0-9]|[1-9]|3[0-1]$"
    year_day = "^[0-2][0-9][0-9]|3[0-5][0-9]|36[0-5]$"


class LogText:
    db_has_message_to_send = "there are some message to send"
    reading_message_db = "reading from messages db"
    successful_sending = "successful sending of message:"
    failed_sending = "failed sending of message:"
    successful_report_upload = "successful receipt report uploading"
    failed_report_upload = "failure receipt report uploading"
    successful_report_sending = "successful receipt report sending"
    failed_report_sending = "failure receipt report sending"
    registering_receipt = "receipt registered successfully"
    notification_registering = "notification registered successfully"
    successful_step_message_sending = "successful step message sending"
    failed_step_message_sending = "failure step message sending"


class TransferInfo:
    isExpenditure = 1
    payer = 2
    description = 4
    date = 9
    status = 10
    msgUID = 6
    receiver = 7
    traceNo = 12
    success_status = "SUCCESS"


class MessageStatus:
    sent = 1
    notSent = 0
    failed = -1


class SendingAttempt:
    first = 1


class MsgUID:
    random_id = 0
    date = 1


class UserData:
    bot = "bot"
    send_message = "send_message"
    logger = "logger"
    session = "session"
    ask_picture = "ask_picture"
    message_type = "message_type"
    message_id = "message_id"
    sending_set_time = "sending_set_time"
    base_message = "base_message"
    db_msg = "db_msg"
    random_id = "random_id"
    sending_attempt = "sending_attempt"
    kwargs = "kwargs"
    user_id = "user_id"
    user_peer = "user_peer"
    step_name = "step_name"
    message = "message"
    attempt = "attempt"
    report_attempt = "report_attempt"
    doc_message = "doc_message"
    file_url = "file_url"


class Value:
    text = "text"
    value = "value"


class Step:
    upload_fail = "upload_failed"
    wrong_service = "wrong_service"
    showing_guide = "showing_guid"
    default_handler = "default_handler"
    finnish_notification_register = "finnish_notification_register"
    wrong_name_response = "wrong_name_response"
    ask_text = "ask_text"
    getting_picture = "getting_picture"
    wrong_picture = "wrong_picture"
    wrong_amount = "wrong_amount"
    ask_amount = "ask_amount"
    wrong_card_number = "wrong_card_number"
    ask_card_number = "ask_card_number"
    wrong_type = "wrong_type"
    ask_type = "ask_type"
    wrong_iterate_number = "wrong_iterate_number"
    ask_iterate_number = "ask_iterate_number"
    wrong_period_type = "wrong_period_type"
    period_type = "period_type"
    wrong_periodic_state = "wrong_periodic_state"
    periodic_state = "periodic_state"
    wrong_time = "wrong_time"
    ask_time = "ask_time"
    conversation_starter = "conversation_starter"


class DefaultPhoto:
    file_id = -2551588256067351294
    access_hash = 201707397
    file_size = 41430
    thumb = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA4KCw0LCQ4NDA0QDw4RFiQXFhQUFiwgIRokNC43NjMuMjI6QVNGOj1OPjIySGJJTlZYXV5dOEVmbWVabFNbXVn/2wBDAQ8QEBYTFioXFypZOzI7WVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVn/wAARCABaAFoDASIAAhEBAxEB/8QAGgABAQEBAQEBAAAAAAAAAAAAAAQFAwIBB//EADwQAAEEAQEEBAkKBwAAAAAAAAEAAgMEEQUSEyExNUFhsRQVIjJCUXFzkSNkdIGCk6GyweEkJVNjcqKj/8QAFwEBAQEBAAAAAAAAAAAAAAAAAAIBA//EACcRAQACAQEGBwEBAAAAAAAAAAEAAhESAxMhMUFRIjJCcYGRsSOh/9oADAMBAAIRAxEAPwD9DREVSIRESIRESIRESIRESIRESIRT3+j7PundxUFPS4zUhkjnswl8bXOEcmASQrKiZWc7WS2Amuiz/Ffz6999+y8jRarnbUxmnPrkkJ7kxXvGq/b/AGWSWq8Ti2SeJjh1OeAVIdapnAidJM8nAZGw5PxXaLTKUQw2tGf8htd6qa0NaGtAaByAHJPAR/R7Ez/GFmRxEGnTEDmZSI+9A/VpMkRVYh1Ne4k/EcFZPLHFGd5M2Ha4BziBg/WseWaoHHfatZfIBx3Rw0+zAx+Kupq5H6znd087fhPd06nWqPsPtxgtx5DIwRxOOZW0sia4yxVEPi+5KwgAbTSAfV5WV38L1DHDTf8Au1LVU5Y+iKWBeK/bNBFPRs+GU459jY28+TnOMEj9FQuKI4Z3ETJJ7/R9n3Tu4pQ6Pre6b3BL/R9n3Tu4pQ6Pre6b3BX6PmR6/iRRWNRsS2Nx4LsRyujG8Ds8PYuv83+Y/wC6+aT5176U9aKq9sOAkUq2rlWZ251SR3l2oIR/bZtd6eLZXkmfULLif6Z2B8Foqe1ZMO7ZGwSTSnZY3OPaT2BYXsuCU0qGbfrOEWkUYiCIA4jreS7P1clZFFHC3ZijZGDxw1oCidYuVQJLbYHQ8A8xZyztweYWgss26uZtCvQxIpLFzeuZFRywHAe6UAHtxzVMBmMf8QGB+fQJI/FdEUrk5SiqOczP0PoiD7X5itBZ+h9EQfa/MVoKtp533k7LyV9iT3+j7PundxXjTZopKMDWSMc5sTQ4BwJHAc1XzXCKpXhl3sULI37Ozloxw9iwTThmtXVkkuk+de+lPWis7SfOvfSnr06rfLiRqOyCeA3DeCq4NnjIopQwZl6juxyCWCzG0yGAnLBzc0jjjtVEDJGQtbLLvXjm/Z2c/UuigcM6JqJnWJ5LkJrwQzMMow58kZaGN6+fM9gWiotOlfKbe8cXbNhzW56gMYC9Wrza8oj3E8riNr5Jm1hUjnSSKoGpZWizheuSZMWmv2eovkDD8CgOrvbnZpx56jtEj4cE3b1Zu8Og/U+6H0RB9r8xWgptPrGpSjgc4Oc3OSO05/VUrLubKTdmJQHtCIimXIJNKgfM6WN80EjiS4xPxklfPFfz6999+y0EV7y3ec91TtM12kRvI3tm3IB6L5cjuVdux4LDvd257ARt49EdZXdfCAQQRkHmCs1L5ppQB08Jj0rscTp2sBlfNbdsNYeY4Zd7MLZUlPTq9J8joWnaeeZOcD1DsVa3aNV8MnZVsHihERROsIiJEIiJEIiJEIiJEIiJEIiJEIiJE//Z"
