
from insta_follower import InstaFollower


bot = InstaFollower()

bot.login()
bot.find_followers()
bot.follow()

input("Press any key to close...")

bot.driver.quit()

