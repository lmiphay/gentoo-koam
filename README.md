#### gentoo-koam

gentoo-koam provides a UI to track merges on gentoo servers.

![gentoo-koam](screenshots/gentoo-koam.png?raw=true "gentoo-koam sample")

#### Installation

1. add the lmiphay overlay (available from layman: `layman -a lmiphay`)
2. keyword app-portage/gentoo-koam ( `echo '=app-portage/gentoo-koam-9999 ~amd64' >>/etc/portage/package.keywords` )
3. `emerge app-portage/gentoo-koam`

#### Dependencies

+ [gentoo-oam](https://github.com/lmiphay/gentoo-oam) installed, configured and running on each server
+ from where koam is run password-less ssh access to each monitored server 

#### Operation

The `koam` script takes a list of servers to monitor:

```
$ koam
usage: koam <server0>...<serverN>
$ koam kippure sorrel seefin &
$
```

#### Copyright

Copyright (c) 2013-2015 Paul Healy

Permission granted to redistribute it and/or modify it under the terms of the
GNU General Public License version 2.
