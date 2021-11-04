#!/usr/bin/python3
import csv
import git
import matplotlib.pyplot as plt
import numpy as np
import os
import time

from upstream_crawler import GitCrawler

FUNC_AUDIO = 'audio'
FUNC_DISPLAY_GRAPHIC = 'display/graphic'
FUNC_OTHER = 'other'

def output_jpg_file(commits):
	x = []
	y_audio = []
	y_display = []
	y_other = []
	y_total = []

	while True:
		now = time.localtime()

		timestamp = time.strftime('%Y-%m%d-%H%M', now)

		jpg_name = 'chrome-mm-linux-upstream-%s.jpg' % (timestamp)
		jpg_path = os.path.abspath(jpg_name)

		if os.path.exists(jpg_path) == False:
			break

		time.sleep(3)

	print('save plot to %s' % (jpg_path))

	for commit in commits:
		year = int(commit['date'].split('-')[0])

		if year not in x:
			x.append(year)
			y_audio.append(0)
			y_display.append(0)
			y_other.append(0)
			y_total.append(0)

		idx = x.index(year)

		y_total[idx] += 1

		function = commit['function']
		if function == FUNC_AUDIO:
			y_audio[idx] += 1
		elif function == FUNC_DISPLAY_GRAPHIC:
			y_display[idx] += 1
		else:
			y_other[idx] += 1 # should not happen

	plt.plot(x, y_audio, label = FUNC_AUDIO)
	plt.plot(x, y_display, label = FUNC_DISPLAY_GRAPHIC)
	plt.plot(x, y_other, label = FUNC_OTHER)
	plt.plot(x, y_total, label = 'total')

	plt.title('Upstream to Linux Repo')
	plt.xlabel('Year')
	plt.ylabel('Commit')

	plt.legend()

	plt.savefig(jpg_path)
	plt.show()

	return

def main():

	crawler = GitCrawler()

	commits = crawler.get_commits()

	if len(commits) != 0:
		crawler.export_csv_file()

	# draw a plot and save to jpg file
	#output_jpg_file(commits)

	return

if __name__ == '__main__':
	main()
