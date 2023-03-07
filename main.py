# -*- coding: utf-8 -*-

import werobot

robot = werobot.WeRoBot(token='tokenhere')

@robot.handler
def hello(message):
    return 'Hello World!'

@robot.filter("帮助")
def show_help(message):
    return """
    帮助
    XXXXX
    """


@robot.text
def hello_world(message):
    return 'Hello World!'

robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()