#!/usr/bin/env python3

import sys

blank=''

vtt_header= 'WEBVTT\n\n'
#https://dvcs.w3.org/hg/text-tracks/raw-file/default/608toVTT/608toVTT.html

# I see no good reason convert to and from hex for these, when I can just do a look up.

char2code = {'':'91b9','’':'9229','Ø':'13ba','©':'92ab','Ì':'1323','ô':'913e','¢':'91b5','õ':'13a8','Ç':'9232',
'¦':'13ae','{':'1329','Ó':'92a2','Ò':'1325','\\':'13ab','ø':'133b','“':'92ae','Ë':'92b5','|':'1337','Õ':'13a7',
'┘':'13bf','Ô':'92ba','Ê':'9234','Ú':'9223','ö':'13b3','Î':'9237','ì':'13a4','£':'91b6','ä':'1331','”':'922f',
'¿':'91b3','Ö':'1332','┐':'133d','à':'9138','Å':'1338','«':'923e','î':'913d','Ü':'92a4','Ï':'9238','™':'9134',
'ò':'1326','Ã':'1320','ï':'92b9','*':'92a8','_':'13ad','Û':'923d','À':'92b0','â':'913b','┌':'13bc','ã':'13a1',
'¡':'92a7','®':'91b0','•':'92ad','ê':'91bc','~':'132f','ü':'9225','Ù':'923b','Ä':'13b0','ß':'1334','ù':'92bc',
'└':'133e','½':'9132','È':'92b3','É':'92a1','ë':'92b6','¥':'13b5','^':'132c','}':'132a','¤':'13b6','—':'922a',
'»':'92bf','Â':'9231','å':'13b9','°':'9131','‘':'9226','♪':'9137','℠':'922c','Á':'9220','è':'91ba','Í':'13a2','û':'91bf'}

chars=list(char2code.keys())

codes=list(char2code.values())

'''
Single-byte codes 0x20-0x7f map to the same Unicode code point, except for:

'''
w3c={'2a': 'á','5c': 'é','5e': 'í','5f': 'ó','60' :'ú',
'7b': 'ç','7c' :'÷','7d' :'Ñ','7e' :'ñ','7f' :'█'}

#9120   change to white, no formatting

drops=('9170','94ae','94ad','9420', '942c','942f','9425','9426','97a1','9454')



def fixup_9470(data):
    return data.replace(' 9470 9470',' 2080 9470 9470')

    
def fixup_newlines(text):
    '''
    Newline cleanup 
    I know this crazy, but it gives me consistent results, 
    despite format variations. If you have a better way, 
    speak up. 
    '''
    text=text.replace('\n\n\n','\n')
    text=text.replace('\n\n','\n')
    return text.replace('\n \n','\n')


def fixup_speaker(caps):
    '''
    Ensure new speaker indicators start on newlines
    '''
    text="".join(caps)
    return text.replace(' >>','>>')#.replace('>>','\n>>')
 
 
def scc2char(half_chunk):
    if half_chunk in w3c.keys(): return w3c[half_chunk]
    s='0x'+half_chunk
    i=int(s,16)
    if i in [80,128,138]: return "\n"
    if half_chunk[0] in 'abcdef': i= i ^ 0x80
    return chr(i)


def scc_time2vtt(line_time):
    lt=line_time.replace(":",".").replace(';','.')
    lt=lt.replace(".",":",2)
    while len(lt.split(".")[1]) < 2: lt=lt+"0"
    return lt


def clear_drops(chunk):
    '''
    drop the drops
    '''
    if chunk in drops: chunk= blank
    return chunk


def scc_chunk2char(chunk):
    '''
    take an scc chunk like '92ad'and see if it is listed in
    see if it's codes and return  chars with the same index
    '''
    decoded=blank
    if chunk in codes:
        idx=codes.index(chunk)
        decoded=chars[idx]
    return decoded


def scc_chunk2twochars(chunk):
    '''
    decode scc into chars
    '''
    decoded=blank
    chunk=chunk.lower()
    if chunk.startswith('9') or chunk.startswith('1'):
        decoded=scc_chunk2char(chunk)
    else:
        one,two=chunk[:2],chunk[2:]
        try:
            decoded=scc2char(one)
            decoded +=scc2char(two)
        except:
            decoded="%s%s"%(one,two)
    return decoded


def scc_dechunk(cap):
    '''
    split captions into chunks,and decode everything
    '''
    buffed=[]
    chunks=cap.split(' ')
    for chunk in chunks:
        chunk=clear_drops(chunk)
        if chunk is not blank:
            decoded=scc_chunk2twochars(chunk)
            buffed.append(decoded)
    return  buffed


def scc_split(scc_cues):
    '''
    times and captions are separated by a tab,
    '''
    scc_times=[]
    scc_caps=[]
    for cue in scc_cues:
        if '\t' in cue:
            sl=cue.split('\t')
            sl[1]=fixup_9470(sl[1])
            dechunked=scc_dechunk(sl[1])
            if len(dechunked) > 1:
                scc_times.append(sl[0])
                scc_caps.append(dechunked)
    return scc_times,scc_caps


def as_vtt(start,stop,cap):
    vtt_cue = '%(start)s --> %(stop)s\n%(cap)s' %{ 'start':start, 'stop': stop,'cap': cap}
    return vtt_cue


def vtt_start_stop(scc_start,scc_stop):
    vtt_start=scc_time2vtt(scc_start)
    vtt_stop=scc_time2vtt(scc_stop)
    return vtt_start,vtt_stop
	
	    
def write_vtt_file(outfile,vtt_cues):
    with open(outfile,'w+') as outfile:
        outfile.write(vtt_header)
        outfile.write('\n')
        for cue in vtt_cues:
            print(cue)
            print(fixup_newlines(cue))
            outfile.write(fixup_newlines(cue))
#            outfile.write(cue)
            outfile.write('\n')
    outfile.close()
    return outfile


def scc_decoder(infile,outfile):
    with open(infile)as infile:
        scc_data=infile.readlines()
        scc_times,scc_cues=scc_split(scc_data)
        vtt=[]
        scc_times.append("00:00:00.00") # add a final stop
        for i in range (len(scc_cues)-1): # minus the one we just added the loop
            start,stop=vtt_start_stop(scc_times[i],scc_times[i+1])
            cue =fixup_speaker(scc_cues[i])
            vtt.append(as_vtt(start,stop,cue))
    infile.close()	    
    write_vtt_file(outfile,vtt)
 