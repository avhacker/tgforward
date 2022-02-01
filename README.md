# tgforward
Forward telegram messages

This tool forwards telegram message from chats/channels/users to other peers. Usage:
$ python3 tgforward sample

This will run the tool according to the config sample.py. It forwars the message sent from "user_to_monitor" in "chat_to_monitor" to "chat_my_share". It also forwars all message in "channel_to_monitor" to "chat_my_share", too.
For api_id and api_hash, you can get it by following the official telemgram document here: https://core.telegram.org/api/obtaining_api_id#obtaining-api-id
