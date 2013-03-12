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

%define _with_gcj_support 1
%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

%define dotname werken.xpath

%define section free

Name:           werken-xpath
Version:        0.9.4
Release:        0.beta.13.0.0.5
Epoch:          0
Summary:        XPath implementation using JDOM
License:        Apache Software License-like
Source0:        %{dotname}-%{version}-beta-src.tar.gz
Source1:        %{name}-%{version}.pom
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
BuildRequires:	antlr-java
BuildRequires:  jdom
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-apis
BuildRequires:  java-rpmbuild >= 0:1.7.2
Group:          Development/Java
%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:    werken.xpath = %{epoch}:%{version}-%{release}
Obsoletes:   werken.xpath < %{epoch}:%{version}-%{release}

%if %{gcj_support}
BuildRequires:		java-gcj-compat-devel
%endif

%description
werken.xpath is an implementation of the W3C XPath Recommendation, on
top of the JDOM library.  It takes as input a XPath expression, and a
JDOM tree, and returns a NodeSet (java.util.List) of selected
elements.  Is is being used in the development of the
as-yet-unreleased werken.xslt (eXtensible Stylesheet Language) and the
werken.canonical (XML canonicalization) packages.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
BuildRequires:  java-1.5.0-gcj-javadoc
Provides:    werken.xpath-javadoc = %{epoch}:%{version}-%{release}
Obsoletes:   werken.xpath-javadoc < %{epoch}:%{version}-%{release}

%description    javadoc
Javadoc for %{name}.

# -----------------------------------------------------------------------------

%prep
%setup -q -n %{dotname}
%patch0 -p0 -b .sav
%patch1 -p0 -b .sav
%patch2 -p0 -b .sav
%patch3 -p0 -b .sav
%patch4 -p0 -b .sav
%patch5 -p0 -b .sav
%patch6 -p0 -b .sav
%patch7 -p0 -b .sav
%patch8 -p0 -b .sav

# remove all binary libs
for j in $(find . -name "*.jar"); do
	mv $j $j.no
done

#pushd lib
#ln -sf $(build-classpath antlr) antlr-runtime.jar
#ln -sf $(build-classpath jdom) jdom.jar
#ln -sf $(build-classpath xerces-j2) xerces.jar
#popd

# -----------------------------------------------------------------------------

%build
export CLASSPATH=$(build-classpath jdom antlr xerces-j2 xml-commons-apis)
%{ant} -Dbuild.compiler=modern package javadoc compile-test
# Note that you'll have to java in PATH for this to work, it is by default
# when using a JPackage JVM.
CLASSPATH=$CLASSPATH:build/werken.xpath.jar:build/test/classes
sh runtests.sh

# -----------------------------------------------------------------------------

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/%{dotname}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done
ln -sf %{name}.jar %{dotname}.jar)

# pom
mkdir -p $RPM_BUILD_ROOT%{_datadir}/maven2/default_poms
cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/maven2/default_poms/JPP-werken-xpath.pom
%add_to_maven_depmap %{name} %{name} %{version} JPP %{name}

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
# -----------------------------------------------------------------------------

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc INSTALL LICENSE LIMITATIONS README TODO
%{_javadir}/*
%{_datadir}/maven2/default_poms/*
%{_mavendepmapfragdir}

%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/werken-xpath-0.9.4.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

# -----------------------------------------------------------------------------


%changelog
* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0:0.9.4-0.beta.13.0.0.4mdv2011.0
+ Revision: 608164
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:0.9.4-0.beta.13.0.0.3mdv2010.1
+ Revision: 524314
- rebuilt for 2010.1

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0:0.9.4-0.beta.13.0.0.2mdv2009.0
+ Revision: 136572
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:0.9.4-0.beta.13.0.0.2mdv2008.1
+ Revision: 121045
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Wed Dec 12 2007 Alexander Kurtakov <akurtakov@mandriva.org> 0:0.9.4-0.beta.13.0.0.1mdv2008.1
+ Revision: 117708
- add maven poms (jpp sync)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:0.9.4-0.beta.12.0.0.2mdv2008.0
+ Revision: 87246
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat
- fix obsoletes on werken.xpath

* Tue Sep 04 2007 David Walluck <walluck@mandriva.org> 0:0.9.4-0.beta.12.0.0.1mdv2008.0
+ Revision: 78968
- Import werken-xpath



* Fri Aug 18 2006 Fernando Nasser <fnasser@redhat.com> 0:0.9.4-0.beta.12jpp
- Add requires for post and postun javadoc sections

* Tue Jul 25 2006 Fernando Nasser <fnasser@redhat.com> 0:0.9.4-0.beta.11jpp
- Add missing header

* Fri May 05 2006 Ralph Apel <r.apel at r-apel.de> 0:0.9.4-0.beta.10jpp
- Rebuild for JPP-1.7

* Mon Aug 30 2004 Ralph Apel <r.apel at r-apel.de> 0:0.9.4-0.beta.9jpp
- Build with ant-1.6.2

* Thu Jan 22 2004 David Walluck <david@anti-microsoft.org> 0:0.9.4-0.beta.8jpp
- use oldjdom

* Sun May 25 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.9.4-0.beta.7jpp
- Add Epochs to dependencies.
- Add non-versioned javadoc symlinks.
- Add Distribution tag.

* Fri May 23 2003 Richard Bullington-McGuire <rbulling@pkrinternet.com> - 0.9.4-0.beta.6jpp
- Reworked spec file for JPackage 1.5 release

* Sun Mar  2 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.9.4-0.beta.5jpp
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
