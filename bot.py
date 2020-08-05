# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount


ACTION_TRIGGER = "@bot"
WELCOME_MESSAGE = """
Привет!
Я бот проекта DC_MDM - буду рад Вам помочь!\n
Вот что сейчас умею:\n
- env 'STAGE', 'UAT', 'PREPRPOD', 'PROD' (слежу за деплойментом на разные среды)
"""

GLOBAL_STATE = {'stage': 'STAGE_RPDC', 'uat': 'UAT_RPDC', 'preprod': 'PREPRPOD_PRDC', 'prod': 'PROD_PRDC'}


def get_command_string(text):
    return text[len(ACTION_TRIGGER) + 1 : ].lower().split(" ")


def show_env_state(env):
    result = "Нет данных"

    if env in GLOBAL_STATE:
        result = f"Сейчас на {env} развернуто {GLOBAL_STATE[env]}"

    return result;

def save_env_state(env, state):
    GLOBAL_STATE[env] = state;
    return f"Сохранил для {env} значение {state}"


def process_env_command(params):
    if (len(params) == 1):
        return show_env_state(params[0])
    if (len(params) == 2):
        return save_env_state(params[0], params[1])
    else:
        return "Неверно задана команда 'env' укажите $ENV" 


def process_command(params):
    if 'env' == params[0]:
        return process_env_command(params[1:])
    else:
        return f"Неизвестная команда {params[0]}"



class MyBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text

        if text.startswith(ACTION_TRIGGER):
            key_words = get_command_string(text)

            result = WELCOME_MESSAGE if len(key_words) < 1 else process_command(key_words)
            await turn_context.send_activity(result)

    async def on_members_added_activity(self,members_added: ChannelAccount, turn_context: TurnContext):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                name = turn_context.activity.from_property.name
                await turn_context.send_activity(WELCOME_MESSAGE)
