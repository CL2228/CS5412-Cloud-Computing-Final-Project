import asyncio
import time


async def sleep(n: int):
    print("Sleep round: {}".format(n))
    await asyncio.sleep(1)
    return n


async def func(li):
    for i in range(len(li)):
        print("element: {}".format(li[i]))
        res = await sleep(i)
        print(res)
    print("task:{} completed".format(li))


async def main():
    t1 = asyncio.create_task(func(['q','w','e']))
    t2 = asyncio.create_task(func(['a','s','d']))
    await t1
    await t2


if __name__ == "__main__":
    # loop1 = asyncio.get_event_loop()
    # loop1.run_until_complete(func(["q", "w", "e"]))
    asyncio.run(main())

