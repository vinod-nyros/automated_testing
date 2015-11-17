# coding: utf-8

from lxml import etree, html
from pyquery import PyQuery

#### Utility functions for scraping

def innerhtml (e):

    return (e.text or '') + ''.join ([html.tostring(child) for child in e.iterchildren()]) + (e.tail or '')


def no_namespaces (s):
    s =  ' '.join (['>' if (t.strip().startswith ('xmlns:') and t.strip().endswith ('>')) else t for t in s.split(' ')])
    s =  ' '.join ([t for t in s.split(' ') if not t.strip().startswith ('xmlns:')])
    return s


def no_fonts (pq):  # yuk - lxml etree and PyQuery objs get confused - nested ones arent removed, this goes only 2 levels
    raise Exception, "yuk - it's a mess, use tidy!"

    pq = PyQuery (pq)
    #print fonts.__class__.__name__
    for font in pq ('font'):
        font = PyQuery (font)
        #font ('a').remove()
        #print font.__class__.__name__
        #print len (font), font [0]
        #print dir (font)
        #import sys
        #sys.exit()

        #inner = innerhtml (font)  # .text() #.replace (':','').strip()
        #print 'Replacing font with:', font.html()
        font.replaceWith (font.html())
        #font.getparent().replace (font, PyQuery (inner))
        print 'font replaced:', font [:60]

        #font = no_fonts (font)

    for font in pq ('font'):
        font = PyQuery (font)
        font.replaceWith (font.html())
        print 'font 2 replaced:', font [:60]

    return pq


