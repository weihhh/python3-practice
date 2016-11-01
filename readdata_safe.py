def read_data(filename):
    lines=[]
    fh=None
    try:
        fh=open[filename,encoding='utf-8']
        for line in    fh:
            if line.strip():
                lines.append(line)
    except(IOError,OSError)as err:
        print(err)
        return []
    finally:
        if fh is not None:
            fh.close()
    return lines