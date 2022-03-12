import json
from Name_and_pricefound import execution_of_orders
from flask import Flask, request, Response
from flask_cors import cross_origin
from run import get_stock_main

app = Flask(__name__)

@app.route("/api/stock/list", methods=['POST'])
#@cross_origin()
def get_stock_list():
    input_json = request.get_json()
    user_name = input_json.get('user_name')
    pass_code = input_json.get('pass_code')
    screener_link = input_json.get('screener_link')
    print(input_json)

    if user_name and pass_code:
        print("getting stock list")
        instance=execution_of_orders()
        instance.login(username=user_name, password=pass_code)
        print('success')
        result = get_stock_main(user_name,pass_code,screener_link,instance)
        output_dict = {
            'data': result
        }
        status = 200
    else:
        print(f"Error: Input JSON is incorrect")
        output_dict = "Wrong input format"
        status = 400

    return Response(json.dumps(output_dict), status, mimetype="application/json")


if __name__ == '__main__':
    app.run(host="10.60.3.213", port="5001", debug=True)
