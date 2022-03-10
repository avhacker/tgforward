from telethon import TelegramClient, events, sync
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import sys
import logging
import traceback
from logging.handlers import RotatingFileHandler

def get_id_from_peer(peer):
    try:
        if isinstance(peer, PeerChat):
            return peer.chat_id
        elif isinstance(peer, PeerChannel):
            return peer.channel_id
        elif isinstance(peer, PeerUser):
            return peer.user_id
    except:
        pass
    return None

if len(sys.argv) < 2:
    print ('Please input config file name')
    exit(-1)
config_name = sys.argv[1]
import importlib
config = importlib.import_module(config_name)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(config_name)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler = RotatingFileHandler(config_name + '.log', mode='a', maxBytes=1048576*10, backupCount=2, encoding=None, delay=0)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)

error_handler = logging.FileHandler(config_name + '.error')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
logger.addHandler(error_handler)

logger.info("program started")

with TelegramClient(config_name, config.api_id, config.api_hash) as client:
    @client.on(events.NewMessage())
    async def handler(event):
        try:
            msg = event.message
            peer_id = get_id_from_peer(msg.peer_id)
            from_id = get_id_from_peer(msg.from_id)
            fwd_from_id = None
            if msg.fwd_from is not None:
                fwd_from_id = get_id_from_peer(msg.fwd_from.from_id)
            logger.info('New message: peer_id: %s, from_id:%s, fwd_from_id:%s, msg: %s', peer_id, from_id, fwd_from_id, msg)
            if peer_id in config.rules:
                tgfilter, dest_peers = config.rules[peer_id]
                if not tgfilter.senders or from_id in tgfilter.senders or fwd_from_id in tgfilter.senders:
                    for dest_peer in dest_peers:
                        logger.info("Forwarding message to %s" % dest_peer)
                        await client.forward_messages(dest_peer, msg)
        except Exception as e:
            logging.error(traceback.format_exc())
client.start()
client.run_until_disconnected()
logger.info("program ended")
