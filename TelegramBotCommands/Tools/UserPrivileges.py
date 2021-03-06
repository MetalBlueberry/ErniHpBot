
from ..CommandsBase import BaseCommand, ChatType
from ..TelegramUser import TUser


def check_for_access(user, command_info):
    return command_info.required_rights and command_info.required_rights not in user.get_set("privileges")


@BaseCommand.register("/GiveAccess",
                      help_description="Give Access to user",
                      help_use_hint="Usage: /GiveAccess @username Led",
                      required_rights="Admin")
def give_access(user, chat, message, command_info, **kwargs):
    if check_for_access(user, command_info):
        chat.sendMessage("Only admins can give access.")
        return
    if len(message) != 3:
        chat.sendMessage(command_info.help_use_hint)
        return
    target_username = message[1]
    privilege = message[2]
    target = TUser.get_user_by_username(target_username)
    if not target:
        chat.sendMessage("User " + target_username + " do not exist")
        return
    target.privileges.add(privilege)
    chat.sendMessage(target_username + " is " + privilege + " now.")

    target.sendMessage(user.username + " gives your right to " + privilege)


@BaseCommand.register("/RemoveAccess",
                      help_description="Remove Access to user,",
                      help_use_hint="Usage: /RemoveAccess @username Led",
                      required_rights="Admin")
def remove_access(user, chat, message, command_info, **kwargs):
    if check_for_access(user, command_info):
        chat.sendMessage("Only admins can remove access.")
        return
    if len(message) != 3:
        chat.sendMessage(command_info.help_use_hint)
        return
    target_username = message[1]
    privilege = message[2]
    target = TUser.get_user_by_username(target_username)
    if not target:
        chat.sendMessage("User " + target_username + " do not exist")
        return
    if message[2] == "Admin" and user == target:
        chat.sendMessage("You can't remove Admin rights from yourself")
        return
    target.privileges.remove(privilege)
    chat.sendMessage(target_username + " is no longer " + privilege)
    target.sendMessage(user.username + " removes your right to " + privilege)


@BaseCommand.register("/CheckAccess",
                      help_description="Check things that you or other user have access to.")
def check_access(user, chat, **kwargs):
    chat.sendMessage(str(user.get_set("privileges")))


@BaseCommand.register("/Admin", help_description="CHEAT!, gives you Admin rights",
                      available_in=set({ChatType.PRIVATE}))
def set_admin(user, **kwargs):
    user.get_set("privileges").add("Admin")
    user.sendMessage("You are Admin now")


# command("/Admin", set_admin, help_description="CHEAT!, gives you Admin rights",
#         available_in=set({ChatType.PRIVATE}))
