zipname_db = []
stat_db = []
# whether to add a ps to disabled mod due to ver compact?


def process_vernum(vernum):
    if vernum[0] == 'V' or vernum[0] == 'v':
        return map(lambda x: int(x),vernum[1:].split('.'))
    else:
        return map(lambda x:int(x), vernum.split('.'))

def refreshmod():
    test_zips()
    for zipname in os.listdir(".\\mod\\"):
        base, ext = os.path.splitext(zipname)

        while ext and base.count('.') > 0:
            base, new_ext = os.path.splitext(base)
            ext = new_ext + ext
        # TODO:ver compact

        if ext == '.zip.disabled':
            zipname_db.append(base + '.zip')
            stat_db.append(False)
        elif ext == '.zip':
            zipname_db.append(zipname)
            stat_db.append(True)
        else:
            print("Invaid file in mod folder:%s" % zipname)


def refresh_plugin_folder():
    pass


def test_zips():
    name_tmp = []
    ver_tmp = []
    dependence_tmp = []
    activate_tmp = []
    zipname_tmp = []
    for zipname in os.listdir(".\\mod\\"):
        base, ext = os.path.splitext(zipname)
        if ext == '.disabled':continue
        with zipfile.ZipFile(zipname) as zipfile_obj:
            with zipfile_obj.open('meta-inf.json') as zip_f:
                content = zip_f.read()

                if isinstance(content, bytes):
                    content = content.decode('utf-8')

                data = json.loads(content)

                if 'ver' in data:
                    ver = process_vernum(data['ver'])
                else:
                    ver = process_vernum('1.0.0')
                if data['name'] in name_tmp:
                    # compete ver num
                    print("found dumplicate mods!")
                    dumplicate_index = name_tmp.index(data['name'])
                    ver_dum = ver_tmp[dumplicate_index]
                    # direct del?
                    if ver > ver_dum:
                        os.rename('.\\mod\\'+zipname_tmp[dumplicate_index],
                                  '.\\mod\\'+zipname_tmp[dumplicate_index]+'.disabled')
                        ver_tmp[dumplicate_index] = ver
                        dependence_tmp[dumplicate_index] = data['dependencies']
                        zipname_tmp[dumplicate_index] = zipname
                    elif ver <= ver_dum:
                        os.rename('.\\mod\\'+zipname,
                                  '.\\mod\\'+zipname+'.disabled')
                        continue
                else:
                    ver_tmp.append(ver)
                    zipname_tmp.append(zipname)
                    name_tmp.append(data['name'])
                    dependence_tmp.append(data['dependencies'])
                    activate_tmp.append(True)


    for dependence in dependence_tmp:
        not_included = []
        if dependence == 0:continue
        for data in dependence:
            if data['name'] in name_tmp:
                continue
            else:
                not_included.append(data['name'])
        if not_included:
            print("mod %s has dependence:%s that are not installed\n auto disable the mod"
                  %(name_tmp[dependence_tmp.index(dependence)],not_included))
            activate_tmp[dependence_tmp.index(dependence)] = False


    for index in range(len(activate_tmp)):
        if not activate_tmp[index]:
            os.rename('\\mods\\'+zipname_tmp[index],
                      '\\mods\\'+zipname_tmp[index]+'.disabled')


def mod_to_plugin():
    for zipname in os.listdir(".\\mod\\"):
        base, ext = os.path.splitext(zipname)

        while ext and base.count('.') > 0:
            base, new_ext = os.path.splitext(base)
            ext = new_ext + ext

        if ext == '.zip':
            with zipfile.ZipFile(fileroute, 'r') as zip_ref:
                with zipfile_obj.open('meta-inf.json') as zip_f:
                    # meta-inf.json
                    content = zip_f.read()
                    if isinstance(content, bytes):
                        content = content.decode('utf-8')
                    data = json.loads(content)

                    extracted = False
                    for file_info in zip_ref.infolist():
                        if file_info.filename == data['file_name']:
                            zip_ref.extract(file_info, r'.\BepInEx\plugins\\')
                            extracted = True
                    if not extracted:
                        print('did not find the mod file related to the meta-inf.json')
                        print('consider the zip/meta-inf.json is broken')

def enablemod_new():
    """
    1.test name
    if in:->test ver->disable/abort
    not in:pass

    2.test dependence
    if in:pass
    not in:show & abort
    """
    pass
