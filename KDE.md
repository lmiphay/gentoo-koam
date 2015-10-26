#### Dependencies

dev-util/plasmate
kde-base/plasma-workspace

#### Hints

##### Applet Fails to Start

If it fails to start with: 'Could not create a python ScriptEngine for the koam widget.'

Check that:
1. kde-base/plasma-workspace has been built with python use flag (i.e. kde-base/plasma-workspace[python])
2. and has been restarted

##### Restart plasma-desktop

You might be able to restart plasma-desktop by:
```
kbuildsycoca4
kquitapp plasma-desktop
sleep 5
kstart plasma-desktop
```

##### Last Resort

Try rebuilding these packages:
```
dev-python/PyQt4
kde-base/pykde4
```

Turn on plasma related debug information in: `kdebugdialog --fullmode`
