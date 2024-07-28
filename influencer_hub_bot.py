import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Load environment variables
load_dotenv()

# States
NAME, PLATFORM, DESCRIPTION, LINK = range(4)

# Function to start the bot
def start(update: Update, context):
    update.message.reply_text(
        "Welcome to the Influencer Hub Admission Bot! 👋\n\n"
        "To join our community, you must have at least 1,000 subscribers on any social media platform.\n\n"
        "Please provide your Name/Handle:"
    )
    return NAME

# Function to get platform info
def get_platform(update: Update, context):
    context.user_data['name'] = update.message.text
    update.message.reply_text("Great! Now, what's your primary platform and niche?")
    return PLATFORM

# Function to get content description
def get_description(update: Update, context):
    context.user_data['platform'] = update.message.text
    update.message.reply_text("Awesome! Please provide a brief description of your content:")
    return DESCRIPTION

# Function to get social media link
def get_link(update: Update, context):
    context.user_data['description'] = update.message.text
    update.message.reply_text("Last step! Please share the link to your social media handle:")
    return LINK

# Function to process the application
def process_application(update: Update, context):
    context.user_data['link'] = update.message.text
    update.message.reply_text("Thank you for sharing your details. Your information is being verified. Please wait while we process your application.")
    
    # Here you would typically implement your verification logic
    # For this example, we'll assume all applications are approved
    
    update.message.reply_text(
        "Great news! Your application has been approved. Welcome to Influencer Hub! 🎉\n\n"
        "Here's your invite link to join the group: [Your Telegram Group Invite Link]\n\n"
        "We look forward to your contributions to our community!"
    )
    return ConversationHandler.END

# Function to cancel the conversation
def cancel(update: Update, context):
    update.message.reply_text("Application cancelled. Feel free to start over when you're ready!")
    return ConversationHandler.END

def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_platform)],
            PLATFORM: [MessageHandler(Filters.text & ~Filters.command, get_description)],
            DESCRIPTION: [MessageHandler(Filters.text & ~Filters.command, get_link)],
            LINK: [MessageHandler(Filters.text & ~Filters.command, process_application)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
