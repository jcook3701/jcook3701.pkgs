# Handbrake

[Handbrake](https://handbrake.fr/) HandBrake is a open-source tool, built by volunteers, for converting video from nearly any format to a selection of modern, widely supported codecs.

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--

# Authors Notes:

 Rip the Raw DVD Contents
``` shell
$ dvdbackup -i /dev/dvd -o ~ -M
```

Transcode to a Single Video File (MP4 or MKV)
``` shell
$ HandBrakeCLI -i ~/[movie_name]/VIDEO_TS -o ~/movie.mp4 --preset="Fast 1080p30"
```

Alternative: Convert Directly to ISO
``` shell
$ genisoimage -dvd-video -udf -o ~/movie.iso ~/[movie_name]
```

# TODO:
>
