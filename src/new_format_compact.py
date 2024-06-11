zipname_db = []
stat_db = []


def refreshmod():
    for zipname in os.listdir(".\\mod\\"):
        base, ext = os.path.splitext(zipname)

        while ext and base.count('.') > 0:
            base, new_ext = os.path.splitext(base)
            ext = new_ext + ext

        if ext == '.zip.disabled':
            zipname_db.append(base + '.zip')
            stat_db.append(False)
        elif ext == '.zip':
            zipname_db.append(zipname)
            stat_db.append(True)
        else:
            print("Invaid file in mod folder:%s" % zipname)
