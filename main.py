import vk_api
import time
import config
from config import COUNT as count
session = vk_api.VkApi(token=config.TOKEN)
vk = session.get_api()
members = vk.messages.getConversationMembers(peer_id=config.PEER_ID)['items']
trigger = []
print('0 - поиск по беседе\nчто угодно - выгрузка из файла')
a = input()
if a == '0':
    for member in members:
        mem = member['member_id']
        if  mem > 0 and vk.groups.isMember(group_id=config.GROUP_ID, user_id=mem) == 0:
            trigger.append('@id{} (&#12288;)'.format(mem))
    with open('last.txt', 'w') as f:
        for i in trigger:
            f.writelines('{}\n'.format(i))
        f.close()

else:
    with open('last.txt', 'r') as f:
        tri=f.read()
        f.close()
trigger=tri.split('\n')
start = len(trigger)

print(len(trigger))
cycle = start
end = 0
oneCycle = 0
while cycle > 0:
    try:
        if cycle >= count:
            one = start // count
            oneCycle = cycle // one
            if oneCycle == 0:
                oneCycle = cycle % one
            vk.messages.send(peer_id=config.PEER_ID,
                             message='{}\n{}'.format(config.MSG,
                                 trigger[end:end+oneCycle]), random_id=0)
            time.sleep(2)
            end += oneCycle
            cycle -= oneCycle
        else:
            vk.messages.send(peer_id=config.PEER_ID,
                             message='{}\n{}'.format(config.MSG,
                                 trigger[end:end + cycle]), random_id=0)
            end += cycle
            cycle = 0
    except:
        time.sleep(10)
        count -= 1
print(end)