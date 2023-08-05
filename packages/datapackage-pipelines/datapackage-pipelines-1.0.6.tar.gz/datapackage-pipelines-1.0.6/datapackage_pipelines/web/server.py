import datetime

import slugify
import yaml
from flask import Flask, render_template, abort, redirect
from flask_cors import CORS
from flask_jsonpify import jsonify

from datapackage_pipelines.status import status

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app)


def datestr(x):
    return str(datetime.datetime.fromtimestamp(x))


def yamlize(x):
    ret = yaml.dump(x, default_flow_style=False)
    return ret


@app.route("/")
def main():
    statuses = sorted(status.all_statuses(), key=lambda x: x.get('id'))
    for pipeline in statuses:
        for key in ['ended', 'last_success', 'started']:
            if pipeline.get(key):
                pipeline[key] = datestr(pipeline[key])
        pipeline['class'] = {'INIT': 'primary',
                             'REGISTERED': 'primary',
                             'INVALID': 'danger',
                             'RUNNING': 'warning',
                             'SUCCEEDED': 'success',
                             'FAILED': 'danger'
                             }[pipeline.get('state', 'INIT')]

        pipeline['slug'] = slugify.slugify(pipeline['id'])

    def state_and_not_dirty(state, p):
        return p.get('state') == state and not p.get('dirty')

    def state_or_dirty(state, p):
        return p.get('state') == state or p.get('dirty')

    categories = [
        ['REGISTERED', 'Waiting to run', state_or_dirty],
        ['INVALID', 'Failed validation', state_and_not_dirty],
        ['RUNNING', 'Running', state_and_not_dirty],
        ['SUCCEEDED', 'Successful Execution', state_and_not_dirty],
        ['FAILED', 'Failed Execution', state_and_not_dirty]
    ]
    for item in categories:
        item.append([p for p in statuses
                     if item[2](item[0], p)])
        item.append(len(item[-1]))
    return render_template('dashboard.html',
                           categories=categories,
                           yamlize=yamlize)


@app.route("/api/<field>/<path:pipeline_id>")
def pipeline_api(field, pipeline_id):
    fields = {
        'log': 'reason',
        'pipeline': 'pipeline',
        'source': 'source'
    }
    field = fields.get(field)
    if not pipeline_id.startswith('./'):
        pipeline_id = './' + pipeline_id
    pipeline_status = status.get_status(pipeline_id)
    if pipeline_status is None or field is None:
        abort(404)
    ret = pipeline_status[field]
    if field != 'reason':
        ret = yamlize(ret)
    ret = ret.split('\n')
    ret = {'text': ret}
    return jsonify(ret)


@app.route("/badge/<path:pipeline_id>")
def badge(pipeline_id):
    if not pipeline_id.startswith('./'):
        pipeline_id = './' + pipeline_id
    pipeline_status = status.get_status(pipeline_id)
    if pipeline_status is None:
        abort(404)
    status_text = pipeline_status.get('message')
    success = pipeline_status.get('success')
    if success is True:
        record_count = pipeline_status.get('stats', {}).get('total_row_count')
        if record_count is not None:
            status_text += ' (%d records)' % record_count
        status_color = 'brightgreen'
    elif success is False:
        status_color = 'red'
    else:
        status_color = 'lightgray'
    return redirect('https://img.shields.io/badge/{}-{}-{}.svg'.format(
        'pipeline', status_text, status_color
    ))
