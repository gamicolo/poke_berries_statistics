#!/usr/bin/env python3

import pytest

import os
import sys
sys.path.append('../src')

import poke_stats_api 

def test_berry_statistics_success():

    r = [{'name': 'cheri', 'growth_time': 3}, {'name': 'chesto', 'growth_time': 1}, {'name': 'pecha', 'growth_time': 8}, {'name': 'lum', 'growth_time': 12}]

    stats = poke_stats_api.Statistics()
    result = stats._get_berry_statistics(r)

    assert result['berries_names'] == ['cheri', 'chesto', 'pecha', 'lum']
    assert result['min_growth_time'] == 1
    assert result['max_growth_time'] == 12
    assert result['mean_growth_time'] == 6
    assert result['median_growth_time'] == 5.5
    assert result['variance_growth_time'] == 24.666666666666668

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

    assert result['berries_names'] == ['cheri', 'pecha', 'lum']
    assert result['min_growth_time'] == 3
    assert result['max_growth_time'] == 12
    assert result['mean_growth_time'] == 7.666666666666667
    assert result['median_growth_time'] == 8
    assert result['variance_growth_time'] == 20.333333333333336


def test_berry_statistics_with_missing_growth_time_key_on_berry_data():

    r = [{'name': 'cheri', 'growth_time': 3}, {'growth_time': 1}, {'name': 'pecha', 'growth_time': 8}, {'name': 'lum', 'growth_time': 12}]

    stats = poke_stats_api.Statistics()
    result = stats._get_berry_statistics(r)

    assert result['berries_names'] == ['cheri', 'pecha', 'lum']
    assert result['min_growth_time'] == 3
    assert result['max_growth_time'] == 12
    assert result['mean_growth_time'] == 7.666666666666667
    assert result['median_growth_time'] == 8
    assert result['variance_growth_time'] == 20.333333333333336

def test_berry_statistics_frequency_growth_time_berries_with_single_frecuency():

    r = [{'name': 'cheri', 'growth_time': 3}, {'name': 'pecha', 'growth_time': 8}, {'name': 'lum', 'growth_time': 12}]

    stats = poke_stats_api.Statistics()
    result = stats._get_berry_statistics(r)

    assert result['frequency_growth_time'] == { 3: 1, 8: 1, 12: 1 }

def test_berry_statistics_frequency_growth_time_berries_without_single_frecuency():

    r = [{'name': 'cheri', 'growth_time': 3}, {'name': 'pecha', 'growth_time': 3}, {'name': 'lum', 'growth_time': 12}]

    stats = poke_stats_api.Statistics()
    result = stats._get_berry_statistics(r)

    assert result['frequency_growth_time'] == { 3: 2, 12: 1 }
