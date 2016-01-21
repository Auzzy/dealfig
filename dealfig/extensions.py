import boto

from dealfig import app

_ASSET_DIR = "assets"
_THUMBNAIL_DIR = "thumbnails"

_S3CONN = boto.connect_s3()
_BUCKET = _S3CONN.get_bucket(app.config["S3_BUCKET"])


def _s3key(designer, folder, filename):
    key = "{designer}/{folder}/{filename}".format(designer=designer, folder=folder, filename=filename)
    return boto.s3.key.Key(_BUCKET, key)

def _asset_url(asset, thumbnail=False):
    folder = _THUMBNAIL_DIR if thumbnail else _ASSET_DIR
    return _s3key(asset.exhibitor.designer.name, folder, asset.filename).generate_url(expires_in=0, query_auth=False)


@app.context_processor
def processors():
    def get_asset_url(asset):
        return _asset_url(asset)
    
    def get_thumb_url(asset):
        return _asset_url(asset, True)
    
    def media_types_to_string(media_types):
        return ', '.join([media_type.display_name for media_type in media_types])
    
    def file_formats_to_string(file_formats):
        print(file_formats)
        return ', '.join(set(fmt.name for fmt in file_formats))
    
    return {
        "get_asset_url": get_asset_url,
        "get_thumb_url": get_thumb_url,
        "media_types_to_string": media_types_to_string,
        "file_formats_to_string": file_formats_to_string
    }