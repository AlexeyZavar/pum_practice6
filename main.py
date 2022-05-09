import asyncio

from src import Simulation, DynamicConfig
from src.visualization import visualize


async def main():
    loop = asyncio.get_event_loop()

    DynamicConfig.time_modifier = 0.005
    simulation = Simulation(14)

    t1 = loop.create_task(simulation.run(), name='Simulation')
    t2 = loop.create_task(visualize(simulation), name='Visualization')

    await asyncio.gather(t1, t2)

if __name__ == "__main__":
    asyncio.run(main())
