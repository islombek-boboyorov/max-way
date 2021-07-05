from telegram import KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, MessageHandler
import os
from django.conf import settings


def main_menu(update, context, chat_id):
    buttons = [
        [KeyboardButton(text="🛒 Buyurtma qilish")],
        [KeyboardButton(text="🛍 Buyurtmalarim")]
    ]
    context.bot.send_message(text="<b>Menu</b>",
                             parse_mode="HTML",
                             chat_id=chat_id,
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))


def get_category(update, context, categories):
    buttons = []
    row = []
    count = 0
    for category in categories:
        row.append(
            InlineKeyboardButton(text=f"{category['name']}",
                                 callback_data=f"category_{category['id']}")
        )
        count += 1
        if count == 2:
            buttons.append(row)
            count = 0
            row = []
    if len(categories) % 2 == 1:
        buttons.append(row)

    update.message.reply_text(
        text="<b>Mahsulot tanlang</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons))


def get_products(update, context, products, chat_id, message_id):
    buttons = []
    row = []
    count = 0
    for product in products:
        row.append(
            InlineKeyboardButton(text=f"{product['title']}",
                                 callback_data=f"category_product_{product['id']}"
                                 )
        )

        count += 1
        if count == 2:
            buttons.append(row)
            row = []
            count = 0
    if len(products) % 2 == 1:
        buttons.append(row)
    buttons.append(
        [InlineKeyboardButton(
            text="⬅️Orqaga",
            callback_data="category_back"
        )]
    )
    context.bot.edit_message_text(
        text="<b>Mahsulotni tanlang!</b>",
        parse_mode="HTML",
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


def get_back_category(update, context, categories, chat_id, message_id):
    buttons = []
    row = []
    count = 0
    for category in categories:
        row.append(
            InlineKeyboardButton(text=f"{category['name']}",
                                 callback_data=f"category_{category['id']}")
        )
        count += 1
        if count == 2:
            buttons.append(row)
            count = 0
            row = []
    if len(categories) % 2 == 1:
        buttons.append(row)

    context.bot.edit_message_text(
        text="<b>Mahsulot tanlang</b>",
        parse_mode="HTML",
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=InlineKeyboardMarkup(buttons))


def sent_product(update, context, product, chat_id, message_id, count=1):
    caption = f"<b>{product['title']}</b>\nNarxi:{product['price']}\n{product['description']}"
    buttons = [
        [
            InlineKeyboardButton(text="➖", callback_data=f"category_product_card_{product['id']}_minus_{count}"),
            InlineKeyboardButton(text=f"{count}", callback_data=f"category_product_card_{product['id']}_count"),
            InlineKeyboardButton(text="➕", callback_data=f"category_product_card_{product['id']}_plus_{count}")
        ],
        [
            InlineKeyboardButton(text="⬅️Orqaga", callback_data=f"category_product_back_{product['category_id']}_"),
            InlineKeyboardButton(text="✅ Savatchaga qo'shish",
                                 callback_data=f"category_product_card_{product['id']}_basket_{count}")
        ]
    ]
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)

    context.bot.send_photo(caption=caption, chat_id=chat_id,
                           photo=open(settings.MEDIA_ROOT / product['image'], "rb"),
                           parse_mode="HTML",
                           reply_markup=InlineKeyboardMarkup(buttons))


def product_amount(update, context, product_id, chat_id, text):
    buttons = [
        [InlineKeyboardButton(text="Tasdiqlash", callback_data=f"category_product_card_{product_id}_submit")],
        [InlineKeyboardButton(text="⬅️Orqaga", callback_data=f"category_product_card_{product_id}_back")]
    ]
    context.bot.send_message(
        text=text,
        chat_id=chat_id,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


def get_back_products(update, context, products, chat_id, message_id):
    buttons = []
    row = []
    count = 0
    for product in products:
        row.append(
            InlineKeyboardButton(text=f"{product['title']}",
                                 callback_data=f"category_product_{product['id']}")
        )
        count += 1
        if count == 2:
            buttons.append(row)
            count = 0
            row = []
    if len(products) % 2 == 1:
        buttons.append(row)
    buttons.append(
        [InlineKeyboardButton(text="⬅️Orqaga",
                              callback_data="category_back")]
    )
    print("B")
    context.bot.send_message(text="<b>Mahsulotni tanlang!</b>",
                             parse_mode="HTML",
                             chat_id=chat_id,
                             reply_markup=InlineKeyboardMarkup(buttons))
