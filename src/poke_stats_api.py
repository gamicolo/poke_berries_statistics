#!/usr/bin/python3
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import logging

import requests

from statistics import mean, median, variance

import aiohttp
import asyncio

from typing import List

#logging.basicConfig(level=logging.DEBUG, filename='stats.log', filemode='w', format='%(asctime)s %(name)s %(levelname)s %(message)s')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s %(message)s')

logger = logging.getLogger('berry_statistics')

#def get_statistics():
#    berries_names: list
#    min_growth_time: time, int
#    median_growth_time: time, float
#    max_growth_time: time, int
#    variance_growth_time: time, float
#    mean_growth_time: time, float
#    frequency_growth_time: time, {growth_time: frequency, ...}


async def get_berry_data(session, url: str) -> dict:

    """ Get the information name and growth_time of a berry """

    async with session.get(url) as resp:
        berry_data = await resp.json()
        if berry_data.get('name') and berry_data.get('growth_time'):
            return { 'name': berry_data['name'], 'growth_time': berry_data['growth_time'] }

async def get_berries_data(urls: List[dict]) -> List[dict]:

    """ Get the information of a list of berries """

    berries_data = []
    async with aiohttp.ClientSession() as session:

        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(get_berry_data(session, url)))

        berries_data = await asyncio.gather(*tasks)

    return berries_data
    
class Statistics(Resource):

    def get(self) -> dict:

        """ Get the data and statistics off all berries from the Poke API """

        berries_data = []
        berry_statistics = {}
        berries = requests.get('https://pokeapi.co/api/v2/berry/').json()['results']

        berries_data = self._get_berries_data(berries)
        berry_statistics = self._get_berry_statistics(berries_data)

        return berry_statistics,200

    def _get_berries_data(self, berries: List[dict]) -> List[dict]:

        """ Get the data from a list of berries """

        urls = []
        berries_data = []
        for berry in berries:
            if berry.get('url'):
                urls.append(berry['url'])

        berries_data = asyncio.run(get_berries_data(urls))

        logging.debug(f"Berries data gathered: {berries_data}")

        return  berries_data
    
    def _get_berry_statistics(self, berries_data: List[dict]) -> dict:

        """ Get the statistics from a list of berries """

        berry_statistics = {}
        berry_statistics['berries_names'] = []
        berry_statistics['min_growth_time'] = 0
        berry_statistics['median_growth_time'] = 0.0
        berry_statistics['max_growth_time'] = 0
        berry_statistics['variance_growth_time'] = 0.0
        berry_statistics['mean_growth_time'] = 0.0
        berry_statistics['frequency_growth_time'] = {}

        growth_values = []
        
        for berry in berries_data:
            if berry.get('name') and berry.get('growth_time'):
                berry_statistics['berries_names'].append(berry['name'])
                growth_values.append(berry['growth_time'])
                if berry_statistics['frequency_growth_time'].get(berry['growth_time']):
                    berry_statistics['frequency_growth_time'][berry['growth_time']] += 1
                else:
                    berry_statistics['frequency_growth_time'][berry['growth_time']] = 1

        growth_values.sort()

        if growth_values:
            berry_statistics['min_growth_time'] = growth_values[0]
            berry_statistics['max_growth_time'] = growth_values[len(growth_values)-1]
            berry_statistics['mean_growth_time'] = mean(growth_values) 
            berry_statistics['median_growth_time'] = median(growth_values)
            berry_statistics['variance_growth_time'] = variance(growth_values)

        logging.debug(f"berry_statistics: {berry_statistics}")

        return berry_statistics


def main(name: str) -> None:

    app = Flask(name)
    api = Api(app)

    api.add_resource(Statistics, "/allBerryStats")

    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":

    main(__name__)
