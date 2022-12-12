from pyrogram import enums
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot import bot, LOGGER, DB_URI, OWNER_ID, PRE_DICT, LEECH_DICT, dispatcher, PAID_USERS, CAP_DICT, PAID_SERVICE, REM_DICT, SUF_DICT, CFONT_DICT, CAPTION_FONT
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.button_build import ButtonMaker
from bot.helper.ext_utils.db_handler import DbManger


def prefix_set(update, context):
    user_id_ = update.message.from_user.id 
    u_men = update.message.from_user.first_name

    if PAID_SERVICE is True:
        if not (user_id_ in PAID_USERS) and user_id_ != OWNER_ID:
            sendMessage(f"Buy Paid Service to Use this Prename Feature.", context.bot, update.message)
            return
    if (BotCommands.PreNameCommand[0] in update.message.text) and (len(update.message.text.split(' ')) == 1):
        help_msg = "<b>Send Prename after command:</b>"
        help_msg += f"\n<code>/{BotCommands.PreNameCommand[0]}" + " {prename}" + "</code>\n"
        help_msg += "\n<b>By Replying to Message (Including Prename):</b>"
        help_msg += f"\n<code>/{BotCommands.PreNameCommand[0]}" + " {message}" + "</code>"
        sendMessage(help_msg, context.bot, update.message)
    else:
        lm = sendMessage(f"<b>Please Wait....Processing🤖</b>", context.bot, update.message)
        pre_send = update.message.text.split(" ", maxsplit=1)
        reply_to = update.message.reply_to_message
        if len(pre_send) > 1:
            txt = pre_send[1]
        elif reply_to is not None:
            txt = reply_to.text
        else:
            txt = ""
        prefix_ = txt
        PRE_DICT[user_id_] = prefix_
        if DB_URI:
            DbManger().user_pre(user_id_, prefix_)
            LOGGER.info(f"User : {user_id_} Prename is Saved in DB")
        editMessage(f"<u><b><a href='tg://user?id={user_id_}'>{u_men}</a>'s Prename is Set Successfully 🚀</b></u>\n\n<b>• Prename Text: </b>{txt}", lm)


def suffix_set(update, context):
    user_id_ = update.message.from_user.id 
    u_men = update.message.from_user.first_name

    if PAID_SERVICE is True:
        if not (user_id_ in PAID_USERS) and user_id_ != OWNER_ID:
            sendMessage(f"Buy Paid Service to Use this Sufname Feature.", context.bot, update.message)
            return
    if (BotCommands.SufNameCommand[0] in update.message.text) and (len(update.message.text.split(' ')) == 1):
        help_msg = "<b>Send sufname after command:</b>"
        help_msg += f"\n<code>/{BotCommands.SufNameCommand[0]}" + " {sufname}" + "</code>\n"
        help_msg += "\n<b>By Replying to Message (Including Sufname):</b>"
        help_msg += f"\n<code>/{BotCommands.SufNameCommand[0]}" + " {message}" + "</code>"
        sendMessage(help_msg, context.bot, update.message)
    else:
        lm = sendMessage(f"<b>Please Wait....Processing🤖</b>", context.bot, update.message)
        pre_send = update.message.text.split(" ", maxsplit=1)
        reply_to = update.message.reply_to_message
        if len(pre_send) > 1:
            txt = pre_send[1]
        elif reply_to is not None:
            txt = reply_to.text
        else:
            txt = ""
        suffix_ = txt
        SUF_DICT[user_id_] = suffix_
        if DB_URI:
            DbManger().user_suf(user_id_, suffix_)
            LOGGER.info(f"User : {user_id_} Sufname is Saved in DB")
        editMessage(f"<u><b><a href='tg://user?id={user_id_}'>{u_men}</a>'s Sufname is Set Successfully 🚀</b></u>\n\n<b>• Sufname Text: </b>{txt}", lm)


