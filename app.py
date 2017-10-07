from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection


from datetime import datetime
import certifi

app = Flask(__name__)
bootstrap = Bootstrap(app)

#test_data = [{'log_date': '2017-10-02', 'chain': 'SavaSeniorCare', 'org': 'SAVA - Glen Burnie', 'v2_shift_overtime_accepted': 18, 'other_overtime_accepted': 25, 'v2_shift_overtime_declined': 0, 'other_overtime_declined': 0, 'avg_alt_workers_per_study': 44.5, 'shift_request_messages': 25, 'response_messages': 1, 'avg_time_sched_before': -9.084523999182215, 'avg_time_sched_before_count': 42, 'avg_time_sched_after': 2.485437644675926, 'avg_time_sched_after_count': 1, 'avg_time_sched_total': -8.815455123743654, 'avg_shift_request_messages_per_study': 0.1}, {'log_date': '2017-10-02', 'chain': 'SavaSeniorCare', 'org': 'SAVA - Matador', 'v2_shift_overtime_accepted': 26, 'other_overtime_accepted': 0, 'v2_shift_overtime_declined': 4, 'other_overtime_declined': 0, 'avg_alt_workers_per_study': 4.0, 'shift_request_messages': 0, 'response_messages': 0, 'avg_time_sched_before': -9.29889634874132, 'avg_time_sched_before_count': 24, 'avg_time_sched_after': 0.7822088623046874, 'avg_time_sched_after_count': 2, 'avg_time_sched_total': -8.523426717122396, 'avg_shift_request_messages_per_study': 0.0}, {'log_date': '2017-10-02', 'chain': 'SavaSeniorCare', 'org': 'SAVA - Greenhills', 'v2_shift_overtime_accepted': 16, 'other_overtime_accepted': 3, 'v2_shift_overtime_declined': 1, 'other_overtime_declined': 0, 'avg_alt_workers_per_study': 12.8, 'shift_request_messages': 2, 'response_messages': 0, 'avg_time_sched_before': -15.838080907751012, 'avg_time_sched_before_count': 16, 'avg_time_sched_after': 0.0, 'avg_time_sched_after_count': 0, 'avg_time_sched_total': -15.838080907751012, 'avg_shift_request_messages_per_study': 0.0}, {'log_date': '2017-10-02', 'chain': 'SavaSeniorCare', 'org': 'SAVA - Mooresville', 'v2_shift_overtime_accepted': 0, 'other_overtime_accepted': 16, 'v2_shift_overtime_declined': 0, 'other_overtime_declined': 0, 'avg_alt_workers_per_study': 14.8, 'shift_request_messages': 4, 'response_messages': 0, 'avg_time_sched_before': -16.114915952329284, 'avg_time_sched_before_count': 16, 'avg_time_sched_after': 0.0, 'avg_time_sched_after_count': 0, 'avg_time_sched_total': -16.114915952329284, 'avg_shift_request_messages_per_study': 0.0}, {'log_date': '2017-10-02', 'chain': 'SavaSeniorCare', 'org': 'SAVA - North Park', 'v2_shift_overtime_accepted': 13, 'other_overtime_accepted': 0, 'v2_shift_overtime_declined': 0, 'other_overtime_declined': 0, 'avg_alt_workers_per_study': 12.1, 'shift_request_messages': 7, 'response_messages': 0, 'avg_time_sched_before': -5.953543440772597, 'avg_time_sched_before_count': 13, 'avg_time_sched_after': 0.0, 'avg_time_sched_after_count': 0, 'avg_time_sched_total': -5.953543440772597, 'avg_shift_request_messages_per_study': 0.0}, {'log_date': '2017-10-02', 'chain': 'SavaSeniorCare', 'org': 'SAVA - Pearl Street', 'v2_shift_overtime_accepted': 11, 'other_overtime_accepted': 0, 'v2_shift_overtime_declined': 0, 'other_overtime_declined': 0, 'avg_alt_workers_per_study': 14.8, 'shift_request_messages': 0, 'response_messages': 0, 'avg_time_sched_before': -4.537089723186728, 'avg_time_sched_before_count': 9, 'avg_time_sched_after': 0.20294422290943287, 'avg_time_sched_after_count': 2, 'avg_time_sched_total': -3.6752653693510626, 'avg_shift_request_messages_per_study': 0.0}, {'log_date': '2017-10-02', 'chain': 'SavaSeniorCare', 'org': 'SAVA - Cambridge North', 'v2_shift_overtime_accepted': 7, 'other_overtime_accepted': 2, 'v2_shift_overtime_declined': 0, 'other_overtime_declined': 0, 'avg_alt_workers_per_study': 12.333333333333334, 'shift_request_messages': 8, 'response_messages': 0, 'avg_time_sched_before': -5.658045227301955, 'avg_time_sched_before_count': 9, 'avg_time_sched_after': 0.0, 'avg_time_sched_after_count': 0, 'avg_time_sched_total': -5.658045227301955, 'avg_shift_request_messages_per_study': 0.0}, {'log_date': '2017-10-02', 'chain': 'SavaSeniorCare', 'org': 'SAVA - Cheyenne', 'v2_shift_overtime_accepted': 1, 'other_overtime_accepted': 8, 'v2_shift_overtime_declined': 0, 'other_overtime_declined': 0, 'avg_alt_workers_per_study': 27.77777777777778, 'shift_request_messages': 1, 'response_messages': 0, 'avg_time_sched_before': -2.5883308215985084, 'avg_time_sched_before_count': 9, 'avg_time_sched_after': 0.0, 'avg_time_sched_after_count': 0, 'avg_time_sched_total': -2.5883308215985084, 'avg_shift_request_messages_per_study': 0.0}, {'log_date': '2017-10-02', 'chain': 'SavaSeniorCare', 'org': 'SAVA - First Colony', 'v2_shift_overtime_accepted': 7, 'other_overtime_accepted': 0, 'v2_shift_overtime_declined': 2, 'other_overtime_declined': 0, 'avg_alt_workers_per_study': 20.11111111111111, 'shift_request_messages': 2, 'response_messages': 0, 'avg_time_sched_before': -5.725419818535053, 'avg_time_sched_before_count': 7, 'avg_time_sched_after': 0.0, 'avg_time_sched_after_count': 0, 'avg_time_sched_total': -5.725419818535053, 'avg_shift_request_messages_per_study': 0.0}, {'log_date': '2017-10-02', 'chain': 'SavaSeniorCare', 'org': 'SAVA - Sheridan', 'v2_shift_overtime_accepted': 2, 'other_overtime_accepted': 6, 'v2_shift_overtime_declined': 1, 'other_overtime_declined': 0, 'avg_alt_workers_per_study': 10.555555555555555, 'shift_request_messages': 2, 'response_messages': 0, 'avg_time_sched_before': -13.23143482349537, 'avg_time_sched_before_count': 2, 'avg_time_sched_after': 0.0, 'avg_time_sched_after_count': 0, 'avg_time_sched_total': -13.23143482349537, 'avg_shift_request_messages_per_study': 0.0}]

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
                           "from": 0, "size": 10000,
                           "query": {
                               "match_all": {}}
                            }
                       )
    result_list = result['hits']['hits']
    parsed_result_list = []
    parsed_category_list = result['hits']['hits'][0]['_source'].keys()
    counter = 0
    for i in result_list:
        for k,v in i.items():
            if counter == 4:
                parsed_result_list.append(v.values())
            counter +=1
            if counter == 5:
                counter = 0
    print(parsed_category_list)
    #print(parsed_result_list)
    return render_template('result.html',
                           the_category = parsed_category_list,
                           the_result = parsed_result_list)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
