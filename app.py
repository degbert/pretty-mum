from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
#from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection


from datetime import datetime
import certifi

app = Flask(__name__)
bootstrap = Bootstrap(app)

# auth = AWSRequestsAuth(aws_access_key='ASIAI3H3JWO27VSDYZ4A',
#                        aws_secret_access_key='NCsQTFMJOWfOBxeFODuonkFZl7D7njNWVmiitqDs',
#                        aws_token="FQoDYXdzEGQaDLDi4aLiUk8QN9XmHiKsAa67LDguPEJxD6f+IVjvwxxhdnfyDAPABDlzGo2yBxOvw7wKEdU7Zuc1xwqUxDfoa5YOu8GyCWFciifVT4S99KGPzGIhBB+fhlXy52tkTGyLyhEjFkUTkpSz0nEEY0oe7nsSCsLBi+Hupjz8zTwNL4O9AgFVAjcKRhbduCTRo8C1jxAKBcN8kVA74aBQehvJn4PjcHdm9oMypCu8Wc5N6RSc+QJ4MI6qpUoSYTso9qffzgU=",
#                        aws_host='https://search-elasticsearch-prod00-uaiyztdprcfqlukwr3xiequjzm.us-east-1.es.amazonaws.com',
#                        aws_region='us-east-1',
#                        aws_service= 'es')

es = Elasticsearch(
    ['https://search-elasticsearch-prod00-uaiyztdprcfqlukwr3xiequjzm.us-east-1.es.amazonaws.com'],
    port=443)
    #connection_class=RequestsHttpConnection,
    #http_auth=auth)

test = {}

@app.route('/')
def hello_world():
    result = es.search(index='schedule_overtime*',
                       body={
                           "query": {
                               "match_all": {}}
                       }
                       )
    result_list = result['hits']['hits']
    parsed_result_list = []
    counter = 0
    for i in result_list:
        for k,v in i.items():
            if counter == 4:
                parsed_result_list.append(v)
            counter +=1
            if counter == 5:
                counter = 0

    print(parsed_result_list)
    return render_template('base.html',
                           the_result = 'blah')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
