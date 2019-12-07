import asyncio
import sys

import tornado.web

import discord
from discord.ext import commands

import config


# # monkey patch du to 3.8 breaking change
if sys.platform == 'win32':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# bot setup

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
	print("the bot is ready")


@bot.command()
async def test(ctx):
	await ctx.send("it works")




# tornado setup

# subclassing RequestHandler is also usefull to define default headers
class BaseHandler(tornado.web.RequestHandler):

	# you can pass whatever you want
	def initialize(self, my_bot_instance, my_database):
		self.bot = my_bot_instance
		self.db = my_database

	async def prepare(self):
		await self.bot.wait_until_ready()



# define an handler
class HelloHandler(BaseHandler):

	async def get(self):
		self.set_status(200)
		self.write(f"hello, my name is {self.bot.user.name}")
		self.finish()


# we don't do anything with bot here, there is no reason to use BaseHandler
class TestHandler(tornado.web.RequestHandler):

	async def get(self, **kwargs):
		self.set_status(200)
		self.write(kwargs)
		self.finish()


# what is passed to inilialize
extra = {
	"my_bot_instance": bot,
	"my_database": "I'm a database",
}


routes = [
	(r"/hello", HelloHandler, extra),
	(r"/test/(?P<param1>[^\/]+)/?(?P<param2>[^\/]+)?/?(?P<param3>[^\/]+)?", TestHandler),
]



app = tornado.web.Application(routes, **config.settings)
app.listen(config.port)
loop = asyncio.get_event_loop()
asyncio.ensure_future(bot.start(config.bot_token), loop=loop)

loop.run_forever()