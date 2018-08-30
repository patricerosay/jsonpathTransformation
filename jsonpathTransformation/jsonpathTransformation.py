#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from pprint import pprint
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse
import fileinput
import re


def parseJsonPathExpression(data, jsonPathExpression):
    """
    Extract a json attribute with a jsonpath expression

    Parameters
    ----------
    data : obj
        a json object containing the data

    jsonPathExpression : string
        a json path string

    Examples
    --------
    >>> data ={"header": {"creationDate": "2018-05-29T12:41:08,306+02:00","updateDate": "2018-05-29T12:41:08,306+02:00", "producer": "vt1","versionSchema": "null"},"smartData": {"label": "%00004410012500000016906834250","zipCode": "000044100","itemId": "12500000016906","itemIdCCKey": "A","serviceCode": "834","countryCode": "250","LetterUUID": "7edb06eb-2298-34b9-a9f5-cf47f645a6b6"}	}
    >>> jsonPathExpression ='$.smartData.LetterUUID'
    >>> parseJsonPathExpression(data,jsonPathExpression)
    ['7edb06eb-2298-34b9-a9f5-cf47f645a6b6']
    """
    jsonpath_expr = parse(jsonPathExpression)
    res = ([match.value for match in jsonpath_expr.find(data)])
    return ([match.value for match in jsonpath_expr.find(data)])


def extractFromFileJsonPathExpression(json_filepath, jsonPathExpression, verbose=True):

    with open(json_filepath, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
    res = parseJsonPathExpression(data, jsonPathExpression)
    if verbose:
        print(res)
    return res


def transform(jsonData, jsonTransfo, containingExpression, verbose):
    """
    Transform a json into another json with a json transformatino file

    Parameters
    ----------
    jsonData : obj
        a json object containing the data

    jsonTransfo : obj
        a json object containing the transformation
    containingExpression: str
        a regular expression
    Examples
    --------
    >>> jsonData ={"header": {"creationDate": "2018-05-29T12:41:08,306+02:00","updateDate": "2018-05-29T12:41:08,306+02:00", "producer": "vt1","versionSchema": "null"},"smartData": {"label": "%00004410012500000016906834250","zipCode": "000044100","itemId": "12500000016906","itemIdCCKey": "A","serviceCode": "834","countryCode": "250","LetterUUID": "7edb06eb-2298-34b9-a9f5-cf47f645a6b6"}	}
    >>> jsonTransfo ={"data": {"uuid": "$.smartData.LetterUUID","UUID": "$.smartData.itemId"}}
    >>> containingExpression=r"(\$.*)"
    >>> transform(jsonData,jsonTransfo,containingExpression)
    {'data': {'uuid': '7edb06eb-2298-34b9-a9f5-cf47f645a6b6', 'UUID': '12500000016906'}}

    >>> jsonData ={"header": {"creationDate": "2018-05-29T12:41:08,306+02:00","updateDate": "2018-05-29T12:41:08,306+02:00", "producer": "vt1","versionSchema": "null"},"smartData": {"label": "%00004410012500000016906834250","zipCode": "000044100","itemId": "12500000016906","itemIdCCKey": "A","serviceCode": "834","countryCode": "250","LetterUUID": "7edb06eb-2298-34b9-a9f5-cf47f645a6b6"}	}
    >>> jsonTransfo ={"data": {"uuid": "vdspService/$.smartData.LetterUUID","UUID": "vdspService/$.smartData.itemId"}}
    >>> containingExpression=r"vdspService\/(.*)\)*"
    >>> transform(jsonData,jsonTransfo,containingExpression)
    {'data': {'uuid': '7edb06eb-2298-34b9-a9f5-cf47f645a6b6', 'UUID': '12500000016906'}}
    """
    data = jsonData
    transfo = jsonTransfo
    regex = containingExpression

    def innerTransform(nodeValue, nodeName, parent):
        global lineCount
        global errorCount
        if isinstance(nodeValue, dict):
            for name, item in nodeValue.items():
                innerTransform(item, name, nodeValue)
        elif isinstance(nodeValue, list):
            for el in nodeValue:
                innerTransform(el, None, nodeValue)
        elif isinstance(nodeValue, str):
            try:
                lineCount = lineCount+1
                matches = re.search(regex, nodeValue)
                match = matches.group(1)
                if match is not None:
                    jsonpath_expr = parse(match)
                    found = False
                    for match in jsonpath_expr.find(data):
                        parent[nodeName] = match.value
                        found = True
                        if(verbose):
                            print(nodeName + ' : ' + match.value)
                    if not found:
                        errorCount = errorCount+1

            except:
                parent[nodeName] = nodeValue
                if(verbose):
                    traceback.print_exception(*exc_info)
                    print(nodeName + ' : ' + nodeValue)
                errorCount = errorCount+1

    innerTransform(transfo, None, None)
    return transfo


def parseJsonPathTransformationFile(json_filepath, jsonPathTransformationFile, outputFile, verbose=False, expr='(\$.*)'):

    with open(json_filepath, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
    dataTemp = ''
    for line in fileinput.input(files=json_filepath):
        dataTemp = dataTemp+re.sub(': null', ': "null"', line.rstrip())

    data = json.loads(dataTemp)

    transfoTempData = ''

    for line in fileinput.input(files=jsonPathTransformationFile):
        transfoTempData = transfoTempData+line.rstrip()

    transfo = json.loads(transfoTempData)

    transform(data, transfo, expr, verbose)
    if(outputFile is not None):
        with open(outputFile, 'w') as f:
            json.dump(transfo, f, ensure_ascii=False, indent=2)
    else:
        pprint(transfo)

    print('{} errors / {} total processed lines'.format(errorCount, lineCount))


def _test():
    import doctest
    doctest.testmod()


def main(json_filepath, jsonPathExpression, jsonPathTransformationFile, outputFile, verbose):
    if (jsonPathExpression is not None):
        parseJsonPathExpression(json_filepath, jsonPathExpression)
    elif (jsonPathTransformationFile is not None):
        parseJsonPathTransformationFile(
            json_filepath, jsonPathTransformationFile, outputFile, verbose)
    else:
        print("Error")




errorCount = 0
lineCount = 0

