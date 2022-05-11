#!/usr/bin/python3
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import logging

import requests

from statistics import mean, median, variance

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


#async def get_berries_data(session, url):
#    async with session.get(url) as resp:
#        berry_data = await resp.json()
#            if berry_data.get('growth_time'):
#                return berry_data['growth_time']
#
    
class Statistics(Resource):

    def get(self):

        berries_data = []
        berry_statistics = {}
        berries = requests.get('https://pokeapi.co/api/v2/berry/').json()['results']

        berries_data = self._get_berries_data(berries)
        berry_statistics = self._get_berry_statistics(berries_data)

        return berry_statistics,200

    def _get_berries_data(self, berries):

        berries_data = []
        for berry in berries:
            if berry.get('url') and berry.get('name'):
                berry_growth_time = requests.get(berry['url']).json()['growth_time']
                if berry_growth_time:
                    berries_data.append({'name':berry['name'], 'growth_time': berry_growth_time})

        #async with aiohttp.ClientSession() as session:

        #    tasks = []
        #    for berry in berries:
        #        if berry.get('url') and berry.get('name'):
        #            tasks.append(asyncio.ensure_future(get_berries_data(session,berry['url'])))

        #    growth_values = await asyncio.gather(*tasks)

        #    for growth_value in growth_values:
        #        berries_data.append({'growth_time': growth_value})
                

        return  berries_data
    
    def _get_berry_statistics(self, berries_data):

        berry_statistics = {}
        berry_statistics['berries_names'] = []
        berry_statistics['min_growth_time'] = 0
        berry_statistics['median_growth_time'] = 0
        berry_statistics['max_growth_time'] = 0
        berry_statistics['variance_growth_time'] = 0
        berry_statistics['mean_growth_time'] = 0
        berry_statistics['frequency_growth_time'] = 0

        growth_values = []
        
        #TODO: evaluar que hacer si falta alguna key, se interrumpe la ejecucion?
        for berry in berries_data:
            if berry.get('name'):
                berry_statistics['berries_names'].append(berry['name'])
            if berry.get('growth_time'):
                growth_values.append(berry['growth_time'])

        logging.debug('growth_values: %s' % growth_values)
        growth_values.sort()
        logging.debug('growth_values sorted: %s' % growth_values)

        if growth_values:
            berry_statistics['min_growth_time'] = growth_values[0]
            berry_statistics['max_growth_time'] = growth_values[len(growth_values)-1]
            berry_statistics['mean_growth_time'] = mean(growth_values) 
            berry_statistics['median_growth_time'] = median(growth_values)
            berry_statistics['variance_growth_time'] = variance(growth_values)

        logging.debug(f"berry_statistics: {berry_statistics}")

        return berry_statistics


def main(name):

    app = Flask(name)
    api = Api(app)

    api.add_resource(Statistics, "/allBerryStats")

    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":

    main(__name__)
