import sys


if len(sys.argv) <3:
    print('more than 3')
    sys.exit()
word=sys.argv[1]
    for filename in sys.argv[2:]
        for lino,line in enumerate(open(filename),start=1)
            if word in line:
                print('{0}:{1}:{2:.40}'.format(filename,lino,line.rstrip()))