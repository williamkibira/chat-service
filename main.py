# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
from app.application import Application
from app.configuration import Configuration

if __name__ == '__main__':
    application: Application = Application(configuration=Configuration.get_instance())
    application.run()


