from flask import Flask, render_template, jsonify, request
from app.utils.auth_utils import get_token
from flask_cors import CORS
import requests

# Create the Flask app with the template folder specified that will contain your index.html and static folder which will contain your JavaScript files
app = Flask(__name__, template_folder='app/templates', static_url_path='/static')
# By adding CORS(app), you are telling Flask to include CORS headers in responses. The flask_cors extension will add headers such as Access-Control-Allow-Origin: *, allowing requests from any origin.
# This way, when your frontend makes requests to your Flask server, the server will respond with the appropriate CORS headers, and the browser will permit the requests. Since the frontend and backend are on the same origin (domain), you won't encounter CORS issues.
# For more info on CORS goto: https://www.bannerbear.com/blog/what-is-a-cors-error-and-how-to-fix-it-3-ways/
CORS(app)

# This is the route that will serve your index.html template
@app.route('/')
def index():
    return render_template('index.html')

# This is the route that will help you get the token and return it as a JSON response
@app.route('/getToken', methods=['GET'])
def display_token():
    # This makes the call to the get_token function in the auth_utils.py file
    response, status_code = get_token()
    # If the request is successful, return the token
    if status_code == 200:
        api_token = response
        return jsonify({'message': api_token})
    #If the request fails, return the error message
    else:
        return jsonify({'message': response})

# /<float:startLat>/<float:startLong>/<float:endLat>/<float:endLong>
# This is the route that will help you get the token and return it as a JSON response
@app.route('/getRoutes/<startLat>/<startLong>/<endLat>/<endLong>', methods=['GET']) 
def get_routes(startLat, startLong, endLat, endLong):
    
    # get token
    auth_token = get_token()

    headers = {
        'Authorization': 'Bearer ' + str(auth_token)
    }



    url = 'https://api.iq.inrix.com/findRoute?wp_1='+str(startLat)+'%2C'+str(startLong)+'&wp_2='+str(endLat)+'%2C'+str(endLong)+'&format=json'

     # Make the request to the INRIX token endpoint
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses

        data = response.json()
        # Extract the token from the response
        # For more info on how to parse the response, see the json_parser_example.py file
        # token = data['result']['token']
        return data, response.status_code

    except requests.exceptions.RequestException as e:
        return f'Request failed with error: {e}', None
    except (KeyError, ValueError) as e:
        return f'Error parsing JSON: {e}', None
    

# This is the route that will help you get the token and return it as a JSON response
@app.route('/getDrawnRoute/<routeID>', methods=['GET']) 
def get_drawn_routes(routeID):
    
    # get token
    auth_token = get_token()

    headers = {
        'Authorization': 'Bearer ' + str(auth_token)
    }

    url = 'https://api.iq.inrix.com/route?routeId=' + str(routeID) + '&useTraffic=false&routeOutputFields=p&format=json'


    # print(url)
    # requests.get(url, headers=headers)

     # Make the request to the INRIX token endpoint
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses

        data = response.json()
        # Extract the token from the response
        # For more info on how to parse the response, see the json_parser_example.py file
        # token = data['result']['token']
        return data, response.status_code

    except requests.exceptions.RequestException as e:
        return f'Request failed with error: {e}', None
    except (KeyError, ValueError) as e:
        return f'Error parsing JSON: {e}', None





if __name__ == '__main__':
    app.run(debug=False, port=5000)
