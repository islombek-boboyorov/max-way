import os.path
from django.core.management.base import BaseCommand
from telegram.ext import (Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, messagequeue as mq)
from telegram.utils.request import Request
from .main import (start_handler, contact_handler, message_handler, image_handler,location_handler, inline_handler)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        updater = Updater("1500549052:AAH7rFmLhrtPlkIVBsgyDsQ--UKaP6ao1Zg")

        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler('start', start_handler))
        dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
        dispatcher.add_handler(CallbackQueryHandler(inline_handler))
        dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))
        dispatcher.add_handler(MessageHandler(Filters.location, location_handler))
        dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))
        dispatcher.add_handler(MessageHandler(Filters.document.mime_type("image/jpeg"), image_handler))

        updater.start_polling()
        updater.idle()