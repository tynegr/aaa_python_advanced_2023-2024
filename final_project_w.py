#!/usr/bin/env python
# coding: utf-8

from copy import deepcopy
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)
import os
import random

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# set higher logging level for httpx to avoid all GET
# and POST requests being logged
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# get token using BotFather

TOKEN = os.getenv('TG_TOKEN')

CONTINUE_GAME, FINISH_GAME = range(2)

FREE_SPACE = '.'
CROSS = 'X'
ZERO = 'O'

DEFAULT_STATE = [[FREE_SPACE for _ in range(3)] for _ in range(3)]


def get_default_state():
    """Helper function to get default state of the game"""
    return deepcopy(DEFAULT_STATE)


def generate_keyboard(state: list[list[str]]) -> list[list[InlineKeyboardButton]]:
    """Generate tic tac toe keyboard 3x3 (telegram buttons)"""
    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f'{r}{c}')
            for r in range(3)
        ]
        for c in range(3)
    ]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    context.user_data['keyboard_state'] = get_default_state()
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'X (your) turn! Please, '
                                    f'put X to the '
                                    f'free place', reply_markup=reply_markup)
    return CONTINUE_GAME


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Main processing of the game"""
    query = update.callback_query
    user = query.from_user
    choice = query.data

    row, col = int(choice[0]), int(choice[1])
    keyboard_state = context.user_data['keyboard_state']

    # Check if the chosen cell is free
    if keyboard_state[row][col] == FREE_SPACE:
        # Update the game state with the user's move
        keyboard_state[row][col] = CROSS

        # Check if the user has won
        if won([keyboard_state[r][c] for r in range(3) for c in range(3)]):
            await query.answer(f'Congratulations! '
                               f'You won, {user.first_name}!', show_alert=True)
            keyboard = generate_keyboard(keyboard_state)
            # Update keyboard with the last move
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f'X (your) turn!'
                                          f' Please, put X '
                                          f'to the free place', reply_markup=reply_markup)
            return end(update, context)  # Call end function when the user wins
        elif all(keyboard_state[r][c] != FREE_SPACE for r in range(3) for c in range(3)):
            # Check if the game is a draw
            await query.answer('It\'s a draw!', show_alert=True)
            keyboard = generate_keyboard(keyboard_state)  # Update keyboard with the last move
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f'X (your) turn! Please, put X to the free place', reply_markup=reply_markup)
            return end(update, context)  # Call end function when the game is a draw
        else:
            # Opponent's move (simple AI: place 'O' randomly in a free cell)
            empty_cells = [(r, c) for r in range(3) for c in range(3) if keyboard_state[r][c] == FREE_SPACE]
            if empty_cells:
                opp_choice = random.choice(empty_cells)
                keyboard_state[opp_choice[0]][opp_choice[1]] = ZERO

                # Check if the opponent has won
                if won([keyboard_state[r][c] for r in range(3) for c in range(3)]):
                    await query.answer(f'Sorry, {user.first_name}. You lost. Better luck next time!', show_alert=True)
                    keyboard = generate_keyboard(keyboard_state)  # Update keyboard with the last move
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await query.edit_message_text(f'X (your) turn! Please, put X to the free place', reply_markup=reply_markup)
                    return end(update, context)  # Call end function when the opponent wins

                # Update the keyboard
                keyboard = generate_keyboard(keyboard_state)
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(f'X (your) turn! Please, put X to the free place', reply_markup=reply_markup)

                return CONTINUE_GAME
            else:
                # No empty cells left, the game is a draw
                await query.answer('It\'s a draw!', show_alert=True)
                keyboard = generate_keyboard(keyboard_state)  # Update keyboard with the last move
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(f'X (your) turn! Please, put X to the free place', reply_markup=reply_markup)
                return end(update, context)  # Call end function when the game is a draw
    else:
        # Cell is already occupied, ask the user to choose again
        await query.answer('This cell is already occupied. Please choose a free cell.')
        return CONTINUE_GAME


def won(fields: list[str]) -> bool:
    """Check if crosses or zeros have won the game"""
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if fields[i] == fields[i + 3] == fields[i + 6] != FREE_SPACE:  # Check columns
            return True
        if fields[i * 3] == fields[i * 3 + 1] == fields[i * 3 + 2] != FREE_SPACE:  # Check rows
            return True
    if fields[0] == fields[4] == fields[8] != FREE_SPACE or fields[2] == fields[4] == fields[6] != FREE_SPACE:  # Check diagonals
        return True
    return False


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    # reset state to default so you can play again with /start
    context.user_data['keyboard_state'] = get_default_state()
    return ConversationHandler.END


def main() -> None:
    """Run the bot"""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Setup conversation handler with the states CONTINUE_GAME and FINISH_GAME
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CONTINUE_GAME: [
                CallbackQueryHandler(game, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
            FINISH_GAME: [
                CallbackQueryHandler(end, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)




if __name__ == '__main__':
    main()











