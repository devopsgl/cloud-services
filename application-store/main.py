import os
from flask import Flask, request
from application_list import storeList
from get_values import getValues
from put_values import putValues
from flask_cors import CORS
import requests

GIT_API_URL = os.getenv('GIT_API_URL', 'no url') 
GIT_ACCESS_TOKEN = os.getenv('GIT_ACCESS_TOKEN', 'no token') 

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/application/list', methods=['GET'])
def getList(): 
    return storeList(GIT_API_URL,GIT_ACCESS_TOKEN)

@app.route('/application/<application_id>/tag/<application_tag>', methods=['GET'])
def getValuesFile(application_id,application_tag): 
    return getValues(GIT_API_URL,GIT_ACCESS_TOKEN,application_id,application_tag)

@app.route('/application', methods=['PUT'])
def putApplication(): 
	repository_id = request.args.get('repositoryId')
	repository_tag = request.args.get('repositoryTag')
	user_group_id = request.args.get('userGroupId')
	service_name = request.args.get('serviceName')
	return putValues(GIT_API_URL,GIT_ACCESS_TOKEN,repository_id,repository_tag,user_group_id,service_name)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=os.getenv('SERVE_PORT','8081'))