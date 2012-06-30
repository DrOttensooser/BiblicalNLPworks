#!/usr/bin/python
# This script scans a text file and creates tags of the most used words.
# The script has been released under BSD license. Copyright (C) 2010 Reiner Rottmann <reiner@rottmann.it>

import string 

def sort_by_value(d): 
    u""" Returns the keys of dictionary d sorted by their values """ 
    items=d.items() 
    backitems=[ [v[1],v[0]] for v in items] 
    backitems.sort() 
    return [ backitems[i][1] for i in range(0,len(backitems))] 

def get_most_used_words(text, n):
    """ Returns the top n used words in a text without counting the top 100 most used words in English and German language"""
    
    # only print lower case words
    text =  text.lower()
    
    
    # replace seperators with spaces
    seperators = "\n\r\f\t\v.,/\\""''"
    #seperators = "\n\r.,"
    for seperator in seperators:
        #text = text.replace(seperator, " ")
        text = text.replace(seperator, " ")
    
    # remove invalid chars
    validchars = "abcdefghijklmnopqrstuvwxyz "
    
    charlist = list(text.lower())
    charlist = [char for char in charlist if char in validchars]
    text = "".join(charlist)
    
    # split up the words
    words  = text.split(" ")
    
    # remove empty list words
    words = [word for word in words if word != ""]
    
    # sort words
    words.sort()
    
    # define some blacklists for German, English language etc.
    blacklistde = "aber all als also an andere auch auf aus bei beispiel bis da damit dann das dass denn der die dies doch du durch eigentlich ein er erste es fuer ganz geben gehen gross gut haben hier ich ihm ihn ihr immer in ja jahr jede jetzt kein koennen kommen lang lassen machen Mal man mehr mein mich mir mit muessen nach neu nicht noch nur oben oder sagen schon sehen sehr sein sein selbst sich sie so sollen stehen ueber um und uns unser unter viel von vor was weil wenn werden wie wieder wir wissen wo wollen zeit zu zwei"
     
    blacklisten = "a about after again against all also and another any around as ask at back because become before begin between both but by call can change child come consider could course day develop do down during each early end even eye face fact feel few find first follow for form from general get give go good govern great group hand have he head help here high hold home house how however I if in increase interest into it just keep know large last late lead leave life like line little long look make man many may mean might more most move much must nation need never new no not now number of off old on one only open or order other out over own part people person place plan play point possible present problem program public real right run same say school see seem set she should show since small so some stand state still such system take tell than that the then there these they thing think this those through time to too turn under up use very want way we well what when where which while who will with without word work world would write year you"

    blacklistbash = "{ } && || $ alias break case continue do done elif else esac exit export fi for if in return set then unalias unset while /C2 halt ifconfig init initlog insmod linuxconf lsmod modprobe reboot rmmod route shutdown traceroute /C3 ] [ awk basename cat cp echo egrep fgrep gawk grep gzip kill killall less md mkdir mv nice pidof ps rd read rm rmdir sed sleep test touch ulimit uname usleep zcat zless"
    
    blacklistcode = "aasmlang abbr above absolute abstract accept acceptcharset access accesskey acos acronym action activate additem address alert align alink alpha alter anchor angle append applet application apply archive area areab arguments array ascending ascii asin assembler assert assign atan attach attr attribute attributes author authorization auto average axisbackground azaz azazazaz azazfunction azazindent back basefont beep before begin behavior bell below between bgcolor bgsound binary bitand bitmap bitnot bitor bitset blank blink block blockquote blue body bold bool boolean border bottom brace browse button buttoncaption byte call cancel caption cast catch ccdefault ccic ccie ccio ccir cdbl cdecl ceil ceiling cell cellspacing center chain change channel char character characters charat charoff chars charset chdir chdrive check checkbox checked checksum children chmod choice choose cint circle cite class classes classid clear click clip clipboard clng clock close closedir cluster code codebase codepage codetype colgroup collapse color colors cols colspan column columns command commands comment comments commit common compact compare compile compiler component compress compute concat condition confirm connect connected connection const constant constraint constructor container contains content contents context control convert coordsdata copy corr cosh count country create createobject cross csng curdir current currentdate currenttime cursor cursordatabase cycle database date dateadd datediff dateformat datepart datetime datevalue deallocate debug decimal declare decode default defer define defined definition delay delete deletefile delimiter delimiters depth desc descending describe description dest detach device dialog dictionary diff difference digits dimension direction directory disable disabled disconnect disk display distance distinct divide document doelse domain double doubleelse drag draw drop dtem dump edit editor eject element ellipse elseif elseunindent elsif embedfieldset empty enable enabled encoding encrypt endcase enddo endfor endfunction endif endloop endm endselect endswitch endwhile enter entity entry enum environ environment equal erase error eruser escape eval evaluate even event every exact except exception exchange exclusive exec execute exist exists expand extendsfalse extensions extern external false fclose feof ferror fetch fflush fgets field fields fieldset file fileclose filecopy filedelete fileexists filename fileopen files filesize filetype fill filter final finally find findnext finish fixed flag fldata float flock floor flush focus fold font fontcolor fontsize fontstyle fopen force foreach foreign form format formula forward found fputs frac frame frameborder frameset frameseth fread free freefile freq fseek ftell function functionget functions functionsabs getattr getdate getday getenv getfile getfullyear gethours getminutes getmonth getobject gets getseconds getsize gettext gettime getutcdate getutcminutes getutcmonth glob global gosub goto gotoif grant graphics gray grey grid group hash head header height help hidden hide high history home host hour href hreflang hspace html htmli htmllang httpequivid icdlevel icon identity ifdef ifndef iframe ignore ilayer image immediate implements import incdelimiters include increment indent index indexes indexof info initial initialize inkey inline inner input inputbox insert instance instr integer interface internal interrupt intersect interval invert ipaddress isalpha isarray isdate isdigit isempty isfinite isindex isindexkbd islower ismaplabel isnan isnull isnumber isnumeric isspace isupper item join kbdlabel keyf keys keywords label language large layer layout layoutmanager lcase lcdd leave left leftb leftmargin legend length level library like line lineno lines link list listbox listen listing listingmap load local locale localtime locate location lock loge long longdescmailto lookup loop lower lowercase ltrim macro margin marginheight marginwidth marker marquee mask master match matd math matrix maximum maxlength mean media median member memory menu menubar menuitem merge message messagebox meta method minimum minus minute miscformat mode model modify module month mouse mousedown mousemove move moveto multicol multicolnextid multiple multiplename names near newline newpage next nlssort nobr nocase node noframes nohref nolayer nolist none noquote noresize norm normal noscript noscriptobject noshadeobject note notor nowait null number numeric numpad object offset omega onblur onchange onclick once ondblclick onerror onfocus onkeydown onkeypress onkeyup online onload onmousedown onmousemove onmouseout onmouseover onmouseup onreset onselect onsubmit onunload open opendir operators optgroup optgroupp optimize option optional options order otherwise outer outfile outgoing output page pagesize pagewidth palette panel paragraph parallel param parameter parameters parent parse parseint part pascal password paste path pathname pattern pause pecc peek perform pfcontrol pfpf picture pipe pitch platform play plot plus pocon point poke poly polygon popen popup popupmenu position post power pragma precision prefix preq prev previous primary print printer printf prior priority private privileges proc procedure process product profile program prompt promptreadonly properties property protected public push query quit quote quoterange rand random randomize range rate readdir readfile readline readonly real receive record rect rectangle redim reference references refresh regexp region register relative release reload remote remove rename repeat replace replicate report request reset resize resource response restart restore restrict result resume retry returns reverse revoke rewind right rightmargin role rollback root roots rotate round rowcount rows rowspan rset rtrim rulesscheme samp save scale scan schema scope screen script scroll scrollbar scrolling search second sect section security seek segment select selected selection self send sendkeys sendmessage separate separator sequence server servername session setattr setdate setfocus sethours setlocale setsize settime setutchours setyear sfxa sfxb sfxc sfxd sfxe sfxf shape share shared shell shift short show sign signal signed single sinh size sizeof skip slice slider small smallint snapshot socket sort sound soundex source space spacer spaces spacing span splice spline split sprintf spusercounter sqrt srand srcp stack stage standard standby start stat state statement static statistics status stddev step stop storage store strcat strcmp stream strike string strings strip strlen strong strstr struct structure stuff style stylesheet subc subject subset substitute substr substring subtract subtype summary super suptable svsv swap switch symbol symbols table tables tanh target task tazaz tazazfunction tbody tcdp tcecp tcon tcscp temp template term terminate text textarea textcolor textfield textheight textsize textwidth tfoot tfunction thead thenunindent thread throw timeout timer times timestamp timevalue timezone tindent title today tolower tolowercase topmargin tostring total toupper touppercase trans transaction transform translate trap trigger trim true trunc truncate type typeurl ucase ulvar umask undef underline unindent union unique unlink unload unlock unpack unshift until update upper uppercase usemapvalign user userid userkey username using valid validate value values valuetype varchar variable variables varwbrxmp vector verify version view visibility visible vlink wait warning wend width window word work wrap write"
    
    blacklistuser = "does setup site talk usage uses versions working written your"
    
    # be picky what to include in the word list
    sorted = {}
    for word in words:
        # accept only words with lenght between 3 and 15
        if len(word) > 3 and len(word) < 15:
            # accept only words that are not in blacklists of the top 100 common words and in various user blacklists
                if word not in blacklistde and word not in blacklisten and word not in blacklistuser and word not in blacklistbash and word not in blacklistcode:
                    sorted[word] = sorted.get(word,0) + 1
   
    # use only the top n words
    top =  sort_by_value(sorted)[-n:]
    
    # don't use the number of occurances as sort criteria anymore
    top.sort()
        
    return " ".join(top)

def usage():
    """ This function prints the usage information"""
    import sys
    print """This script has been released under BSD license. Copyright (C) 2010 Reiner Rottmann <reiner@rottmann.it>

keywords.py analyzes a text file and prints a list of the top 25 used words.

Usage: ./keywords.py  [textfile] [-]

Examples:
 $ ./keywords.py kernel-parameters.txt
 boot default device devices disable driver...
 
 $ echo "Lorem ipsum..."  | ./keywords.py -
 assentior lorem molestie mollis mundi...  """
    sys.exit(1)

def main():
    """ This is the main function"""
    import sys
    # check whether no commandline argument has been entered and show usage
    if len(sys.argv) == 1:
        usage()
    else:
        # read from stdin if "-" is present as first commandline argument
        if sys.argv[1] == "-":
            text = sys.stdin.read()
        else:
            # open file in any other case; should there be errors, print error message and usage
            try:    
                file = sys.argv[1]
                fd = open(file, 'r')
                text = fd.read()
                fd.close()
            except:
                print "ERROR: Input file could not be opened."
                usage()
    # get top 25 used words
    print get_most_used_words(text,25)

# run main function if called directly
if __name__=="__main__":
   main() 
