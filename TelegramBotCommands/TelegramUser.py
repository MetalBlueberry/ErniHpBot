"""
This file contais the definition of TUser class and helpers to
abstract the communication with the database
"""

from telepot.namedtuple import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from .RedisStorage import RedisStorage, CONN, redis_decode


class TChat(RedisStorage):
    # This variables will be defined externaly after bot initialization in __init__.py
    bot = None
    bot_username = ""

    def redis_prefix(self, attr=""):
        """Generates the prefix for a desired attribute."""
        return "TChat:" + str(self.id) + ":" + attr

    def sendMessage(self, msg, keyboard=None, inlinekeyboard=None):
        if keyboard is not None and inlinekeyboard is not None:
            raise Exception("You can't use inlinekeyboard and keyboard at the same time.")
        if keyboard is not None:
            keyboard_markup = self.generate_keyboard_from_list(keyboard)
            self.bot.sendMessage(self.id, msg, reply_markup=keyboard_markup)
        elif inlinekeyboard is not None:
            keyboard_markup = self.generate_inlinekeyboard_from_list(inlinekeyboard)
            self.bot.sendMessage(self.id, msg, reply_markup=keyboard_markup)
        else:
            self.bot.sendMessage(self.id, msg)

    @staticmethod
    def generate_keyboard_from_list(keyboard, resize=True, one_time_keyboard=True):
        buttons = list()
        for rowkey in keyboard:
            buttons.append(list())
            if isinstance(rowkey,list):
                for columkey in rowkey:
                    buttons[-1].append(KeyboardButton(text=columkey))
            else:
                buttons[-1].append(KeyboardButton(text=rowkey))
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=resize,
                                   one_time_keyboard=one_time_keyboard)
    @staticmethod
    def generate_inlinekeyboard_from_list(keyboard, resize=True, one_time_keyboard=True):
        buttons = list()
        for rowkey in keyboard:
            buttons.append(list())
            if isinstance(rowkey,list):
                for columkey in rowkey:
                    buttons[-1].append(InlineKeyboardButton(text=columkey, callback_data="/InlineKeyboard_" + columkey))
            else:
                buttons[-1].append(InlineKeyboardButton(text=columkey, callback_data=columkey))
        return InlineKeyboardMarkup(inline_keyboard=buttons)
class TUser(TChat):
    """handles the data for each user"""
    def redis_prefix(self, attr=""):
        """Generates the prefix for a desired attribute."""
        return "TUser:" + str(self.id) + ":" + attr
    @staticmethod
    def get_user_by_username(username: str):
        username = username.replace("@", "")
        keys = CONN.keys("*username")
        usernames = list(map(redis_decode, CONN.mget(keys)))
        usernames_dict = dict(zip(usernames, keys))
        for key, value in usernames_dict.items():
            if username.lower() == key.lower():
                id = int(value[str(value).find(":")-1:str(value).rfind(":") - 2])
                return TUser.get_user_by_id(id)
        return None

    @staticmethod
    def get_user_by_id(id):
        return TUser({"id": id})


class TGroup(TChat):
    """handles the data for each group"""
    def redis_prefix(self, attr=""):
        """Generates the prefix for a desired attribute."""
        return "TGroup:" + str(self.id) + ":" + attr