def caption_set(update, context):
    user_id_ = update.message.from_user.id 
    u_men = update.message.from_user.first_name
    buttons = ButtonMaker()

    if PAID_SERVICE is True:
        if not (user_id_ in PAID_USERS) and user_id_ != OWNER_ID:
            sendMessage(f"Buy Paid Service to Use this Caption Feature.", context.bot, update.message)
            return
    buttons.sbutton("🛠 Change Font Style", f"capfont {user_id_} font")
    button = buttons.build_menu(2)
    if (BotCommands.CaptionCommand[0] in update.message.text) and (len(update.message.text.split(' ')) == 1):
        hlp_me = "<b>Send text with format along with command line:</b>\n"
        hlp_me += f"<b>Example:</b> /{BotCommands.CaptionCommand[0]}" + "{filename}\n\n"
        hlp_me += "<b>Custom Fillings:</b>\n"
        hlp_me += "{filename} - Filename of the File\n"
        hlp_me += "{size} - Size of the File"
        sendMarkup(hlp_me, context.bot, update.message, button)
    else:
        lm = sendMessage(f"<b>Please Wait....Processing🤖</b>", context.bot, update.message)
        pre_send = update.message.text.split(" ", maxsplit=1)
        reply_to = update.message.reply_to_message
        if len(pre_send) > 1:
            txt = pre_send[1]
        elif reply_to is not None:
            txt = reply_to.text
        else:
            txt = ""
        caption_ = txt
        CAP_DICT[user_id_] = caption_
        if DB_URI:
            DbManger().user_cap(user_id_, caption_)
            LOGGER.info(f"User : {user_id_} Caption is Saved in DB")
        editMessage(f"<b><u><a href='tg://user?id={user_id_}'>{u_men}</a>'s Caption is Set Successfully :</u></b>\n\n<b>• Caption Text: </b>{txt}", lm, button)


