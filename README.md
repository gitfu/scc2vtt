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
```js
function squash(evt)
    	evt.preventDefault();
    	evt.stopPropagation();
	return false;
}

function leftKey(){ 
	console.log("left key");
}

function upKey(){ 
	console.log("up key");
}

function rightKey(){ 
	console.log("right key");
}

function downKey (){ 
	console.log("down key");
}
	 		


document.onkeydown = function(evt) {	
    evt = evt || window.event;
    var k  = evt.keyCode
    squash(evt)
    switch (k) {
        case 37:
		leftKey();
		break;
        case 39:
		rightKey();
		break;
	case 38:
		upKey();
		break;
        case 40:
		downKey();
		break;
    }
};

var keychainOne { 37: leftKey
		, 38: upKey
		, 39: rightKey
		, 40: downKey
		}


document.onkeydown = function (e){
    	e  = e ||window.event
    	var k  = e.keyCode
    	squash(e)
    	if (keychain[k]){
        	keychain[k]()
    	}
}







```



