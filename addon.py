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

def format_menu_item(item):
	_item = {}
	_item['label'] = item['label']

	if item.get('is_playable'):
		_item['is_playable'] = item['is_playable']

	if item.get('path'):
		_item['path'] = item['path']

	if item.get('youtube_id'):
		_item['path'] = "plugin://plugin.video.youtube/?action=play_video&videoid=" + item['youtube_id']
		_item['is_playable'] = True

	if item.get('folder_id'):
		_item['path'] = plugin.url_for('show_folder_content', folderid=item['folder_id'])

	return _item



@plugin.route('/')
def main_menu():
	data = httpgetjson('http://localhost:3000/items.json')
	
	items = []
	for item in data['items']:
		items.append(format_menu_item(item))

	items.append ({
		"label": "Karaoke Search",
		"path": plugin.url_for('search')
	})

	return items



@plugin.route('/folders/<folderid>/')
def show_folder_content(folderid):
	data = httpgetjson('http://localhost:3000/'+folderid+'/folder.json')

	items = []
	for item in data['items']:
		items.append(format_menu_item(item))

	return items

@plugin.route('/karaoke/<karoke_number>/')
def show_karoke_number(karoke_number):
	response = httpgetjson('http://localhost:3000/api/v1/karaokes/' + karoke_number)
	if response.get('content'):
		item = format_menu_item(response['content'])
		return [item]

@plugin.route('/search/')
def search():
	search_string = plugin.keyboard(default=None, heading="Heading ...")
	if search_string:
		plugin.redirect(plugin.url_for('show_karoke_number', karoke_number=search_string))


if __name__ == '__main__':
	plugin.run()