def setCapFont(update, context):
    query = update.callback_query
    message = query.message
    user_id_ = query.from_user.id
    data = query.data
    data = data.split()
    buttons = ButtonMaker()
    buttons.sbutton("Spoiler", f"capfont {user_id_} Spoiler")
    buttons.sbutton("Italics", f"capfont {user_id_} Italics")
    buttons.sbutton("Monospace", f"capfont {user_id_} Code")
    buttons.sbutton("Strike", f"capfont {user_id_} Strike")
    buttons.sbutton("Underline", f"capfont {user_id_} Underline")
    buttons.sbutton("Bold", f"capfont {user_id_} Bold")
    buttons.sbutton("Regular", f"capfont {user_id_} Regular")
    btns = buttons.build_menu(2)
    if user_id_ != int(data[1]):
        query.answer(text="Not Yours!", show_alert=True)
        return
    elif data[2] == "font":
        FONT_SPELL = {'b':'<b>Bold</b>', 'i':'<i>Italics</i>', 'code':'<code>Monospace</code>', 's':'<s>Strike</s>', 'u':'<u>Underline</u>', 'tg-spoiler':'<tg-spoiler>Spoiler</tg-spoiler>'}
        editMessage("<u>Change your Font Style from below:</u>\n\n• Current Style : " + CFONT_DICT.get(user_id_, [f'{FONT_SPELL[str(CAPTION_FONT)]} (Default)'])[0], message, btns)
    elif data[2] == "Spoiler":
        eVal = ["<tg-spoiler>Spoiler</tg-spoiler>", "tg-spoiler"]
        CFONT_DICT[user_id_] = eVal
        if DB_URI:
            DbManger().user_cfont(user_id_, eVal)
            LOGGER.info(f"User : {user_id_} Font Style Saved in DB")
        query.answer(text="Font Style changed to Spoiler!", show_alert=True)
        editMessage("<u>Change your Font Style from below:</u>\n\n• Current Style : "+ CFONT_DICT.get(user_id_)[0], message, btns)
    elif data[2] == "Italics":
        eVal = ["<i>Italics</i>", "i"]
        CFONT_DICT[user_id_] = eVal
        if DB_URI:
            DbManger().user_cfont(user_id_, eVal)
            LOGGER.info(f"User : {user_id_} Font Style Saved in DB")
        query.answer(text="Font Style changed to Italics!", show_alert=True)
        editMessage("<u>Change your Font Style from below:</u>\n\n• Current Style : "+ CFONT_DICT.get(user_id_)[0], message, btns)
    elif data[2] == "Code":
        eVal = ["<code>Monospace</code>", "code"]
        CFONT_DICT[user_id_] = eVal
        if DB_URI:
            DbManger().user_cfont(user_id_, eVal)
            LOGGER.info(f"User : {user_id_} Font Style Saved in DB")
        query.answer(text="Font Style changed to Monospace!", show_alert=True)
        editMessage("<u>Change your Font Style from below:</u>\n\n• Current Style : "+ CFONT_DICT.get(user_id_)[0], message, btns)
    elif data[2] == "Strike":
        eVal = ["<s>Strike</s>", "s"]
        CFONT_DICT[user_id_] = eVal
        if DB_URI:
            DbManger().user_cfont(user_id_, eVal)
            LOGGER.info(f"User : {user_id_} Font Style Saved in DB")
        query.answer(text="Font Style changed to Strike!", show_alert=True)
        editMessage("<u>Change your Font Style from below:</u>\n\n• Current Style : "+ CFONT_DICT.get(user_id_)[0], message, btns)
    elif data[2] == "Underline":
        eVal = ["<u>Underline</u>", "u"]
        CFONT_DICT[user_id_] = eVal
        if DB_URI:
            DbManger().user_cfont(user_id_, eVal)
            LOGGER.info(f"User : {user_id_} Font Style Saved in DB")
        query.answer(text="Font Style changed to Underline!", show_alert=True)
        editMessage("<u>Change your Font Style from below:</u>\n\n• Current Style : "+ CFONT_DICT.get(user_id_)[0], message, btns)
    elif data[2] == "Bold":
        eVal = ["<b>Bold</b>", "b"]
        CFONT_DICT[user_id_] = eVal
        if DB_URI:
            DbManger().user_cfont(user_id_, eVal)
            LOGGER.info(f"User : {user_id_} Font Style Saved in DB")
        query.answer(text="Font Style changed to Bold!", show_alert=True)
        editMessage("<u>Change your Font Style from below:</u>\n\n• Current Style : "+ CFONT_DICT.get(user_id_)[0], message, btns)
    elif data[2] == "Regular":
        eVal = ["Regular", "r"]
        CFONT_DICT[user_id_] = eVal
        if DB_URI:
            DbManger().user_cfont(user_id_, eVal)
            LOGGER.info(f"User : {user_id_} Font Style Saved in DB")
        query.answer(text="Font Style changed to Regular!", show_alert=True)
        editMessage("<u>Change your Font Style from below:</u>\n\n• Current Style : "+ CFONT_DICT.get(user_id_)[0], message, btns)


def userlog_set(update, context):
    user_id_ = update.message.from_user.id 
    u_men = update.message.from_user.first_name

    if PAID_SERVICE is True:
        if not (user_id_ in PAID_USERS) and user_id_ != OWNER_ID:
            sendMessage(f"Buy Paid Service to Use this Dump Feature.", context.bot, update.message)
            return
    if (BotCommands.UserLogCommand[0] in update.message.text) and (len(update.message.text.split(' ')) == 1):
        help_msg = "<b>Send channel id after command:</b>"
        help_msg += f"\n<code>/{BotCommands.UserLogCommand[0]}" + " -100xxxxxxx" + "</code>\n"
        help_msg += "\n<b>By Replying to Message (Including Channel ID):</b>"
        help_msg += f"\n<code>/{BotCommands.UserLogCommand[0]}" + " {message}" + "</code>"
        sendMessage(help_msg, context.bot, update.message)
        return
    lm = sendMessage("Checking your Channel ID... 🛃", context.bot, update.message)          
    pre_send = update.message.text.split(" ", maxsplit=1)
    reply_to = update.message.reply_to_message
    if len(pre_send) > 1:
        dumpid_ = pre_send[1]
    elif reply_to is not None:
        dumpid_ = reply_to.text
    else:
        dumpid_ = ""
    if not dumpid_.startswith('-100'):
        editMessage("<i><b>Your Channel ID Should Start with</b> -100xxxxxxxx, <u>Retry Again</u> !!</i>", lm)
        return
    dumpid_ = int(dumpid_.strip())
    try:
        editMessage("<i>Checking Your Channel Interaction ...</i> ♻️", lm)
        bot.sendMessage(chat_id=dumpid_, text=f'''╭─《 DUMP CHANNEL 》
│
├🆔 <b>Dump ID :</b> <code>{dumpid_}</code>
│
╰📂 <i>From Now On, The Bot will Send you Files in this Channel !!</i>''',  parse_mode='HTML')
    except Exception as err:
        editMessage(f"<i>Make Sure You have Added the Bot as Admin with Post Permission, Retry Again.</i>\n\nError : {err}", lm)
        return
    LEECH_DICT[user_id_] = str(dumpid_)
    if DB_URI:
        DbManger().user_dump(user_id_, str(dumpid_))
        LOGGER.info(f"User : {user_id_} LeechLog ID Saved in DB")
    editMessage(f"<b><a href='tg://user?id={user_id_}'>{u_men}</a>'s Dump Channel ID Saved Successfully...🛸</b>", lm)


