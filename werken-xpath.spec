%{?_javapackages_macros:%_javapackages_macros}
# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define dotname werken.xpath

Name:           werken-xpath
Version:        0.9.4
Release:        12.beta.12.5.1%{?dist}
Epoch:          0
Summary:        XPath implementation using JDOM
License:        Saxpath
Source0:        %{name}-%{version}.tar.xz
Source1:        http://repo1.maven.org/maven2/%{name}/%{name}/%{version}/%{name}-%{version}.pom
# used to generate Source0, upstream has no tarball like this anymore
Source2:        generate-tarball.sh
Patch0:         %{name}-ElementNamespaceContext.patch
Patch1:         %{name}-Partition.patch
Patch2:         %{name}-ParentStep.patch
Patch3:         %{name}-NodeTypeStep.patch
Patch4:         %{name}-UnAbbrStep.patch
Patch5:         %{name}-StringFunction.patch
Patch6:         %{name}-Test.patch
Patch7:         %{name}-Driver.patch
Patch8:         %{name}-runtests_sh.patch
URL:            http://sourceforge.net/projects/werken-xpath/
Requires:       jdom
BuildRequires:  ant >= 0:1.6
BuildRequires:  antlr
BuildRequires:  jdom
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-apis
BuildRequires:  jpackage-utils >= 0:1.6

BuildArch:      noarch
Provides:       werken.xpath = %{epoch}:%{version}-%{release}
Obsoletes:      werken.xpath < 0.9.4

%description
werken.xpath is an implementation of the W3C XPath Recommendation, on
top of the JDOM library.  It takes as input a XPath expression, and a
JDOM tree, and returns a NodeSet (java.util.List) of selected
elements.  Is is being used in the development of the
as-yet-unreleased werken.xslt (eXtensible Stylesheet Language) and the
werken.canonical (XML canonicalization) packages.

%package        javadoc
Summary:        Javadoc for %{name}

BuildRequires:  java-javadoc
Provides:       werken.xpath-javadoc = %{epoch}:%{version}-%{release}
Obsoletes:      werken.xpath-javadoc < 0.9.4

%description    javadoc
Javadoc for %{name}.

# -----------------------------------------------------------------------------

%prep
%setup -q
%patch0
%patch1
%patch2
%patch3
%patch4
%patch5
%patch6
%patch7
%patch8

# remove all binary libs
for j in $(find . -name "*.jar"); do
         mv $j $j.no
done

cp %{SOURCE1} .

# -----------------------------------------------------------------------------

%build
export CLASSPATH=$(build-classpath jdom antlr xerces-j2 xml-commons-apis)
ant -Dbuild.compiler=modern package javadoc compile-test
# Note that you'll have to java in PATH for this to work, it is by default
# when using a JPackage JVM.
CLASSPATH=$CLASSPATH:build/werken.xpath.jar:build/test/classes
sh runtests.sh

# -----------------------------------------------------------------------------

%install
# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/%{dotname}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# maven
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 %{name}-%{version}.pom \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar


# -----------------------------------------------------------------------------

%files
%doc INSTALL LICENSE LIMITATIONS README TODO
%{_javadir}/*
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc LICENSE
%{_javadocdir}/%{name}

# -----------------------------------------------------------------------------

%changelog
* Wed Jul 31 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:0.9.4-12.beta.12.5
- Correct license tag to Saxpath

* Tue Jul 30 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:0.9.4-11.beta.12.5
- Provide script to generate clean tarball

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:0.9.4-10.beta.12.5
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.4-10.beta.12.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 12 2012 Michal Srb <msrb@redhat.com> - 0:0.9.4-9.beta.12.4
- Fixed name of the POM file (resolves: #655826)
- Moved from add_to_maven_depmap to add_maven_depmap
- Spec file cleanup

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.4-8.beta.12.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.4-7.beta.12.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.4-6.beta.12.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 30 2010 Alexander Kurtakov <akurtako@redhat.com> 0:0.9.4-5.beta.12.4
- Drop gcj support.
- No more versioned jars/javadoc.

* Sat Feb 13 2010 Mary Ellen Foster <mefoster at gmail.com> - 0:0.9.4-5.beta.12.3
- Add maven dependency information

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 0:0.9.4-4.beta.12.3
- Convert specfile to UTF-8.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.4-3.beta.12.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.4-2.beta.12.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:0.9.4-1.beta.12.3
- drop repotag
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:0.9.4-1.beta.12jpp.2
- Autorebuild for GCC 4.3

* Tue Mar 20 2007 Florian La Roche <laroche@redhat.com> 0:0.9.4-0.beta.12jpp.2
- change Provides:/Obsoletes: to standard way of epoch:version-release

* Fri Aug 18 2006 Fernando Nasser <fnasser@redhat.com> 0:0.9.4-0.beta.12jpp.1
- Merge with upstream
- Re-add define gcj_support

* Fri Aug 18 2006 Fernando Nasser <fnasser@redhat.com> 0:0.9.4-0.beta.12jpp
- Add requires for post and postun javadoc sections

* Thu Aug 03 2006 Fernando Nasser <fnasser@redhat.com> 0:0.9.4-0.beta.11jpp_2fc
- Remove define gcj_support and rebuild

* Tue Jul 25 2006 Fernando Nasser <fnasser@redhat.com> 0:0.9.4-0.beta.11jpp_1fc
- Merge with upstream

* Tue Jul 25 2006 Fernando Nasser <fnasser@redhat.com> 0:0.9.4-0.beta.11jpp
- Add missing header

* Fri May 05 2006 Ralph Apel <r.apel at r-apel.de> 0:0.9.4-0.beta.10jpp
- Rebuild for JPP-1.7

* Mon Aug 30 2004 Ralph Apel <r.apel at r-apel.de> 0:0.9.4-0.beta.9jpp
- Build with ant-1.6.2

* Thu Jan 22 2004 David Walluck <david@anti-microsoft.org> 0:0.9.4-0.beta.8jpp
- use oldjdom

* Sun May 25 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:0.9.4-0.beta.7jpp
- Add Epochs to dependencies.
- Add non-versioned javadoc symlinks.
- Add Distribution tag.

* Fri May 23 2003 Richard Bullington-McGuire <rbulling@pkrinternet.com> - 0.9.4-0.beta.6jpp
- Reworked spec file for JPackage 1.5 release

* Sun Mar  2 2003 Ville Skyttä <ville.skytta@iki.fi> - 0.9.4-0.beta.5jpp
- Fix Group, License and Distribution tags.
- Patched to work with recent JDOM versions.
- Run unit tests during build.
- Use sed instead of bash 2 extension when symlinking jars during build.
- Some spec file cleanup.

* Mon Jan 21 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 0.9.4-0.beta.4jpp
- versioned dir for javadoc
- no dependencies for javadoc package
- macro section
- prevented Jikes use

* Fri Dec 7 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 0.9.4-0.beta.3jpp
- javadoc into javadoc package

* Sat Oct 13 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 0.9.4-0.beta.2jpp
- first unified release
- used original archive
- s/jPackage/JPackage

* Tue Aug 28 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 0.9.4-0.beta.1mdk
- first Mandrake release
