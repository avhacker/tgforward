chat_to_monitor = 1111111111
channel_to_monitor = 222222222
chat_to_monitor_transfer = 33333333
users_to_monitor = [55555555]
chats_to_forward = [-44444444]

# necessary variables
# note that user monitor is ignoreed in channel
#fwd_from = {chat_to_monitor: [user_to_monitor, ], channel_to_monitor: []}
#fwd_to = [chat_my_share,]
rules = {
    fwd_from_group: {"filters": {"senders": [senders_to_monitor]}, "forward_to_groups": [], "add_msg_url": True}
}
api_id = 99999999
api_hash = 'myhashmyhasmyhash_please_replace'
