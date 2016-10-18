#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

jsonnote = '''[{"@id": ":IPI",
                ":syn": "International Prognosis Index",
                ":value":
                  {":summands": [
                    {":desc": "Ann Arbor stage >= 3"},
                    {":desc": "> 1 extranodal site"},
                    {":desc": "elevated serum LDH"},
                    {":orTerms": [
                      {":desc": "Karnofsky-Index <= 60 %"},
                      {":desc": "ECOG-Score >= 2"}]},
                    {":desc": "age > 60 a"}]},
                "schema:estimatesRiskOf": ":Non-Hodgkin-Lymphom"}]'''

parsednote = json.loads(jsonnote)

def pretty_id(name):
    if name[0] == ':':
        name = name[1:]
        name = name.replace('_', ' ')
    return name

# Calculate the value for a given score entity
# atm using estimatesRiskOf for testing (TODO)
riskForEntity = ":Non-Hodgkin-Lymphom"

def calculate_expression(expression):
    if type(expression) == int:
        return expression
    elif ':desc' in expression:
        return eval(input(expression[':desc'] + '?: '))
    elif ':summands' in expression:
        result = 0
        for summand in expression[':summands']:
            result += calculate_expression(summand)
        return result
    elif ':factors' in expression:
        result = 1
        for factor in expression[':factors']:
            result = result * calculate_expression(factor)
        return result
    elif ':orTerms' in expression:
        result = False
        for orTerm in expression[':orTerms']:
            result = result or calculate_expression(orTerm)
        return int(result)
    else:
        print('not supported operation')

# testing:
expression = {':desc': 'age > 60 a'}
expression = {':orTerms': [expression, {':desc': 'gray hair'}]}
expression = {':factors': [8, expression]}
expression = {':summands': [expression, {':desc': 'elevated LDH'}]}
#print('score: ' + str(calculate_expression(expression)))

def score_value(valueSpec):
    """This functions asks for the necessary input and calculates the value
    for a given value specification of a score"""
    # Error handling; TODO: Use Exceptions!
    specKey = list(key for key in valueSpec)
    if len(specKey) != 1:
        return 'invalid value specification: not 1 key'
    elif specKey[0] not in [':summands', ':factors', ':orTerms']:
        return ('invalid value specification: key is "' + specKey[0] +
                '". It must be ":summands", ":factors" or ":orTerms".')
    else:
        result = calculate_expression(valueSpec)
        return result

for entity in parsednote:
    if 'schema:estimatesRiskOf' in entity and entity['schema:estimatesRiskOf'] == riskForEntity:
        heading = ''
        if '@id' in entity:
            heading += pretty_id(entity['@id'])
        if ':syn' in entity:
            heading += ' (' + entity[':syn'] + ')'
        print(heading)
        if ':value' in entity:
            print('value specification found')
            print(score_value(entity[':value']))
        else:
            print('no value specification fount')

# # agenda
# * also calculate non-integer but floating scores!!! :-D
