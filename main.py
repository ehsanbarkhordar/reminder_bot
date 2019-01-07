from reminder.reminder_bot import updater, loop, check_for_sending_message
from reminder.models.base import Base, engine

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    loop.call_soon(check_for_sending_message)
    updater.run()
