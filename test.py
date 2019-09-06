from plurk_oauth import PlurkAPI
import json
import requests

plurk = PlurkAPI.fromfile("API.keys")
channelAddr = plurk.callAPI("/APP/Realtime/GetUserChannel").get("comet_server")[:-len("&offset=0")]
offset = 0

while True:
    callback = json.loads(requests.get(channelAddr+"&offset="+str(offset))
                          .text[len("CometChannel.scriptCallback("):-len(");")])
    newOffset = callback.get("new_offset")
    if newOffset != -1:
        tds = callback.get("data")
        for td in tds:
            print(json.dumps(td, indent=4, sort_keys=True, ensure_ascii=False))
            # TODO: stuff td in to a queue

        offset = newOffset

# example of calling plurk API
# response = plurk.callAPI('/APP/Responses/get', options={'plurk_id': 1419178662})

# comet server call back data model:
# {
#    "data": [
#       {<json>},
#       {<json>}....
#    ],
#    "new_offset": 16
# }

# print(td.get("type"))
# possible value:
# "update_notification" /unfriend /follow /friend request
# "new_response"
# "new_plurk"
# CometChannel.scriptCallback(
# {"new_offset": 9,"data": [{"counts": {"req": 1, "noti": 1}, "type": "update_notification"}]});
