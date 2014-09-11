import urllib2 
from xbmcswift2 import Plugin
from resources.lib.academicearth.api import AcademicEarth
from StringIO import StringIO

try:
	import json
except:
	import simplejson as json

plugin = Plugin()

def httpgetjson(url):
	response = urllib2.urlopen(url)
	return json.load(response)

@plugin.route('/')
def main_menu():
	
	data = httpgetjson('http://localhost:3000/items.json')

	items = []
	for item in data['items']:
		_item = {}
		_item['label'] = item['label']

		if item.get('is_playable'):
			_item['is_playable'] = item['is_playable']

		if item.get('path'):
			_item['path'] = item['path']

		if item.get('youtube_id'):
			_item['path'] = "plugin://plugin.video.youtube/?action=play_video&videoid=" + item['youtube_id']
			_item['is_playable'] = True

		items.append(_item)

	return items

@plugin.route('/subjects/')
def show_subjects():
	api = AcademicEarth()
	subjects = api.get_subjects()
	items = [
		{
		'label': subject.name,
		'path': plugin.url_for('show_subject_info', url=subject.url),
		} for subject in subjects
	]
	sorted_items = sorted(items, key=lambda item: item['label'])
	return sorted_items

@plugin.route('/subjects/<url>/')
def show_subject_info(url):
	pass

if __name__ == '__main__':
	plugin.run()