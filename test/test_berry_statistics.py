#!/usr/bin/env python3

import pytest

import os
import sys
sys.path.append('../src')

import poke_stats_api 

def test_berry_statistics_success():
#    berries_names: list
#    min_growth_time: time, int
#    median_growth_time: time, float
#    max_growth_time: time, int
#    variance_growth_time: time, float
#    mean_growth_time: time, float
#    frequency_growth_time: time, {growth_time: frequency, ...}

    r = [{'name': 'cheri', 'growth_time': 3}, {'name': 'chesto', 'growth_time': 1}, {'name': 'pecha', 'growth_time': 8}, {'name': 'lum', 'growth_time': 12}]

    stats = poke_stats_api.Statistics()
    result = stats._get_berry_statistics(r)
#{'berries_names': ['cheri', 'chesto', 'pecha', 'lum'], 'min_growth_time': 1, 'median_growth_time': 5.5, 'max_growth_time': 12, 'variance_growth_time': 24.666666666666668, 'mean_growth_time': 6, 'frequency_growth_time': 0}

    #assert result['berries_names'] == ['cheri', 'chesto', 'pecha', 'lum']
    #assert result['min_growth_time'] == 1
    #assert result['max_growth_time'] == 12
    #assert result['mean_growth_time'] == 5.5
    #assert result['median_growth_time'] == 6
    #assert result['variance_growth_time'] == 24.67 


def test_berry_statistics_with_empty_berry_data():

    stats = poke_stats_api.Statistics()
    result = stats._get_berry_statistics([])

    assert result['berries_names'] == []
    assert result['min_growth_time'] == 0
    assert result['max_growth_time'] == 0
    assert result['mean_growth_time'] == 0
    assert result['median_growth_time'] == 0
    assert result['variance_growth_time'] == 0


def test_berry_statistics_with_missing_name_key_on_berry_data():

    r = [{'name': 'cheri', 'growth_time': 3}, {'name': 'chesto'}, {'name': 'pecha', 'growth_time': 8}, {'name': 'lum', 'growth_time': 12}]

    stats = poke_stats_api.Statistics()
    result = stats._get_berry_statistics(r)


def test_berry_statistics_with_missing_growth_time_key_on_berry_data():

    r = [{'name': 'cheri', 'growth_time': 3}, {'growth_time': 1}, {'name': 'pecha', 'growth_time': 8}, {'name': 'lum', 'growth_time': 12}]

    stats = poke_stats_api.Statistics()
    result = stats._get_berry_statistics(r)

