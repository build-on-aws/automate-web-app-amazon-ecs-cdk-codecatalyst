# Copyright 2015. Amazon Web Services, Inc. All Rights Reserved.
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

import os
import sys
import json

import flask
from flask import request, Response

import boto3

print("Configue the application")
# Default config vals
THEME = 'default' if os.environ.get('THEME') is None else os.environ.get('THEME')
FLASK_DEBUG = 'false' if os.environ.get('FLASK_DEBUG') is None else os.environ.get('FLASK_DEBUG')

# Create the Flask app
application = flask.Flask(__name__)

# Load config values specified above
application.config.from_object(__name__)

# Load configuration vals from a file
application.config.from_pyfile('application.config', silent=True)

# Only enable Flask debugging if an env var is set to true
application.debug = application.config['FLASK_DEBUG'] in ['true', 'True']

# Connect to DynamoDB and get refo to Table
print("Connect to DynamoDB")
ddb    = boto3.resource('dynamodb', region_name=application.config['AWS_REGION'])
client = boto3.client('dynamodb', region_name=application.config['AWS_REGION'])

@application.route('/')
def welcome():
    theme = application.config['THEME']
    return flask.render_template('index.html', theme=theme, flask_debug=application.debug)


@application.route('/signup', methods=['POST'])
def signup():
    signup_data = dict()
    for item in request.form:
        signup_data[item] = request.form[item]

    # try:
    #     store_in_dynamo(signup_data)
    # except client.exceptions.ConditionalCheckFailedException:
    #     return Response("", status=409, mimetype='application/json')

    return Response(json.dumps(signup_data), status=201, mimetype='application/json')


def store_in_dynamo(signup_data):
    table = ddb.Table(application.config['STARTUP_SIGNUP_TABLE'])
    table.put_item(
        Item=signup_data
    )
    print("PutItem succeeded:")


# def create_table():
#     ddb.create_table(
#         TableName=application.config['STARTUP_SIGNUP_TABLE'], 
#         AttributeDefinitions=[
#             {
#                 'AttributeName': 'email',
#                 'AttributeType': 'S'
#             }
#         ],
#         KeySchema=[
#             {
#                 'AttributeName': 'email',
#                 'KeyType': 'HASH'
#             }
#         ], 
#         BillingMode='PAY_PER_REQUEST'
#     )


# def init_db():
#     try:
#         print("Check DynamoDB table")
#         response = client.describe_table(TableName=application.config['STARTUP_SIGNUP_TABLE'])
#     except client.exceptions.ResourceNotFoundException as err:
#         print("DynamoDB table doesn't exist, please create as part of the guide")
#         # create_table()

if __name__ == '__main__':
    init_db()
    application.run(host='0.0.0.0')
