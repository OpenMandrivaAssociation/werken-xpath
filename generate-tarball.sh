cvs -d:pserver:anonymous@werken-xpath.cvs.sourceforge.net:/cvsroot/werken-xpath login 
cvs -z3 -d:pserver:anonymous@werken-xpath.cvs.sourceforge.net:/cvsroot/werken-xpath co \
    -D 2013-07-01 -P werken.xpath-jdom

mv werken.xpath-jdom werken-xpath-0.9.4

# remove files with unknown licensing
rm werken-xpath-0.9.4/lib/*.jar

find werken-xpath-0.9.4 -name CVS -type d -exec rm -rf \{\} \;
tar cJf werken-xpath-0.9.4.tar.xz werken-xpath-0.9.4
