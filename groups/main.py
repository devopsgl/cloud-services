from flask import Flask
from create import createGroup
import os
app = Flask(__name__)

@app.route('/create/group/<string:id>', methods=['GET'])
def get_user(id):
    responseMsg=createGroup(id)
    return responseMsg

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=os.getenv('SERVE_PORT','8080'))