if __name__ == '__main__':
    #print
    no_namespaces ('''
    <!-- now content page goes in this cell-->
<div class="big" xmlns:html="http://www.w3.org/1999/xhtml">
    Open Source Software Reading:</div>
<p xmlns:html="http://www.w3.org/1999/xhtml">
    &nbsp;</p>
<table border="0" bordercolor="#efefef" cellpadding="5" cellspacing="0" width="97%" xmlns:html="http://www.w3.org/1999/xhtml">
    <tbody>''')


    from pyquery import PyQuery

    rslt = no_fonts (PyQuery ('''

<table width="100%" cellpadding="3">
<tr><td align="left" valign="top">
<font face="verdana,geneva,sans-serif" color="#000000" size="4">
 eRacks Open Source Systems News
<font size="2"><p>Please <a href="mailto:info@eracks.com">email</a> or call for a Press Kit.
<p>
See examples of some of eRacks' <a href="./brochures/index_html">past brochures and flyers</a>.
</font>
</font>
</td><td align="right"><p>
<img src="/press/news" border="0">
</td></tr>

<tr><td colspan="2" valign="top" align="left">
<font face="verdana,geneva,sans-serif" color="#000000" size="2">

 <a href="120827">Aug 27, 2012 - eRacks Launches Amazon Storefront Featuring Custom Line of Computers and Servers</a><p>
 <a href="120521">May 21 , 2012 - theVARGuy.com: eRacks Offers High-End PC to Open Source Crowd</a><p>
 <a href="120518">May 18, 2012 - eRacks Announces AresPro Line of High Performance Desktop Computers Tailored For Engineers, Graphic Designers, Video Editors, and High-End Gamers</a><p>
 <a href="120509">May  09, 2012 - Top 50 Open Source Companies: Where Are They Now?</a><p>
 <a href="120425">April 25, 2012 - Custom NAS50 File Server from eRacks Makes Petabyte-scale Data Storage Accessible for Every Business </a><p>
 <a href="120409">April 09, 2012 - eRacks Introduces Eseries Line of Fast, Green Intel E5-Powered Rackmount Servers</a><p>
 <a href="120328">March  28, 2012 - ownCloud Launches Partner Program, Announces Partnerships Across the Globe</a><p>
 <a href="120315">March 15, 2012 - eRacks adds blade servers to its rackmount server line.</a><p>
 <a href="120201">Feb 01, 2012 - MakeTechEasier.com: 2012 Linux Computer Buyer's Guide</a><p>
 <a href="120130">Jan 30, 2012 - eRacks Bucks Server Trend Towards Higher Prices</a><p>
 <a href="111121">Nov 21, 2011 - eRacks releases line of Fully-Redundant Failover Firewalls</a><p>
 <a href="110909">Sep 9, 2011 - eRacks Open Source Systems Announces Reseller Agreement with Canonical</a><p>
 <a href="110825">Aug 25, 2011 - eRacks Releases AMD Fusion A-Series Desktop and Rackmount Computer Models</a><p>
 <a href="110705">July 5, 2011 - eRacks releases Intel Xeon E7-4800 and E7-8800 series rackmount servers</a><p>
 <a href="110429">Apr 29, 2011 - 10 Gigabit Ethernet Connectivity Available on eRacks Rackmount Servers. </a><p>
 <a href="110228">Feb 28, 2011 - eRacks/SANDYCORE - utilizing the second generation Intel Core processor, Sandy Bridge CPU</a><p>
 <a href="110123">Jan 23, 2011 - eRacks/FLAT: the Dust-proof and Silent Small Form Factor Computer</a><p>
 <a href="101222">Dec 22, 2010 - eRacks introduces the first 150TB storage server, bringing affordable petabyte-class storage to a space-hungry market.</a><p>
 <a href="100924">Sep 24, 2010 -      eRacks presents the OPT4100 AMD low energy, high power, affordable server.</a><p>
 <a href="100513">May 13, 2010 - eRacks releases the Opternator</a><p>
 <a href="100126">January 26, 2010 - eRacks Introduces largest NAS & DAS storage systems</a><p>
 <a href="090828">August 26, 2009 - eRacks introduces Cash for PC Clunkers program</a><p>
 <a href="090716">July 16, 2009 - eRacks Latest Virtualization Server Utilizes the Six-Core AMD Opteron Processor</a><p>
 <a href="090601">June 01, 2009 -eRacks Introduces an Energy-Saving Quad-Core Xeon 5000 Rackmount Server, the eRacks/NSERVE</a><p>
 <a href="090407">Apr 07, 2009 - eRacks Introduces a Behemoth 100TB Capacity 8U Rackmount Server</a><p>
 <a href="090306">Mar 06, 2009 - eRacks to debut AMD AM3 rackmount server with triple/quad core Phenom II CPUs</a><p>
 <a href="090223">Feb 23, 2009 - eRacks Announces New Shallow-Depth Rackmount Server for Broadcast and Audio Studios</a><p>
 <a href="090211">Feb 11, 2009 - eRacks Announces Significant Uptick in Demand for Open Source Systems</a><p>
 <a href="090108">Jan 08, 2009 - eRacks offers top netbooks preinstalled with Ubuntu and Fedora Linux</a><p>
 <a href="081215">Dec 15, 2008 - eRacks  Announces a Linux Intel Core i7 Desktop Computer </a><p>
 <a href="071207">Dec 7, 2007 - eRacks Open Source Systems announces eRacks Hosting, a division offering dedicated hosting services.</a><p>
 <a href="071019">Oct 19, 2007 - Desktop Linux: The wide world of pre-installed Ubuntu</a><p>
 <a href="070801">Aug 1, 2007 - eRacks offers a Virtualization Server Solution</a><p>
 <a href="070227">Feb 27, 2007 - eRacks enables donations to OpenBSD with rackmount server sales</a><p>
 <a href="070216">Feb 16, 2007 - eRacks partners with Canonical to promote Ubuntu Linux</a><p>
 <a href="061208">Dec 8, 2006  -  Processor Magazine: Server Quietization</a><p>
 <a href="060929">Sept 29, 2006  -  Processor Magazine: Ready-To-Run Desktops & Servers</a><p>
 <a href="060810">August 10, 2006  -  eRacks offers ready-to-run Ubuntu desktops and servers.</a><p>
 <a href="050525">May 25, 2005  -  Dual Redundant Firewalls with Failover in Single 1U Rackmount Offered by eRacks </a><p>
 <a href="050201">Feb 1, 2005 - eRacks Open Source Systems Enables & Matches Donation to EFF</a><p>
 <a href="040928">Sep 28, 2004 - eRacks Open Source Systems offers Leasing</a><p>
 <a href="040804">Aug 3, 2004 - eRacks Introduces a 4-way Opteron Server</a><p>
 <a href="040318">Mar 18, 2004 - eRacks Offers a New Level of Server Customization</a><p>
 <a href="031231">Dec 31, 2003 - eRacks Announces Linux Centrino Laptop</a><p>
 <a href="031021">Oct 21, 2003 - eRacks Expands Line of Quiet Computers</a><p>
 <a href="031008">Oct 8, 2003 - eRacks Contributes Web & Mail Server to OCLUG</a><p>
 <a href="030922">Sep 22, 2003  - eRacks Mirrors Two Terabytes in RealTime</a><p>
 <a href="030627">Jun 27, 2003  - eRacks Presents QUIET Rackmount Systems</a><p>
 <a href="030510">May 10, 2003 -  eRacks Presents Open Source Laptops</a><p>
 <a href="020226">Feb 26, 2002 - eRacks Announces ISP/ASP Partner Program</a><p>
 <a href="010420">April 20, 2001 - eRacks offers Preconfigured Rackmount Computers</a><p>

</font></td></tr></table>
    '''))


    print '\n\nAfter No Fonts:\n\n', rslt