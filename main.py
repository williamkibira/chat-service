# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from domain.core.application import Application

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    application: Application = Application(port=4000)
    application.run()


