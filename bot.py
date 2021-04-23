#!/usr/bin/env python
import os
import time
import logging
from web3 import Web3
from dotenv import load_dotenv
from telegram.ext import Updater
from telegram.ext import CommandHandler

# load variables from .env file
load_dotenv(override=True)
NODE_URL_ETH = os.getenv('NODE_URL_ETH')
NODE_URL_MATIC = os.getenv('NODE_URL_MATIC')
NODE_URL_BSC = os.getenv('NODE_URL_BSC')
BOT_TOKEN_TELEGRAM = os.getenv('BOT_TOKEN_TELEGRAM')
BOT_CHANID_TELEGRAM = os.getenv('BOT_CHANID_TELEGRAM')

# web3 instances
w3 = Web3(Web3.HTTPProvider(NODE_URL_ETH))
m3 = Web3(Web3.HTTPProvider(NODE_URL_MATIC))
b3 = Web3(Web3.HTTPProvider(NODE_URL_BSC))

# really basic Telegram bot config
updater = Updater(token=BOT_TOKEN_TELEGRAM, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# stuff for DQUICK price
CONTRACT_DQUICK_ADDR = os.getenv("CONTRACT_DQUICK_ADDR")
CONTRACT_DQUICK_ABI = os.getenv("CONTRACT_DQUICK_ABI")
dquick_contract = m3.eth.contract(address=CONTRACT_DQUICK_ADDR, abi=CONTRACT_DQUICK_ABI)
state = {}

def get_price():
    price = dquick_contract.functions['dQUICKForQUICK'](10**18).call() * 10**-18
    print(f'price: {price} QUICK')
    return price
    
def get_staked():
    price = dquick_contract.functions['dQUICKForQUICK'](10**18).call() * 10**-18
    staked = price * dquick_contract.functions['totalSupply']().call() * 10**-18
    print(f'staked: {staked} QUICK')
    return staked

def print_state(state, context):
    updater.bot.sendMessage(chat_id=BOT_CHANID_TELEGRAM, text=f'1 dQUICK = {state["price"]:.8f} QUICK; {state["staked"]:.0f} QUICK staked')

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    while True:
        state['price'] = get_price()
        state['staked'] = get_staked()
        print_state(state, context)
        time.sleep(120)

def main():
    # bot action is started up by sending the bot `/start` in a DM
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()

if __name__ == '__main__':
    main()
