# 登陆微信
from wxpy import *

bot  = Bot()
my_friend = bot.friends()
print(my_friend)