# scc2vtt
Translates Scenarist SCC  closed captions to WebVTT 

### Requires Python3

* This is a work in progress, 
* The times and text are accurate, however no formating or positioning is retained .
* Rollups are removed. 
* Sys.argv[1] is the input , 
* if sys.argv[2] is present it's the output,  else the output file is call out.vtt


## How to use

* Full working example.

* Create conv_scc.py  
* Write this to  conv_scc.py 
```
import scc2vtt
import sys


def name_files():
	if len(sys.argv) > 1:
		infile=sys.argv[1]
		try: outfile=sys.argv[2]
		except: outfile="out.vtt"
	return infile,outfile

if __name__=='__main__':
	infile,outfile=name_files()
	scc_decoder(infile,outfile)

```

* Run it like so.

```
python conv_scc.py  my_in.scc my_out.vtt
````
