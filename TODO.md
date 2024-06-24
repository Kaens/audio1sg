# How to contribute

This file covers the grand TODO of things, the conventions of informing, and the scan flags.

## TODO

The following formats are to be reversed (or otherwise understood) and most likely sanity check-tested. Or given up on (like if it's a headless OPL or AdLib command dump where you can't sanity-check anything).

This is where you can contribute the most! (sorted by extension)

 - Herad Music System `.AGD`/`.SDB`/`.SQX`
 - Compoz `.CPZ`
 - Megadrive `.CYM`
 - Edlib .`EDL`
 - Twin TrackPlayer `.DMO` (decrypt, unpack...)
 - Digital Studio `.DST` (Spectrum)
 - Pixel Painters `.FMF`, `.FTF`
 - Flash Tracker `.FTS`
 - Jason Brooke's `.JB`
 - Jesper Olsen's `.JO`
 - Kris Hatlelid's `.KH`
 - Loudness Sound System `.LDS`
 - Ultima 6 `.M`
 - Sidplayer `.MUS`
 - Startrekker AM's `.NT` info files
 - Westwood `.SND`
 - SAM Coupe `.SNG`
 - Paul Summers's `.SNK`
 - Beni Tracker `.PIS`
 - Paul Shields's `.PS`
 - Powertracker `.PT`
 - Peter Verswyvelen's `.PVP`
 - Quartet ST `QTS.`
 - Speedy A1 System `.SAS`
 - SoundControl `.SC`
 - SCUMMVM `.SCUMM`
 - Synth Dream `SDR.`
 - Tomy Tracker `.SG`
 - Scott Johnston's SoundPlayer `SJS.`
 - Sound Master `.SM`
 - Pierre Adane Packer `.PAP`
 - Stereo Sidplayer `.STR`
 - .DMM, `.SQD` - test patterns!
 - TFM Music Maker `.TFE`
 - Thomas Hermann's `THM.`
 - Sound Images `.TW`
 - Vibrants `.VIB` (I just have 1 file of this)
 - Optionally (desirably), various sample formats

There are also lots of TODO marking their way through the entire `audio.1.sg`, and they want attention as well. Many things that don't have the mark still can be improved by adding and outputting some analysis towards orders/patterns/samples/instruments/tempo/speed or whatever else the format has to offer.

The test files may be found in this gigantic collection, I presume: https://archive.org/download/amiga-back-2-roots-ftp . And in this one http://oakvalley.textfiles.com/oakvalley/


## A word on how sanity checks work

As you can see by scrolling through the latter part of `audio.1.sg`, there are quite a few sanity check-based detectors, which work by assuming the file has this or that format and proceeding to parse the file as such and validate its every byte as pertains:

 - for example, the tempo may be within the range of 3 through 15, so 0..2 and 16+ are invalid and should count as a failed detection;
 - for another example, if a format only has OPL2 commands in a known block, any bits that can only be set for OPL3 are a no;
 - or you can require that the pattern block doesn't overlap with the other blocks of data (unless you know of some files that deliberately exploit that by putting pattern data into, say, the song title block to achieve various ends), that no blocks are outside of the file size, etc.

The more tests there are that can easily fail, the "tighter" the detection will be, and the more desirable.

I was principally copying the other people's sanity checks (hello Bul'ba, asle, Vitamin, Neumann & more!) so I wasn't commenting that code; if you want to grasp some principles, please read the referenced sources. The OpenMPT and ProWizard ones normally have the most comments so those are recommended.

## On sVersion, isVerbose, isDeepScan, isHeuristicScan and conventions

As long as we just want to show what kind of file it is and what version it is, the information should appear either way.

Sometimes the version includes mentioning which chip a chiptune uses, sometimes a word when we want to complain that the tune is malformed. The version always starts with a `v` followed by either a floating-point info like `1.0xx` or, usually for internal format versions, a single number either in decimal or in hexadecimal (in the latter case, output it like `0Eh`: the module `read` has the function `Hex` for that, for simplicity.)

However, if we want to show the user the track title, or the author's rant, or how many different instruments the track has, or whatever else that goes into sOptions, then only add those if `Binary.isVerbose()` is `true`. Very simple.

The common tags and other things have a small convention for themselves (add in this order):

| content | output like this |
|-|:-:|
| track name | `Pyllamarama Theme` |
| tracks in multitrack | `×15` (note the non-ASCII "×") |
| author | `by: P.J.Summerbottom` |
| game | `for: Pyllamarama` |
| system | `on: Seagull Minidrive` |
| comment | `Hi everyone, just FYI script kiddos suk` |

If there are several tags that say the same in different languages (EN/JP being the most common), output them like this: `title/タイトル` etc. There's a function called `slashtag` that you can use for this.

If you want to output a lot of quick ubiquitous parameters (tempo, initial speed, orders, patterns, instruments, samples, notes), do write them out in a single sOptions addition that goes *after* any customisable tags you want to show and looks like `tempo:AA spd0:BB ord:CC ptn:DD ins:EE smp:FF notes:GGGGG`, you can probably find the other ones you want for reference somewhere in the file. If it's too hard to output that as a single string in one go, give up and output them like `tempo: BB`, `init.speed: BB`, `orders: CC` etc. one at a time.

I additionally follow the rule "don't overload it", like I don't show all sample names of a .MOD just because it's oft-used for info, but just the first couple, enough in case the author's name is in there.

`Binary.isDeepScan()` should mean that a detection that you know takes a lot of time should not run if this flag is off; most sanity checks feature cycles of uncertain iterations, so they only happen with Deep scan flag on.

`Binary.isHeuristicScan()` is meaningful in two cases for this file:
 - either you just relied on the file extension (and optionally some super generic signature like "PK" at 0 bytes. It's VERY ~~lazy~~ heuristic, doing something like that, but very rarely it's the best you can do),
 - or you saw just one or two files that are hella broken and you have a player that still manages to play them, but it really breaks the rules of some stuff that can make a detection of the overall format much tighter (for example, just the sample loops are out of bounds and the player simply doesn't loop that sample). So at this point you want to check for that stuff you first look at this flag, and if it is set, you just append "/malformed" after the version (or without a slash if there's no version to tell) — and if it's unset, you fail the detection.

It's generally nice to report files that are clearly of the detected format but are broken in some way, anyway. Two functions are there in "read" script to facilitate that: appendS and addIfNone. Quicker shown than explained, the code would look like this:
 ```js
bad = ""; ...
if(globalvolume > 0x40) bad = bad.addIfNone("!badgvol");
...

numericVersion = File.read_uint8(4);
if(numericVersion > 0) sVersion = "v"+numericVersion;
if(bad != "") sVersion.appendS("malformed"+bad,"/");
```
And if `numericVersion` is 2 and globalvolume's malformed, the version line would look like this:
`v2/malformed!badgvol`