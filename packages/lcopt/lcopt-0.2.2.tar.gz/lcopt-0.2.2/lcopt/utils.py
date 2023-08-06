try:
    import brightway2 as bw2
except:
    raise ImportError('Please install the brightway2 package first')

DEFAULT_DB_NAME = "LCOPT_Setup"

def lcopt_bw2_setup(ecospold_path, overwrite = False):
	if DEFAULT_DB_NAME in bw2.projects:
		if overwrite:
			bw2.projects.delete_project(name=DEFAULT_DB_NAME, delete_dir=True)
		else:
			print('Looks like bw2 is already set up - if you want to overwrite the existing version, use overwrite = True')
			return False

	bw2.projects.set_current(DEFAULT_DB_NAME)
	bw2.bw2setup()
	ei = bw2.SingleOutputEcospold2Importer(ecospold_path, "Ecoinvent3_3_cutoff")
	ei.apply_strategies()
	ei.statistics()
	ei.write_database()

	return True




