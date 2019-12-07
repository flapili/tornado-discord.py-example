# tornado-discord.py-example

A really short example to show how combine a web server and a discord bot.

this example have 2 demonstrations endpoints:

`http://localhost:8080/test/a/b/c` -> {"param1": "a", "param2": "b", "param3": "c"}

`http://localhost:8080/hello`-> hello, my name is tornado example


tip: Tornado should only be used as backend/API, render your pages with something else (I personally use VueJs),
use AJAX or WS to communicate between your backend and your front end
