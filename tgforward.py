from telethon import TelegramClient, events, sync
from telethon.tl.types import PeerChat, PeerChannel
import sys
import logging
from logging.handlers import RotatingFileHandler

if len(sys.argv) < 2:
    print ('Please input config file name')
    exit(-1)
config_name = sys.argv[1]
import importlib
config = importlib.import_module(config_name)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(config.session_name)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler = RotatingFileHandler(config.session_name + '.log', mode='a', maxBytes=1048576*10, backupCount=2, encoding=None, delay=0)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)

error_handler = logging.FileHandler(config.session_name + '.error')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
logger.addHandler(error_handler)

logger.info("program started")

with TelegramClient(config.session_name, config.api_id, config.api_hash) as client:
    @client.on(events.NewMessage())
    async def handler(event):
        msg = event.message
        logger.info('new message: msg: %s', msg)
        peer_id = None
        if isinstance(msg.peer_id, PeerChat): # from chat
            peer_id = msg.peer_id.chat_id
            if peer_id in config.fwd_from:  # matched chat
                user_id = msg.from_id.user_id
                fwd_user_id = None
                if msg.fwd_from is not None:
                    fwd_user_id = msg.fwd_from.from_id.user_id
                if (len(config.fwd_from[peer_id]) == 0 or       # no user_id filtering
                    user_id in config.fwd_from[peer_id] or      # user_id matched
                    fwd_user_id in config.fwd_from[peer_id]):   # fwd_user_id matched
                    for fwd in config.fwd_to:
                        logger.info("forwarding to %s" % fwd)
                        await client.forward_messages(fwd, msg)
        elif isinstance(msg.peer_id, PeerChannel):
            peer_id = msg.peer_id.channel_id
            if peer_id in config.fwd_from:  # matched channel
                user_id = msg.from_id.user_id
                if (len(config.fwd_from[peer_id]) == 0 or       # no user_id filtering
                    user_id is None or                          # channel owner
                    user_id in config.fwd_from[peer_id]):       # user_id matched
                    for fwd in config.fwd_to:
                        logger.info("forwarding to %s" % fwd)
                        await client.forward_messages(fwd, msg)

client.start()
client.run_until_disconnected()