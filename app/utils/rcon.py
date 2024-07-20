from aiomcrcon import Client
from aiomcrcon import RCONConnectionError


class MinecraftRconClient:
    def __init__(self, host='127.0.0.1', port=666, password=''):
        self.host = host
        self.port = port
        self.password = password
        self.client: Client = None

    async def connect(self):
        self.client = Client(self.host, self.port, self.password)
        try:
            await self.client.connect()
        except RCONConnectionError as e:
            self.client = None

    async def execute(self, args):
        if self.client is not None:
            response = await self.client.send_cmd(args)
            return response
        return

    async def disconnect(self):
        if self.client is not None:
            await self.client.close()

        self.client = None
