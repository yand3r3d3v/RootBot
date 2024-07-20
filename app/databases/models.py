from redis.asyncio import StrictRedis, ConnectionPool

from aiocache import cached


class RedisClient:
    def __init__(self, host='localhost', password='', port=6379):
        self.host = host
        self.password = password
        self.port = port
        self.connection: StrictRedis = None
        self.connection_pool = ConnectionPool(
            host=self.host,
            port=self.port,
            password=self.password,
            decode_responses=True
        )

    async def connect(self):
        try:
            self.connection = await StrictRedis(
                connection_pool=self.connection_pool
            ).initialize()
        except ConnectionError as e:
            self.connection = None

    async def disconnect(self):
        if self.connection is None:
            return
        await self.connection.close()
        await self.connection_pool.disconnect()

    @cached(ttl=60)
    async def available_commands(self, group):
        if self.connection is None:
            return
        return await self.connection.lrange(f'group:{group}', 0, -1)


redisClient = RedisClient()

# async def run_test():
#     await redisClient.connect()
#     result = await redisClient.connection.keys('group:*')
#     maxed = max(int(i.split(':')[1]) for i in result)
#     print(maxed)
#
# asyncio.run(run_test())
