#!/usr/bin/python3
'''
module creates route /status on object app_views
'''


from api.v1.views import app_views



@app_views.route('/status')
def app_views():
    return "WE ARE TETSTING"