def remname_set(update, context):
    user_id_ = update.message.from_user.id 
    u_men = update.message.from_user.first_name

    if PAID_SERVICE is True:
        if not (user_id_ in PAID_USERS) and user_id_ != OWNER_ID:
            sendMessage(f"Buy Paid Service to Use this Remname Feature.", context.bot, update.message)
            return
    if (BotCommands.RemnameCommand[0] in update.message.text) and (len(update.message.text.split(' ')) == 1):
        hlp_msg = "<b>Send Remname after command:</b>"
        hlp_msg += f"\n<code>/{BotCommands.RemnameCommand[0]}" + " {remname}" + "</code>\n"
        hlp_msg += "\n<b>By Replying to Message (Including Remname):</b>"
        hlp_msg += f"\n<code>/{BotCommands.RemnameCommand[0]}" + " {message}" + "</code>"
        sendMessage(hlp_me, context.bot, update.message)
    else:
        lm = sendMessage(f"<b>Please Wait....Processing🤖</b>", context.bot, update.message)
        pre_send = update.message.text.split(" ", maxsplit=1)
        reply_to = update.message.reply_to_message
        if len(pre_send) > 1:
            txt = pre_send[1]
        elif reply_to is not None:
            txt = reply_to.text
        else:
            txt = ""
        remname_ = txt
        REM_DICT[user_id_] = remname_
        if DB_URI:
            DbManger().user_rem(user_id_, remname_)
            LOGGER.info(f"User : {user_id_} Remname is Saved in DB")
        editMessage(f"<b><a href='tg://user?id={user_id_}'>{u_men}</a>'s Remname is Set Successfully :</b>\n\n<b>• Remname Text: </b>{txt}", lm)



prefix_set_handler = CommandHandler(BotCommands.PreNameCommand, prefix_set,
                                       filters=(CustomFilters.authorized_chat | CustomFilters.authorized_user), run_async=True)
suffix_set_handler = CommandHandler(BotCommands.SufNameCommand, suffix_set,
                                       filters=(CustomFilters.authorized_chat | CustomFilters.authorized_user), run_async=True)
caption_set_handler = CommandHandler(BotCommands.CaptionCommand, caption_set,
                                       filters=(CustomFilters.authorized_chat | CustomFilters.authorized_user), run_async=True)
userlog_set_handler = CommandHandler(BotCommands.UserLogCommand, userlog_set,
                                       filters=(CustomFilters.authorized_chat | CustomFilters.authorized_user), run_async=True)
remname_set_handler = CommandHandler(BotCommands.RemnameCommand, remname_set,
                                       filters=(CustomFilters.authorized_chat | CustomFilters.authorized_user), run_async=True) 
cap_font_handler = CallbackQueryHandler(setCapFont, pattern="capfont", run_async=True)

dispatcher.add_handler(prefix_set_handler)
dispatcher.add_handler(suffix_set_handler)
dispatcher.add_handler(caption_set_handler)
dispatcher.add_handler(userlog_set_handler)
dispatcher.add_handler(remname_set_handler)
dispatcher.add_handler(cap_font_handler)
