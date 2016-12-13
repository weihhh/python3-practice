import sys,os,glob

if sys.platform.startswith('win'):
    def get_files(names):
        for name in names:
            if os.path.isfile(name):
                yield name 
            else:
                for file in glob.iglob(name):
                    if not os.path.isfile(file):
                        continue
                    yield file
else :
    def get_files(names):
        return (file for file in names if os.path.isfile(file))

files=get_files(sys.argv[1:])
for file in files:
    print(file)