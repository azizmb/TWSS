#!/usr/bin/env python
#
# Copyright 2010 Brian McKenna, Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This code is based on a Python library written by Brian McKenna which
# can be found at http://gist.github.com/407134.


"""This module provides an interface to the Google Prediction API.
"""


__author__ = 'Brian McKenna, Robert Kaplow'

import cgi
from getpass import getpass
import urllib
import urllib2
try:
  import json
except ImportError:
  from django.utils import simplejson as json


def GetAuthentication(email, password):
  """Retrieves a Google authentication token.
  """

  url = 'https://www.google.com/accounts/ClientLogin'
  post_data = urllib.urlencode([
      ('Email', email),
      ('Passwd', password),
      ('accountType', 'HOSTED_OR_GOOGLE'),
      ('source', 'companyName-applicationName-versionID'),
      ('service', 'xapi'),
  ])

  request = urllib2.Request(url, post_data)
  response = urllib2.urlopen(request)

  content = '&'.join(response.read().split())
  query = cgi.parse_qs(content)
  auth = query['Auth'][0]

  response.close()
  return auth


def Train(auth, datafile):
  """Tells the Google Prediction API to train the supplied data file.
  """

  url = ('https://www.googleapis.com/prediction/v1.1/training?data='
         '%s' % urllib.quote(datafile, ''))

  headers = {
      'Content-Type': 'application/json',
      'Authorization': 'GoogleLogin auth=%s' % auth,
  }

  post_data = json.dumps({
      'data': {},
  })

  request = urllib2.Request(url, post_data, headers)
  response = urllib2.urlopen(request)
  response.close()


def Predict(auth, model, query):
  """
  Makes a prediction based on the supplied model and query data. The query needs
  to be a list, where the elements in the list are the features in the dataset.
  The return is a tuple [prediction, scores], where:
  In a classification task, prediction is the most likely label, and scores is
  a dictionary mapping labels to scores.
  In a regression task, prediction is the real-valued prediction for the input
  data, and scores is an empty list.
  """

  url = ('https://www.googleapis.com/prediction/v1.1/training/'
         '%s/predict' % urllib.quote(model, ''))

  headers = {
      'Content-Type': 'application/json',
      'Authorization': 'GoogleLogin auth=%s' % auth,
  }

  post_data = GetPostData(query)

  request = urllib2.Request(url, post_data, headers)
  response = urllib2.urlopen(request)
  content = response.read()
  response.close()

  json_content = json.loads(content)['data']

  scores = []
  print json.loads(content)
  # classification task
  if 'outputLabel' in json_content:
    prediction = json_content['outputLabel']
    jsonscores = json_content['outputMulti']
    scores = ExtractDictScores(jsonscores)
  # regression task
  else:
    prediction = json_content['outputValue']

  return [prediction, scores]


def ExtractDictScores(jsonscores):

  scores = {}
  for pair in jsonscores:
    for key, value in pair.iteritems():
      if key == 'label':
        label = value
      elif key == 'score':
        score = value
    scores[label] = score
  return scores


def GetPostData(query):
  data_input = {}
  data_input['mixture'] = query

  post_data = json.dumps({
      'data': {
          'input': data_input
              }
  })
  return post_data


def main():
  """Asks for the user's Google credentials, Prediction API model and queries.
  """

  google_email = raw_input('Email: ')
  google_password = getpass('Password: ')
  auth = GetAuthentication(google_email, google_password)
  model = raw_input('Model: ')

  query = []
  message = 'Enter feature for classification. Type quit when done: '
  while True:
    feature = raw_input(message)
    if feature == 'quit':
      break
    try:
      float(feature)
      query.append(float(feature))
    except ValueError:
      query.append(feature)
  print query
  print Predict(auth, model, query)


if __name__ == '__main__':
  main()
