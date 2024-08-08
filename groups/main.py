from flask import Flask ,request  # type: ignore
from group_create import createGroup
from sub_group_create import createSubGroup
import os
app = Flask(__name__)

@app.route('/create/group/', methods=['POST'])
def create_group():
    data = request.get_json()
    id = data.get("name")
    responseMsg=createGroup(id)
    return responseMsg
@app.route('/create/subgroup/', methods=['POST'])
def create_sub_group():
    data = request.get_json()
    id = data.get("parent_name")
    sub =data.get("sub_name")
    responseMsg=createSubGroup(id,sub)
    return responseMsg
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=os.getenv('SERVE_PORT','8080'))
