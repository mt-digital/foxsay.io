import glob
import os

from collections import OrderedDict
from datetime import datetime, timedelta

from flask import render_template, Flask, request, redirect

app = Flask(__name__)


@app.route('/')
def display_summaries():

    has_next = True

    date = request.args.get('date')
    if date is None:
        date = datetime.now()
        solr_date = _fmt_solr(date - timedelta(days=1))

        has_next = False

        return redirect('/?date=' + solr_date)
        # date = datetime(2016, 1, 1)
    else:
        y = int(date[:4])
        m = int(date[4:6])
        d = int(date[6:])

        try:
            date = datetime(y, m, d)
        except ValueError:
            if m in [9, 4, 5, 11]:
                d = 30
            else:
                if y % 4 == 0:
                    d = 29
                else:
                    d = 28

            try:
                date = datetime(y, m, d)
            except:
                date = datetime(2016, 1, 1)

    solr_date = _fmt_solr(date)
    yesterday_solr_date = _fmt_solr(datetime.now() - timedelta(days=1))

    next_solr_date = None
    prev_solr_date = None

    has_next = has_next and solr_date != yesterday_solr_date
    if has_next:
        next_solr_date = _fmt_solr(date + timedelta(days=1))

    # only have data for 2016 for now
    has_prev = solr_date[:4] != '20160101'
    if has_prev:
        prev_solr_date = _fmt_solr(date - timedelta(days=1))

    # summaries = _read_day_summaries(day=solr_date)
    summaries = _read_day_summaries(data_dir='data/2016', day=solr_date)

    return render_template('index.html', date=date,
                           prev_solr_date=prev_solr_date,
                           next_solr_date=next_solr_date,
                           summaries=summaries)


def _fmt_solr(d):
    return d.strftime('%Y%m%d')


# the latest available summaries are from yesterday, not today
YESTERDAY_SOLR = _fmt_solr(datetime.now() - timedelta(1))


# XXX robust? Don't actually care, would be simplified in Mongo version
def _extract_show_name(_dir):
    return '\n'.join(_dir.split('_')[3:])


def _read_show_summary(d):

    ret = ''

    try:
        ret = open(
            os.path.join(d, 'summary.txt')
        ).read()
    except:
        pass

    return ret


def _read_day_summaries(data_dir='data/shows/FOXNEWSW', day=YESTERDAY_SOLR):

    yr_month = day[:6]
    # glb = glob.glob(os.path.join(data_dir, yr_month, '*' + day + '*'))
    glb = glob.glob(os.path.join(data_dir, '*' + day + '*'))

    summaries = OrderedDict([

        (
            _extract_show_name(d),
            _read_show_summary(d)
        )

        for d in glb
    ])

    return summaries
