from mpegdash.parser import MPEGDASHParser

mpd_path = './a.mpd'

mpd = MPEGDASHParser.parse(mpd_path)

representations = mpd.periods[0].adaptation_sets[0].representations

metadata = [
    
]

for i in range(len(representations)):
    metadata.append({
        "id": representations[i].id,
        "width": representations[i].width,
        "height": representations[i].bandwidth,
        "codecs": representations[i].codecs,
        "scanType": representations[i].scan_type,
        "baseURL": representations[i].base_urls[0].base_url_value
    })
    
print(metadata)    