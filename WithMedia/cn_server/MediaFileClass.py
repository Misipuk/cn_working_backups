from typing import Dict, List, Optional
import os
import base64

PHOTO = "photo"
VIDEO = "video"


class MediaFile:
    id: int
    cafeid: int
    type: str

    def __init__(self, cafeid: int, type: str):
        self.id = None
        self.cafeid = cafeid
        self.type = type
        self.bcd = None
        pass

    def generate_path(self):
        if self.type == PHOTO:
             if os.path.isdir("./photos/" + str(self.cafeid)):
                return "./photos/" + str(self.cafeid) + "/" + str(self.id) + ".jpg"
             else:
                 os.mkdir("./photos/" + str(self.cafeid))
                 return "./photos/" + str(self.cafeid) + "/" + str(self.id) + ".jpg"

        elif self.type == VIDEO:
            if os.path.isdir("./videos/" + str(self.cafeid)):
                return "./videos/" + str(self.cafeid) + "/" + str(self.id) + ".mov"
            else:
                os.mkdir("./videos/" + str(self.cafeid))
                return "./videos/" + str(self.cafeid) + "/" + str(self.id) + ".mov"

        else:
            raise Exception("unknown type")

    def copy(self):
        mf = MediaFile(self.cafeid, self.type)
        mf.id = self.id
        mf.bcd = self.bcd
        return mf

def b64_encode(b: bytes) -> bytes:
    return base64.urlsafe_b64encode(b)

class MediaFiles:
    # cafe_id -> list of MediaFiles
    _cafe_files: Dict[int, List[MediaFile]]
    _all_files: List[MediaFile]

    def __init__(self):
        self._cafe_files = {}
        self._all_files = []

    def get(self, cid: int) -> Optional[List[MediaFile]]:
        mfl = self._cafe_files.get(cid)
        if mfl is None:
            return None
        for fl in mfl:
            path = fl.generate_path()
            with open(path, mode='rb') as f:
                fl.bcd = b64_encode(f.read()).decode()
        return MediaFiles._copy_if_none(mfl)

    def put(self, mf: MediaFile, body) -> MediaFile:
        if mf.id is None:
            if len(self._all_files) != 0:
                mf.id = len(self._all_files) + 1
            else:
                mf.id = 1

        # image_data = open('photos/'+mf.id, 'rb')
        # bytes = image_data.write() ?
        # To list
        if len(self._all_files)!=0:
            self._all_files.append(mf)
        else:
            self._all_files = [mf]

        #store_image
        self._store_image(mf, body)

        # To dict
        if self._cafe_files.get(mf.cafeid) is not None:
            self._cafe_files[mf.cafeid] = self._cafe_files[mf.cafeid] + [mf]
        else:
            self._cafe_files[mf.cafeid] = [mf]
        return mf

    def put_init(self, mf: MediaFile) -> MediaFile:
        if mf.id is None:
            if len(self._all_files) != 0:
                mf.id = len(self._all_files) + 1
            else:
                mf.id = 1

        # image_data = open('photos/'+mf.id, 'rb')
        # bytes = image_data.write() ?
        # To list
        if self._all_files is not None:
            self._all_files.append(mf)
        else:
            self._all_files = [mf]

        # To dict
        if self._cafe_files.get(mf.cafeid) is not None:
            self._cafe_files[mf.cafeid] = self._cafe_files[mf.cafeid] + [mf]
        else:
            self._cafe_files[mf.cafeid] = [mf]
        return mf

    def _store_image(self, mf: MediaFile, body):
        path = mf.generate_path()
        with open(path, mode='wb') as f:
            f.write(body)

    def delete_by_cafeid(self, cafeid: int, fileid: int):
        for mf in self._all_files:
            if mf.id == fileid and mf.cafeid == cafeid:
                self._all_files.remove(mf)
                os.remove(mf.generate_path())

        lst = self._cafe_files.get(mf.cafeid)
        for mf in lst:
            if mf.id == fileid and mf.cafeid == cafeid:
                lst.remove(mf)
                return 1
        return -1

    @staticmethod
    def _copy_if_none(mf: List[MediaFile]):
        if mf is not None:
            mf1 = []
            for f in mf:
                mf1.append(f.copy())
            return mf1
        else:
            return None
