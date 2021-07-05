from django.shortcuts import render
from telegram import KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, MessageHandler
from datetime import datetime
from . import database
from . import comman


def check_user_data(func):
    def inner(update, context):
        chat_id = update.message.from_user.id
        user = database.get_user_by_chat_id(chat_id)
        state = context.user_data.get("state", 0)
        if state == 0 or state == 4:
            if user:
                if not user['first_name']:
                    update.message.reply_text(
                        text="Ismingizni kiriting",
                        reply_markup=ReplyKeyboardRemove()
                    )
                    context.user_data['state'] = 1
                    return False

                elif not user['last_name']:
                    update.message.reply_text(
                        text="Familiyangizni kiriting",
                        reply_markup=ReplyKeyboardRemove()
                    )
                    context.user_data['state'] = 2
                    return False

                elif not user['contact']:
                    update.message.reply_text(
                        text="Telefon nomeringizni kiriting yoki \n'Yuborish' tugmasini bosing",
                        reply_markup=ReplyKeyboardMarkup(
                            [[KeyboardButton(text="Yuborish", request_contact=True)]],
                            resize_keyboard=True)
                    )
                    context.user_data['state'] = 3
                    return False

                else:
                    return func(update, context)

            else:
                database.create_user(chat_id, datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                update.message.reply_text(
                    text=f"<b>Xush kelibsiz </b>",
                    parse_mode="HTML"
                )
                update.message.reply_text(

                    text="Ismingizni kiriting",
                )
                context.user_data['state'] = 1

                return False
        else:
            return func(update, context)

    return inner


def check_user_state(update, context):
    try:
        chat_id = update.message.from_user.id
    except:
        chat_id = update.callback_query.message.chat_id
    user = database.get_user_by_chat_id(chat_id)
    if user:
        if not user['first_name']:
            update.message.reply_text(
                text="Ismizni kiriting",
                reply_markup=ReplyKeyboardRemove()
            )
            context.user_data['state'] = 1

        elif not user['last_name']:
            update.message.reply_text(
                text="Familiyangizni kiriting",
                reply_markup=ReplyKeyboardRemove()
            )
            context.user_data['state'] = 2

        elif not user['contact']:
            update.message.reply_text(
                text="Telefon nomeringizni kiriting yoki \n'Yuborish' tugmasini bosing",
                reply_markup=ReplyKeyboardMarkup(
                    [[KeyboardButton(text="Yuborish", request_contact=True)]],
                    resize_keyboard=True)
            )
            context.user_data['state'] = 3

        else:
            context.user_data['state'] = 4
            comman.main_menu(update, context, chat_id)


@check_user_data
def start_handler(update, context):
    chat_id = update.message.from_user.id
    check_user_state(update, context)
    comman.main_menu(update, context, chat_id)


@check_user_data
def message_handler(update, context):
    msg = update.message.text
    chat_id = update.message.from_user.id
    state = context.user_data.get('state', 0)

    if state == 1:
        database.update_user(state, chat_id, msg)
        check_user_state(update, context)

    elif state == 2:
        database.update_user(state, chat_id, msg)
        check_user_state(update, context)

    elif state == 3:
        database.update_user(state, chat_id, msg)
        check_user_state(update, context)

    elif state == 5:
        context.user_data["first_name"] = msg
        update.message.reply_text(
            text="Familiyangizni kiriting ?"
        )
        context.user_data["state"] = 6

    elif state == 6:
        context.user_data['last_name'] = msg
        update.message.reply_text(
            text="Telefon nomeringizni kiriting yoki \n'Yuborish' tugmasini bosing",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton(text="Yuborish", request_contact=True)]],
                resize_keyboard=True)
        )
        context.user_data['state'] = 7

    elif state == 7:
        context.user_data["phone_number"] = msg
        update.message.reply_text(
            text="Manzilingizni kiriting yoki Yuborish tugmasini bosing!",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton(text="Yuborish", request_location=True)]],
                resize_keyboard=True
            )
        )
        context.user_data['state'] = 8

    elif state == 8:
        context.user_data["address"] = msg
        update.message.reply_text(text="To'lov",
                                  reply_markup=ReplyKeyboardRemove())
        buttons = [
            [InlineKeyboardButton(text="Naxd pul ko'rinishida", callback_data="price_1")],
            [InlineKeyboardButton(text="Pul ko'chirish yordamida", callback_data="price_2")]
        ]
        update.message.reply_text(
            text="<b>To'lov turini tanlang!</b>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    else:
        if msg == "🛒 Buyurtma qilish":
            categories = database.get_category()
            comman.get_category(update, context, categories)

        elif msg == "🛍 Buyurtmalarim":
            orders = database.get_info_order(chat_id)
            text = ""
            n = 1
            total = 0
            for order in orders:
                for i, j in eval(order['products']).items():
                    product = database.get_product_by_id(int(i))
                    if order['status'] == 1:
                        text += f"<b>{n}. {product['title']} ⏩ {j} = {int(j) * product['price']} so'm</b>\n Buyurtma yetkazilmoqa 🚚\n\n"
                        total += int(j) * product['price']
                        n += 1
                    elif order['status'] == 2:
                        text += f"<b>{n}. {product['title']} ⏩ {j} = {int(j) * product['price']} so'm </b>\n Yetkazib berilgan ✅\n\n"
                        total += int(j) * product['price']
                        n += 1
                    elif order['status'] == 3:
                        text += f"<b>{n}. {product['title']} ⏩ {j} = {int(j) * product['price']} so'm </b>\n Bekor qilingan ❌\n\n"
                        n += 1

            update.message.reply_text(
                text=text,
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="⬅️Orqaga", callback_data="back_menu")]]
                )
            )
            update.message.reply_text(text="Buyurtmalarim",
                                      reply_markup=ReplyKeyboardRemove())



