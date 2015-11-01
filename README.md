#### gentoo-koam

gentoo-koam provides a UI to track merges on gentoo servers.

It provides a summary for each server running updates:

![gentoo-koam](screenshots/gentoo-koam-2.png?raw=true "gentoo-koam sample")

And it provides an at-a-glance set of progress bars for all the servers being monitored:

![gentoo-koam](screenshots/gentoo-koam-3.png?raw=true "gentoo-koam sample")

#### Installation

1. add the lmiphay overlay (available from layman: `layman -a lmiphay`)
2. keyword app-portage/gentoo-koam ( `echo '=app-portage/gentoo-koam-9999 ~amd64' >>/etc/portage/package.keywords` )
3. `emerge app-portage/gentoo-koam`

#### Dependencies

+ [gentoo-oam](https://github.com/lmiphay/gentoo-oam) installed, configured and running on each server
+ from where koam is run password-less ssh access to each monitored server 

#### Operation

`koam` optionally takes a list of servers to monitor:

```
$ koam -h
usage: koam [-h] [-d] [<server0>...<serverN>]
$ koam kippure sorrel seefin &
$
```

Passing the `-d` option will add DEBUG level logging to the console (in addition to the default INFO
level messages).

The list of servers being monitored can be saved and reloaded at a later time (the save is made to
`~/.koam/koam.servers` in yaml format).

#### Copyright

Copyright (c) 2013-2015 Paul Healy

Permission granted to redistribute it and/or modify it under the terms of the
GNU General Public License version 2.
