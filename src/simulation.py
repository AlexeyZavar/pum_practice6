import asyncio
import logging
import random
from dataclasses import dataclass

from src.consts import *


logger = logging.getLogger(__name__)


@dataclass()
class DynamicConfig:
    time_modifier: float = 1


class Person:
    def __init__(self, current_station: 'Station'):
        self.destination: Station = random.choice([station for station in stations if station != current_station])


class Train:
    def __init__(self):
        self.current_station = rokossovskaya
        self.next_station = sobornaya
        self.direction = 1
        self.path_total = 0
        self.people = []

    def unload_people(self):
        s = self.people.copy()

        for person in s:
            if person.destination == self.current_station:
                self.people.remove(person)

    def load_people(self):
        s = self.current_station.people.copy()

        for person in s:
            if len(self.people) >= TRAIN_CAPACITY:
                break

            if (self.current_station < person.destination and self.direction == 1) or \
                    (person.destination < self.current_station and self.direction == -1):
                self.people.append(person)
                self.current_station.remove_person(person)

    def change_direction_if_required(self):
        if self.direction == 1 and self.current_station == biblioteka:
            self.direction = -1
        elif self.direction == -1 and self.current_station == rokossovskaya:
            self.direction = 1

    async def do_stuff(self):
        await asyncio.sleep(0)

        while 1:
            self.unload_people()

            await asyncio.sleep(TRAIN_AFK * DynamicConfig.time_modifier)
            self.change_direction_if_required()

            self.load_people()
            await asyncio.sleep(0)

            self.next_station = stations[self.current_station.idx + self.direction]

            w = paths[self.current_station][self.next_station] / path_length
            for _ in range(100):
                self.path_total += w * self.direction
                await asyncio.sleep(abs(w) * DynamicConfig.time_modifier)

            self.current_station = self.next_station


class Station:
    def __init__(self, name: str, idx: int):
        self.name = name
        self.idx = idx - 1
        self.people = []

    def add_person(self, person: Person):
        self.people.append(person)

    def remove_person(self, person: Person):
        self.people.remove(person)

    async def spawn_people(self):
        while 1:
            self.people.append(Person(self))
            if len(self.people) > PLATFORM_CAPACITY:
                print(f'HAHA DED ON {self.name}')
                exit(666)

            await asyncio.sleep(1 * DynamicConfig.time_modifier)

    def __gt__(self, other):
        return self.idx > other.idx

    def __lt__(self, other):
        return self.idx < other.idx

    def __eq__(self, other):
        return self.idx == other.idx

    def __hash__(self):
        return self.idx

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.name} ({len(self.people)} people)'


rokossovskaya = Station('Rokossovskaya', 1)
sobornaya = Station('Sobornaya', 2)
crystal = Station('Crystal', 3)
zarechnaya = Station('Zarechnaya', 4)
biblioteka = Station('Biblioteka im. Gleba', 5)

stations = [
    rokossovskaya,
    sobornaya,
    crystal,
    zarechnaya,
    biblioteka
]
paths = {
    rokossovskaya: {
        sobornaya: 6 * 60,
    },
    sobornaya: {
        rokossovskaya: 6 * 60,
        crystal: 3 * 60,
    },
    crystal: {
        sobornaya: 3 * 60,
        zarechnaya: 2 * 60,
    },
    zarechnaya: {
        crystal: 2 * 60,
        biblioteka: 7 * 60,
    },
    biblioteka: {
        zarechnaya: 7 * 60,
    }
}

path_length = 18 * 60


class Simulation:
    def __init__(self, trains_count):
        self.trains = [Train() for _ in range(trains_count)]

    async def stats(self):
        while 1:
            logger.info('Stats:')
            logger.info(f'Rosovskaya: {len(rokossovskaya.people)}')
            logger.info(f'Sobornaya: {len(sobornaya.people)}')
            logger.info(f'Crystal: {len(crystal.people)}')
            logger.info(f'Zarechnaya: {len(zarechnaya.people)}')
            logger.info(f'Biblioteka: {len(biblioteka.people)}')

            for train in self.trains:
                logger.info(f'Train: {len(train.people)} people, on {train.current_station.name}, {train.path_total}% of the way')

            await asyncio.sleep(2)

    async def run(self):
        interval = 38 * 60 / len(self.trains)

        trains_tasks = []

        for item in self.trains:
            trains_tasks.append(asyncio.create_task(item.do_stuff()))
            await asyncio.sleep(interval * DynamicConfig.time_modifier)

        stations_tasks = [asyncio.create_task(station.spawn_people()) for station in stations]
        await asyncio.sleep(0)

        tasks = stations_tasks + trains_tasks
        tasks.append(asyncio.create_task(self.stats()))

        await asyncio.gather(*tasks)
