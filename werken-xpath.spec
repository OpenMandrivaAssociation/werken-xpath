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
Release:        6.beta.12.4
Summary:        XPath implementation using JDOM
# Worth noting that this ASL 1.1 has slightly different wording.
# It may be GPL compatible as a result.
License:        ASL 1.1
Source0:        %{dotname}-%{version}-beta-src.tar.gz
Source1:        http://repo1.maven.org/maven2/%{name}/%{name}/%{version}/%{name}-%{version}.pom
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
Group:          Development/Java
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:    werken.xpath = %{version}-%{release}
Obsoletes:   werken.xpath < 0.9.4

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
BuildRequires:  java-javadoc
Provides:    werken.xpath-javadoc = %{version}-%{release}
Obsoletes:   werken.xpath-javadoc < 0.9.4

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

cp %{SOURCE1} .

#pushd lib
#ln -sf $(build-classpath antlr) antlr-runtime.jar
#ln -sf $(build-classpath jdom) jdom.jar
#ln -sf $(build-classpath xerces-j2) xerces.jar
#popd

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
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/%{dotname}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# maven
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 %{name}-%{version}.pom \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}.pom
%add_to_maven_depmap %{name} %{name} %{version} JPP %{name}


# -----------------------------------------------------------------------------

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc INSTALL LICENSE LIMITATIONS README TODO
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

# -----------------------------------------------------------------------------

