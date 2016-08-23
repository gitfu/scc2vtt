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
