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

def scc2char(half_chunk):
    if half_chunk in w3c.keys():
        return w3c[half_chunk]
    s='0x'+half_chunk
    i=int(s,16)
    if i in [80,128,138]:
        return "\n"
    if half_chunk[0] in 'abcdef':
        i= i ^ 0x80
    return chr(i)

def scc_time2vtt(line_time):
    lt=line_time.replace(":",".")
    lt=lt.replace(".",":",2)
    while len(lt.split(".")[1]) < 3:
        lt=lt+"0"

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
    decode scc into chaars
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


def scc_dechunk(chunked):
    '''
    split captions into chunks,and decode everything
    '''
    buffed=[]
    chunks=chunked.split(' ')
    for chunk in chunks:
        chunk=clear_drops(chunk)
        if chunk is not blank:
            decoded=scc_chunk2twochars(chunk)
            buffed.append(decoded)
    return  buffed

def scc_split(scc_data):
    '''
    times and captions are separated by a tab,
    '''
    scc_times=[]
    scc_caps=[]
    for line in scc_data:
        if '\t' in line:
            sl=line.split('\t')
            dechunked=scc_dechunk(sl[1])
            if len(dechunked) > 1:
                scc_times.append(sl[0])
                scc_caps.append(dechunked)
    return scc_times,scc_caps

def as_vtt(start,stop,text):
    if text.startswith('>>'):
        text='-'+text[2:]
    vtt_data = ['%(start)s --> %(stop)s ' %{ 'start':start, 'stop': stop},
    '%(text)s \n\n' %{'text':text}]
    return '\n'.join(vtt_data)

def unroll(newcaps,lastcaps):
    text=''.join(newcaps)
    try: lastline="".join(lastcaps).split('\n')[-2].strip()
    except: lastline=""
    thisline=text.split('\n')[0].strip()
    if thisline==lastline:
        text=text.replace(lastline,'')
    text=text.strip()
    return text

def scc_decoder(infile,outfile):
    with open(infile)as infile:
        scc_data=infile.readlines()
        scc_times,scc_caps=scc_split(scc_data)
        vtt=[vtt_header]
        for i in range (len(scc_caps)):
            start=scc_time2vtt(scc_times[i])
            try: stop=scc_time2vtt(scc_times[i+1])
            except: stop="00:00:00.000"
            text=unroll(scc_caps[i],scc_caps[i-1])
            vtt.append(as_vtt(start,stop,text))
            
    with open(outfile,'w+') as outfile:
        outfile.write(''.join(vtt))
        print(outfile.read())   
    return outfile
