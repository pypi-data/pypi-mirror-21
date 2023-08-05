.PHONY: all import export clean

bguo = ./bguo

all: import export
import: import.mh import.mutt import.voipms import.seltzer import.merge
export: export.konftel export.mh export.mutt export.newsbeuter \
	export.email export.feed export.name export.name-latin export.phone export.post \
	export.phone-numeric export.post-formatted
clean:
	rm -Rf export.* import.*

# Custom imports
import.merge: orig.voipms orig.mh
	./merge.py orig.voipms orig.mh import.merge

# Integrations
import.mh: orig.mh
	$(bguo) import mh orig.mh import.mh

import.mutt: orig.mutt
	$(bguo) import mutt orig.mutt import.mutt

import.voipms: orig.voipms
	$(bguo) import voipms orig.voipms import.voipms

import.seltzer: orig.seltzer
	$(bguo) import seltzer orig.seltzer import.seltzer

export.konftel: orig.bguo
	$(bguo) export orig.bguo konftel > export.konftel

export.mh: orig.bguo
	$(bguo) export orig.bguo mh > export.mh

export.mutt: orig.bguo
	$(bguo) export orig.bguo mutt > export.mutt

export.newsbeuter: orig.bguo
	$(bguo) export orig.bguo newsbeuter > export.newsbeuter

# Single-field exports
export.email: orig.bguo
	$(bguo) export orig.bguo custom '{identifier}: {email}' > export.email

export.feed: orig.bguo
	$(bguo) export orig.bguo custom '{identifier}: {feed}' > export.feed

export.name: orig.bguo
	$(bguo) export orig.bguo custom '{identifier}: {name}' > export.name

export.name-latin: orig.bguo
	$(bguo) export orig.bguo custom '{identifier}: {name-latin}' > export.name-latin

export.phone: orig.bguo
	$(bguo) export orig.bguo custom '{identifier}: {phone}' > export.phone

export.phone-numeric: orig.bguo
	$(bguo) export orig.bguo custom '{identifier}: {phone-numeric}' > export.phone-numeric

export.post: orig.bguo
	$(bguo) export orig.bguo custom '{identifier}: {post}' > export.post

export.post-formatted: orig.bguo
	$(bguo) export orig.bguo custom '{post-formatted}' -sep '***' > export.post-formatted
