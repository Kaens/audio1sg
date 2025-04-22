# audio1sg
 The comprehensive tracker/retro/exotic music format detection script for Detect-it-Easy (https://github.com/horsicq/Detect-It-Easy)

I've been working over the entirety of http://modland.com/pub/modules/ and some more rarities. This currently supports 380 distinct formats, and 17 more of them less reliably for various reasons. 207 of them are parsed for the expected filesize, allowing for basic integrity checks, or ripping. (I count them by counting occurrences of `bDetected =`, `"~audio"`, and `outSz`, correspondingly.)

I've made this separate from DiE for the sake of flexibility, as DiE releases are rather slow per se, and keeping its sources cloned is very storage-heavy. That said, please use [the latest build](https://github.com/horsicq/DIE-engine/actions/) of DiE! (Click the latest workflow run, scroll down to the artifacts and choose yours.)\
In case of issues, also ensure the `read` and `chunkparsers` scripts from [the master github repo](https://github.com/horsicq/Detect-It-Easy/tree/master/db) are current!

Changes are quite welcome; if you know more about a format, please add used software to sVersion, and add the sOptions (which are basically extra info fields) regarding orderlist lengths, pattern/instrument/sample counts, check for basic file integrity like pointers leading outside the file or impossible pattern counts or volumes (for example, to add credibility to some overly generic-looking signature scans) — and of course, make it more fun in general for the user who chose "Verbose"! Read more in detail at [TODO.md](TODO.md) (which also includes contribution guidelines).

Don't fear the algo-heavier scans: at its first release, the entire script's checking routine takes within 0.1 sec even with the sanity check-based detection.
 
----

Supporting my efforts via crypto is also an option, not just the common way!
 
<img src="https://cryptologos.cc/logos/bitcoin-btc-logo.svg?v=040" height=32dp alt="BTC" /> `1LwFDfgzVvi5ghDNhiC7D61wzf1wRrnDTY`

<img src="https://cryptologos.cc/logos/versions/ethereum-eth-logo-colored.svg?v=040" height=32dp alt="ETH" /> `0x431abcbeef27330630776b69d846ea57d3b6d3ab`