def location_handler(update, context):
    loca = update.message.location
    context.user_data['location'] = loca
    update.message.reply_text(
        text="To'lov",
        reply_markup=ReplyKeyboardRemove()
    )
    buttons = [
        [InlineKeyboardButton(text="Naxd pul ko'rinishida", callback_data="price_1")],
        [InlineKeyboardButton(text="Pul ko'chirish yordamida", callback_data="price_2")]
    ]
    update.message.reply_text(
        text="<b>To'lov turini tanlang!</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


def contact_handler(update, context):
    chat_id = update.message.from_user.id
    contact = update.message.contact.phone_number
    state = context.user_data.get("state", 0)
    if state == 3:
        database.update_user(state, chat_id, contact)
        check_user_state(update, context)

    elif state == 7:
        context.user_data['phone_number'] = contact
        update.message.reply_text(
            text="Manzilingizni kiriting yoki Yuborish tugmasini bosing!",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton(text="Yuborish", request_location=True)]],
                resize_keyboard=True
            )
        )
        context.user_data["state"] = 8


def image_handler(update, context):
    pass


def inline_handler(update, context):
    query = update.callback_query
    chat_id = query.from_user.id
    message_id = query.message.message_id
    data = query.data.split('_')
    if data[0] == "category":
        if data[1] == "back":
            categories = database.get_category()
            comman.get_back_category(update, context, categories, chat_id, message_id)

        elif data[1] == "product":
            if data[2] == "back":
                products = database.get_category_products(int(data[3]))
                context.bot.delete_message(chat_id=chat_id, message_id=message_id)
                comman.get_back_products(update, context, products, chat_id, message_id)
            elif data[2] == "card":
                if len(data) > 4:
                    text = context.user_data.get("text", "")
                    if data[4] == "minus":
                        count = int(data[5])
                        if count > 1:
                            count -= 1
                            product = database.get_product_by_id(int(data[3]))
                            cart = context.user_data.get("cart", {})
                            cart[data[3]] = cart.get(data[3], 1) - 1
                            print(cart, "AAa")
                            context.user_data['cart'] = cart
                            total_price = context.user_data.get("total_price", 0)
                            for i, j in cart.items():
                                product = database.get_product_by_id(int(i))
                                price = int(product['price'])
                                total_price += price * int(j)
                                text += f"{product['title']} ⏩ {int(j)}\n"
                            context.user_data['total_price'] = total_price
                            context.user_data['text'] = text
                            comman.sent_product(update, context, product, chat_id, message_id, count)

                    elif data[4] == "plus":
                        text = context.user_data.get("text", "")
                        print(type(text))
                        count = int(data[5])
                        count += 1
                        product = database.get_product_by_id(int(data[3]))
                        cart = context.user_data.get("cart", {})
                        cart[data[3]] = cart.get(data[3], 1) + 1
                        print(cart)
                        context.user_data['cart'] = cart
                        total_price = context.user_data.get("total_price", 0)
                        for i, j in cart.items():
                            product = database.get_product_by_id(int(i))
                            price = int(product['price'])
                            total_price += price * int(j)
                            text += f"{product['title']} ⏩ {int(j)}\n"
                        context.user_data['total_price'] = total_price
                        context.user_data['text'] = text
                        comman.sent_product(update, context, product, chat_id, message_id, count)

                    elif data[4] == "basket":
                        cart = context.user_data.get("cart", {})
                        total_price = context.user_data.get("total_price", 0)
                        if int(data[5]) == 1:
                            product = database.get_product_by_id(int(data[3]))
                            text += f"{product['title']} ⏩ 1\n"
                            total_price += int(product['price'])
                            context.user_data['text'] = text
                            cart[data[3]] = 1
                        context.user_data["text"] = text
                        context.user_data['cart'] = cart
                        context.user_data["total_price"] = total_price
                        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
                        comman.product_amount(update, context, int(data[3]), chat_id, text)

                    elif data[4] == "back":
                        category_id = database.get_product_by_id(int(data[3]))['category_id']
                        products = database.get_category_products(category_id)
                        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
                        comman.get_back_products(update, context, products, chat_id, message_id)

                    elif data[4] == "submit":
                        cart = context.user_data.get("cart", {})
                        total_price = context.user_data.get("total_price", 0)
                        database.update_order(total_price, datetime.now().strftime("%d-%m-%Y %H:%M:%S"), cart, chat_id)
                        context.user_data['cart'] = {}
                        context.user_data['total_price'] = 0
                        context.user_data['text'] = ""
                        context.user_data['order_id'] = database.get_max_id(chat_id)
                        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
                        context.bot.send_message(
                            text="Ismingizni kiriting",
                            chat_id=chat_id,
                            reply_markup=ReplyKeyboardRemove()
                        )
                        context.user_data["state"] = 5

                else:
                    comman.product_amount(update, context, int(data[3]), chat_id, message_id)

            else:
                product = database.get_product_by_id(int(data[2]))
                comman.sent_product(update, context, product, chat_id, message_id)

        else:
            print(data[1])
            products = database.get_category_products(int(data[1]))
            comman.get_products(update, context, products, chat_id, message_id)

    elif data[0] == "price":
        a = 0
        if data[1] == '1':
            a = 1
        elif data[1] == "2":
            a = 2
        context.user_data['price_type'] = a
        first_name = context.user_data.get('first_name')
        last_name = context.user_data.get('last_name')
        phone = context.user_data.get('phone_number')
        price = context.user_data.get('price_type')
        time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        order = context.user_data.get('order_id')
        address = context.user_data.get('address')
        database.update_user_site(first_name, last_name, phone, price, time, order, address)
        context.bot.send_message(
            text="Sizning buyurtmangiz qabul qilindi\nMuamoa yuzaga kelsa biz bilan bog'laning\ntel: +99 890 123 45 67",
            chat_id=chat_id,
        )
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        check_user_state(update, context)

    elif data[0] == "back":
        check_user_state(update, context)
