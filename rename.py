import storage, sys
storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = "PYGAMER0"
storage.remount("/", readonly=True)
sys.exit()