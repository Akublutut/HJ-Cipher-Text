from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from keep_alive import keep_alive  # Import keep_alive.py

# Mapping letters to numbers (A=01, B=02, ..., Z=26)
letter_to_number = {chr(i + 65): f"{i + 1:02d}" for i in range(26)}  # 'A' = 01, 'B' = 02, ..., 'Z' = 26
number_to_letter = {v: k for k, v in letter_to_number.items()}

# Function to convert text to numbers with space between words
def text_to_numbers(text):
    words = text.upper().split()  # Split text into words
    converted_words = ['-'.join(letter_to_number[char] for char in word if char in letter_to_number) for word in words]
    return ' '.join(converted_words)

# Function to convert numbers to text
def numbers_to_text(numbers):
    numbers = numbers.replace("-", "")  # Remove dashes if present
    text = ""
    for i in range(0, len(numbers), 2):  # Read every two digits
        number = numbers[i:i+2]
        if number in number_to_letter:
            text += number_to_letter[number]
        else:
            return "Invalid code. Make sure it matches the format (e.g., 08-05-12-12-15)."
    return text

# Handle start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome! Send me a word or a code, and I'll convert it for you.")

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text.strip()  # Remove leading/trailing spaces
    if message.isalpha():  # If the message is text (only letters)
        result = text_to_numbers(message)
        await update.message.reply_text(f"{message} = `{result}`", parse_mode="Markdown")
    elif all(part.isdigit() and len(part) == 2 for part in message.split("-")):  # If the message is numbers (properly formatted)
        result = numbers_to_text(message)
        await update.message.reply_text(f"`{message}` = `{result}`", parse_mode="Markdown")
    else:
        # Invalid input
        await update.message.reply_text("Please send a valid word or number sequence (e.g., 08-05-12-12-15).")

# Main function to run the bot
def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = Application.builder().token("8160553859:AAEwOfOYspcIZDmwtGCJv9WBv3KanxGQNJY").build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

# Run keep_alive to ensure the bot stays alive on Render
if __name__ == "__main__":
    keep_alive()  # Start the web server to keep the bot alive
    main()  # Run the bot
