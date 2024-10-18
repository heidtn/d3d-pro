### Setup

#### Setup AP

The first step is to enable the SoftAP that comes with the beaglebone. It can run simultanously in client and hotspot mode.

`sudo cp hostapd.conf /etc/hostapd/hostapd.conf`

#### Enable permissions for WiFi control

Second step is to create a polkit rule for netdev so we don't have to run as root.  Create a file called `10-networkmanager.riles` to `/etc/polkit-1/rules.d` and add the following:

```
polkit.addRule(function(action, subject) {
	if (subject.isInGroup("netdev")) {
    	if (action.id == "org.freedesktop.NetworkManager.settings.modify.own" ||
        	action.id == "org.freedesktop.NetworkManager.settings.modify.system" ||
        	action.id == "org.freedesktop.NetworkManager.network-control" ||
        	action.id == "org.freedesktop.NetworkManager.enable-disable-wifi") {
        	return polkit.Result.YES;
    	}
	}
});
```

Finally add the user to the netdev group: `usermod -a -G netdev YOUR_USERNAME` where YOUR_USERNAME is whatever you have setup to be the main user on the beaglebone.

#### Set the Hostname

If you want to set a custom mdns hostname, simple change the name in `/etc/hostname` which is typically beagle by default.

### Configure nginx to allow octoprint and our server to run side by side
