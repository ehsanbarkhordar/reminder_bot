import os


class BotConfig:
    receipts_report_name = os.environ.get('RECEIPTS_REPORT_NAME', "receipts_report.csv")
    bot_token = os.environ.get('TOKEN', "17fcfa921bae323895d2d70e6d3d998a2b3d000e")
    db_message_checking_interval = int(os.environ.get('MESSAGE_DB_CHECK_INTERVAL', 30))
    system_local = os.environ.get('SYSTEM_LOCAL', "fa_IR")
    accepted_datetime_format = os.environ.get('ACCEPTED_DATETIME_FORMAT', "%Y-%m-%d %H:%M")
    resending_max_try = int(os.environ.get('RESENDING_MAX_TRY', 5))
    re_uploading_max_try = int(os.environ.get('RE_UPLOADING_MAX_TRY', 5))


class DbConfig:
    db_user = os.environ.get('POSTGRES_USER', 'ehsan')
    db_password = os.environ.get('POSTGRES_PASSWORD', 'ehsan1379')
    db_host = os.environ.get('POSTGRES_HOST', 'localhost')
    db_name = os.environ.get('POSTGRES_DB', 'reminder')
    db_port = os.environ.get('POSTGRES_PORT', '5432')
    database_url = "postgresql://{}:{}@{}:{}/{}".format(db_user, db_password, db_host, db_port, db_name, "")
