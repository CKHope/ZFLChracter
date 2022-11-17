import asyncio
import httpx
import time

start_time = time.time()


async def main():

    async with httpx.AsyncClient() as client:

        for number in range(1, 151):
            pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{number}"

            resp = await client.get(pokemon_url)
            pokemon = resp.json()
            print(pokemon["name"])


asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))
