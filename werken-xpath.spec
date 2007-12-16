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
Release:        %mkrel 0.beta.13.0.0.2
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
%patch0 -b .sav
%patch1 -b .sav
%patch2 -b .sav
%patch3 -b .sav
%patch4 -b .sav
%patch5 -b .sav
%patch6 -b .sav
%patch7 -b .sav
%patch8 -b .sav

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
