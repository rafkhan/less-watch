import sys, os
from pyinotify import *

class INEventHandler(ProcessEvent):

	def __init__(self, outdir, ignore):
		self.indir = indir
		self.outdir = outdir
		self.ignore_list = ignore

	def process_IN_MODIFY(self, event):
		self.less_command(event)

	def process_IN_CREATE(self, event):
		self.less_command(event)

	def less_command(self, event):
		if not event.path in self.ignore_list:

			call = 'lessc ' + event.path + '/' + event.name + ' > '
			call += self.outdir + '/' + event.name[:len(event.name) - 4] + 'css'
			print call
			os.system(call)


if __name__ == '__main__':

	if len(sys.argv) > 2:
		indir = sys.argv[1]
		outdir = sys.argv[2]

		if os.path.isdir(indir):
			wm = WatchManager()
			ignore = set(sys.argv[2:]) if len(sys.argv) > 3 else set()
			notifier = Notifier(wm, INEventHandler(outdir, ignore))
			wdd = wm.add_watch(indir, IN_MODIFY, rec=False)

			while True:
				try:
					notifier.process_events()
					if notifier.check_events():
						notifier.read_events()
				except KeyboardInterrupt:
					notifier.stop()
					break

		else:
			print "not a directory"

	else:
		#naw nuff arguments
		print "naw nuff"
