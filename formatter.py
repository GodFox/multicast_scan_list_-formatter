import os
from ipytv import playlist

def parse_ref(ref_file) -> dict:
    ref_channels = {}
    pl = playlist.loadf(ref_file)
    channels = pl.get_channels()
    for channel in channels:
        ip = channel.url.split('/')[-1].split(':')[0]
        ref_channels[ip] = channel
    return ref_channels


def match_channel(channels_url, ref_channels: dict):
    for url, detail in channels_url.items():
        if detail != {}:
            continue
        ip = url.split(':')[0]
        if ip in ref_channels.keys():
            channels_url[url] = ref_channels[ip]

    return channels_url


def main():
    input_file = f"scan_list/scan_list.txt"
    channels_url = {}
    with open(input_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == '':
                continue
            channels_url[line] = {}

    ref_files = [
        f"ref/bj-unicom-iptv/bj-unicom-iptv.m3u",
        f"ref/Beijing-IPTV/IPTV-Unicom-Multicast.m3u",
        f"ref/BeiJing-Unicom-IPTV-List/iptv.m3u"
    ]

    for ref_file in ref_files:
        ref_channels = parse_ref(ref_file)
        channels_url = match_channel(channels_url, ref_channels)

    udproxy_prefix = f"http://192.168.10.1:1024/rtp/"
    path, input_file_name = os.path.split(input_file)
    output_file_name = os.path.splitext(input_file_name)[0]
    output_file = os.path.join(path, output_file_name + '.m3u')
    with open(output_file, 'w') as f:
        f.write('#EXTM3U name="IPTV_bj_unicom"\n')
        for url, detail in channels_url.items():
            detail.url = udproxy_prefix + url.replace('://', '/')
            print(f"{url}: {detail.to_m3u_plus_playlist_entry()}")
            f.write(detail.to_m3u_plus_playlist_entry())


if __name__ == "__main__":
    main()