from tgfilter import TgFilter

chat_to_monitor = 1111111111
channel_to_monitor = 222222222
chat_to_monitor_transfer = 33333333
chat_my_share = -44444444
user_to_monitor = 55555555

# necessary variables
# note that user monitor is ignoreed in channel
#fwd_from = {chat_to_monitor: [user_to_monitor, ], channel_to_monitor: []}
#fwd_to = [chat_my_share,]
rules = {
    chat_to_monitor: (TgFilter([user_to_monitor, ]), [chat_my_share,]),
}
api_id = 99999999
api_hash = 'myhashmyhasmyhash_please_replace'
