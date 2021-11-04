#!/usr/bin/python3
import argparse
import os
import time

from upstream_crawler import GerritCrawler
from upstream_crawler import GitCrawler
from upstream_crawler import GithubCrawler
from upstream_crawler import PatchworkCrawler

support_actions = ['gerrit', 'git', 'github', 'patchwork']

def find_report_directory(config_file):

	# remove the directory part
	_, tmp = os.path.split(config_file)

	# remove the ext part
	config_name, _ = os.path.splitext(tmp)

	while True:
		now = time.localtime()

		timestamp = time.strftime('%Y-%m%d-%H%M', now)

		report_name = '%s-%s' % (config_name, timestamp)
		report_directory = os.path.abspath('./' + report_name)

		if os.path.exists(report_directory) == False:
			break

		time.sleep(1)

	return report_directory

def validate_args(args):

	actions = []

	if args.action == '' or args.action == 'all':
		actions = support_actions
	else:
		actions = args.action.split(' ')

		for action in actions:
			if action not in support_actions:
				print('invalid action \'%s\'' % (action))
				return []

	if 'github' in actions:
		if args.user_name == None:
			print('missing github username')
			return []
		if args.token == None:
			print('missing github token')
			return []

	if args.config_file == None:
		print('missing config file')
		return []

	if os.path.isfile(args.config_file) == False:
		print('invalid config file')
		return []

	return actions

def main():

	# parse argument
	parser = argparse.ArgumentParser()

	parser.add_argument('action', nargs = '?', default = '', help = 'action to do')
	parser.add_argument('-c', '--config_file', help = 'config file')
	parser.add_argument('-u', '--user_name', help = 'github username')
	parser.add_argument('-t', '--token', help = 'github token')

	args = parser.parse_args()

	actions = validate_args(args)

	if len(actions) == 0:
		# no action to perform...
		return

	report_directory = find_report_directory(args.config_file)
	os.mkdir(report_directory)

	if 'gerrit' in actions:
		# gerrit
		crawler = GerritCrawler(args.config_file)

		changes = crawler.get_changes()

		if len(changes) != 0:
			crawler.export_csv_file(report_directory)
			crawler.export_excel_file(report_directory)
		else:
			print('fail to get changes from gerrit server')

	if 'git' in actions:
		# git
		crawler = GitCrawler(args.config_file)

		commits = crawler.get_commits()

		if len(commits) != 0:
			crawler.export_csv_file(report_directory)
			crawler.export_excel_file(report_directory)
		else:
			print('fail to get commits from git repo')

	if 'github' in actions:
		# github
		github_auth = (args.user_name, args.token)

		crawler = GithubCrawler(args.config_file, github_auth)

		pulls = crawler.get_pulls()

		if len(pulls) != 0:
			crawler.export_csv_file(report_directory)
			crawler.export_excel_file(report_directory)
		else:
			print('fail to get pulls from github repo')

	if 'patchwork' in actions:
		# patchwork
		crawler = PatchworkCrawler(args.config_file)

		patches = crawler.get_patches()

		if len(patches) != 0:
			crawler.export_csv_file(report_directory)
			crawler.export_excel_file(report_directory)
		else:
			print('fail to get changes from patchwork server')

	return

if __name__ == '__main__':
	main()
