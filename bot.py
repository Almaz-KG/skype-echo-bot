# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount


ACTION_TRIGGER = "@bot"
WELCOME_MESSAGE = """
Привет!
Я бот проекта DC_MDM - буду рад Вам помочь!\n
Вот что сейчас умею:\n
- env 'STAGE', 'UAT', 'PREPRPOD', 'PROD' - задачи DI на деплоймент
"""

GLOBAL_STATE = {'STAGE': 'STAGE_RPDC', 'UAT': 'UAT_RPDC', 'PREPROD': 'PREPRPOD_PRDC', 'PROD': 'PROD_PRDC'}


def get_command_string(text):
    return list(map(lambda x: x.strip(), text[len(ACTION_TRIGGER) + 1 : ].split(" ")))


def show_env_state(env):
    result = "Нет данных"

    if env.upper() in GLOBAL_STATE:
        result = f"Сейчас на {env} развернуто {GLOBAL_STATE[env.upper()]}"

    return result;


def save_env_state(env, state):
    GLOBAL_STATE[env.upper()] = state;
    return f"Сохранил для {env} значение {state}"


def show_all_env_state():
    result = f"""
    Текущий статус по средам: 

    """
    for k in GLOBAL_STATE.keys():
        result += f"""
    {k}: {GLOBAL_STATE[k]}"""
    return result;


def process_env_command(cmd):
    if (len(cmd) == 0):
        return show_all_env_state()
    if (len(cmd) == 1):
        return show_env_state(cmd[0])
    else:
        return save_env_state(cmd[0], " ".join(cmd[1:]))


def process_command(params):
    if 'env' == params[0].lower():
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