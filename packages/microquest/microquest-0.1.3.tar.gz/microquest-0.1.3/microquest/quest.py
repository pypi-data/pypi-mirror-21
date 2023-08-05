import microquest
import sys
import configparser
class Quest(object):
	def __init__(self, key, description=None, value=50, savefp=None):
		self.key = key
		if description == None:
			description = key
		self.description = description
		self.value = value
		self.savefp = savefp

	# save the quest
	def save(self):
		try:
			cfg = configparser.ConfigParser()
			cfg.read(self.savefp)
			cfg[self.key] = {
				'description': self.description,
				'value': str(self.value)
			}
			with open(self.savefp, 'w') as cfgfile:
				cfg.write(cfgfile)
		except Exception as e:
			print(e)
			sys.stderr.write("couldn't save quest {self.key}\n")
			sys.exit(1)

		return True

	# load conf file and remove itself from it
	def delete(self, verbose=True):
		cfg = configparser.ConfigParser()
		cfg.read(self.savefp)
		cfg.remove_section(self.key)
		with open(self.savefp, 'w') as cfgfile:
			cfg.write(cfgfile)
		if verbose:
			print(f'{self.description} removed')

		

