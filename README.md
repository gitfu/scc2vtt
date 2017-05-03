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
	scc2vtt.scc_decoder(infile,outfile)

```

* Run it like so.

```
python conv_scc.py  my_in.scc my_out.vtt


```
I love JavaScript, but I loathe switch statements.
Here's a way to have switch like functionality, but with objects instead.
This is a simple key listener that calls a different function for each of the arrow keys.  
You can open a browser console on any web page and copy and paste this code in.   



* This function is to stop the event.
```js
function squash(evt){
    	evt.preventDefault();
    	evt.stopPropagation();
	return false;
};
```
* The functions for each key
```js
function leftKey(){ 
	console.log("left key");
};

function upKey(){ 
	console.log("up key");
};

function rightKey(){ 
	console.log("right key");
};

function downKey (){ 
	console.log("down key");
};
```	 		

* This is the keychain object used to maqp keycodes to each function. 
```js
var keychain = { 37: leftKey
		, 38: upKey
		, 39: rightKey
		, 40: downKey
		};
```
* Finally the event listener
```js
document.onkeydown = function (e){
    	e  = e ||window.event
    	var k  = e.keyCode
    	squash(e)
    	if (keychain[k]){
        	keychain[k]()
    	}
}
```

* If you try this in a browser console, make sure to switch the focus back to the web when you press the keys. 




```



