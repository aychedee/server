from PIL import Image
from cStringIO import StringIO
from datetime import datetime
from dropbox import Dropbox, files, exceptions
from hashlib import sha1
from pprint import pformat
import boto3
import io
import json
import os
import requests


WIDTHS = [
    2560,
    1920,
    1280,
    720
]
REVERSE_GEOCODE_URL = (
    'http://maps.googleapis.com'
    '/maps/api/geocode/json?latlng={lat},{lon}'
)



def save_image(img):
    container = io.BytesIO()
    img.save(
        container,
        format='JPEG',
        optimize=True,
        quality=90,
        progressive=True,
        icc_profile=img.info.get('icc_profile')
    )
    container.seek(0)
    img_name = '{}.jpg'.format(sha1(container.read()).hexdigest())

    save_to_s3(container, img_name)

    return img_name


class Photo(object):

    def __init__(self, location, taken, assets):
        self.location = location
        if isinstance(taken, datetime):
            self.taken = taken
        else:
            self.taken = datetime.strptime(taken, '%Y-%m-%d %H:%M:%S')
        self.assets = assets

    def __lt__(self, other):
        return other.taken < self.taken

    def __str__(self):
        return '{} @ {} : {}'.format(self.location, self.taken, self.assets)

    def __hash__(self):
        return int(sha1('{}{}'.format(
            self.location,
            self.taken,
        )).hexdigest(), 16)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def as_dict(self):
        return {
            'taken': str(self.taken),
            'location': self.location,
            'assets': self.assets,
        }


def get_best_address(lat, lon):
    for address in requests.get(REVERSE_GEOCODE_URL.format(lat=lat, lon=lon)).json()['results']:
        if 'postal_code' in address['types']:
            return address['formatted_address']


def get_feed(dbx):
    try:
        return [
            Photo(p['location'], p['taken'], p['assets']) for p
            in json.loads(dbx.files_download('/feed.json')[1].content)
        ]
    except exceptions.ApiError:
        return []


def asset_dict(img, path):
    return {
        'path': path,
        'width': img.size[0],
        'height': img.size[1]
    }


def save_to_s3(file_obj, name, content_type='image/jpeg'):
    s3 = boto3.client('s3')
    file_obj.seek(0)
    s3.upload_fileobj(
        file_obj,
        'photos.interpretthis.org',
        name,
        ExtraArgs={
            'ACL': 'public-read',
            'ContentType': content_type
        }
    )


def run():
    dbx = Dropbox(os.environ['DROPBOX_TOKEN'])
    feed = get_feed(dbx)
    delete_on_success = []

    for entry in dbx.files_list_folder('').entries:
        print(entry.name)

        metadata, response = dbx.files_download('/{}'.format(entry.name))

        if not metadata.media_info:
            continue

        pmd = metadata.media_info.get_metadata()

        if not type(pmd) is files.PhotoMetadata:
            continue

        address = get_best_address(
            pmd.location.latitude,
            pmd.location.longitude
        )
        taken = pmd.time_taken
        assets = {}

        for width in WIDTHS:
            # Save each different width
            img = Image.open(io.BytesIO(response.content))
            img.thumbnail((width, width*2), Image.ANTIALIAS)
            image_name = save_image(img)
            assets[width] = asset_dict(img, image_name)

        # Save original sized image
        img = Image.open(io.BytesIO(response.content))
        image_name = save_image(img)
        assets[pmd.dimensions.width] = asset_dict(img, image_name)
        feed.append(Photo(address, taken, assets))

        delete_on_success.append(entry.name)
        # dbx.files_delete('/{}'.format(entry.name))

    save_to_s3(
        io.BytesIO(json.dumps(
            [p.as_dict() for p in sorted(set(feed))],
            indent=4, separators=(',', ': ')
        )),
        'feed.json',
        content_type='application/json'
    )

    for name in delete_on_success:
        dbx.files_delete('/{}'.format(name))


if __name__ == '__main__':
    run()
