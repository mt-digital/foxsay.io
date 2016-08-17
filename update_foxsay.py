from datetime import datetime, timedelta

from iatv import download_all_transcripts, search_items, summarize_standard_dir

yesterday = datetime.now() - timedelta(days=1)

dstr = yesterday.strftime('%Y%m%d')

items = search_items('I', channel='FOXNEWSW', time=dstr, rows=100000)

shows = [item for item in items if 'commercial' not in items]

download_all_transcripts(shows, base_directory='/home/mt/foxsay.io/data/2016')

summarize_standard_dir('/home/mt/foxsay.io/data/2016/', 10)
