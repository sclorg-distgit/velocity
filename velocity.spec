%global pkg_name velocity
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

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

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.7
Release:        10.12%{?dist}
Epoch:          0
Summary:        Java-based template engine
License:        ASL 2.0
URL:            http://velocity.apache.org/
Source0:        http://www.apache.org/dist/%{pkg_name}/engine/%{version}/%{pkg_name}-%{version}.tar.gz
Source1:        http://repo1.maven.org/maven2/org/apache/%{pkg_name}/%{pkg_name}/%{version}/%{pkg_name}-%{version}.pom
Patch0:         0001-Remove-avalon-logkit.patch
Patch2:         0003-Use-system-jars.patch
Patch3:         0004-JDBC-41-compat.patch
Patch4:         0001-Don-t-use-Werken-XPath.patch
Requires:       %{?scl_prefix_java_common}apache-commons-collections
Requires:       %{?scl_prefix_java_common}apache-commons-logging
Requires:       %{?scl_prefix_java_common}apache-commons-lang
Requires:       %{?scl_prefix_java_common}tomcat-servlet-3.0-api
Requires:       %{?scl_prefix_java_common}jakarta-oro
Requires:       %{?scl_prefix_java_common}junit
Requires:       hsqldb
Requires:       %{?scl_prefix_java_common}jaxen
Requires:       %{?scl_prefix_java_common}jdom
Requires:       %{?scl_prefix_java_common}bcel
Requires:       %{?scl_prefix_java_common}log4j

BuildRequires:  %{?scl_prefix_java_common}ant
BuildRequires:  %{?scl_prefix_java_common}antlr-tool
BuildRequires:  %{?scl_prefix_java_common}junit
BuildRequires:	%{?scl_prefix_java_common}ant-junit
BuildRequires:  hsqldb
BuildRequires:  %{?scl_prefix_java_common}apache-commons-collections
BuildRequires:  %{?scl_prefix_java_common}apache-commons-logging
BuildRequires:  %{?scl_prefix_java_common}apache-commons-lang
BuildRequires:  %{?scl_prefix_java_common}tomcat-servlet-3.0-api
BuildRequires:  %{?scl_prefix_java_common}jakarta-oro
BuildRequires:  %{?scl_prefix_java_common}jaxen
BuildRequires:  %{?scl_prefix_java_common}jdom
BuildRequires:  %{?scl_prefix_java_common}bcel
BuildRequires:  %{?scl_prefix_java_common}log4j
BuildRequires:  %{?scl_prefix_java_common}javapackages-tools

# It fails one of the arithmetic test cases with gcj
BuildArch:      noarch

%description
Velocity is a Java-based template engine. It permits anyone to use the
simple yet powerful template language to reference objects defined in
Java code.
When Velocity is used for web development, Web designers can work in
parallel with Java programmers to develop web sites according to the
Model-View-Controller (MVC) model, meaning that web page designers can
focus solely on creating a site that looks good, and programmers can
focus solely on writing top-notch code. Velocity separates Java code
from the web pages, making the web site more maintainable over the long
run and providing a viable alternative to Java Server Pages (JSPs) or
PHP.
Velocity's capabilities reach well beyond the realm of web sites; for
example, it can generate SQL and PostScript and XML (see Anakia for more
information on XML transformations) from templates. It can be used
either as a standalone utility for generating source code and reports,
or as an integrated component of other systems. Velocity also provides
template services for the Turbine web application framework.
Velocity+Turbine provides a template service that will allow web
applications to be developed according to a true MVC model.

%package        manual
Summary:        Manual for %{pkg_name}
Requires:       %{?scl_prefix}runtime

%description    manual
Documentation for %{pkg_name}.

%package        javadoc
Summary:        Javadoc for %{pkg_name}

%description    javadoc
Javadoc for %{pkg_name}.

%package        demo
Summary:        Demo for %{pkg_name}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    demo
Demonstrations and samples for %{pkg_name}.

# -----------------------------------------------------------------------------

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

# remove bundled libs/classes (except those used for testing)
find . -name '*.jar' -o -name '*.class' -not -path '*test*' -print -delete

# Remove dependency on avalon-logkit
rm -f src/java/org/apache/velocity/runtime/log/AvalonLogChute.java
rm -f src/java/org/apache/velocity/runtime/log/AvalonLogSystem.java
rm -f src/java/org/apache/velocity/runtime/log/VelocityFormatter.java

# need porting to new servlet API. We would just add a lot of empty functions
rm  src/test/org/apache/velocity/test/VelocityServletTestCase.java

cp %{SOURCE1} ./pom.xml

# remove rest of avalon logkit refences
%patch0 -p1

# Use system jar files instead of downloading from net
%patch2 -p1

%patch3 -p1

# Use jdom instead of werken-xpath
%patch4 -p1
%pom_remove_dep werken-xpath:

# -----------------------------------------------------------------------------
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
export CLASSPATH=$(build-classpath \
antlr \
apache-commons-collections \
commons-lang \
commons-logging \
tomcat-servlet-api \
junit \
jakarta-oro \
log4j \
jaxen \
jdom \
bcel \
junit):%{_root_datadir}/java/hsqldb.jar
ant \
  -buildfile build/build.xml \
  -Dbuild.sysclasspath=first \
  jar javadocs test

# fix line-endings in generated files
sed -i 's/\r//' docs/api/stylesheet.css docs/api/package-list

# -----------------------------------------------------------------------------
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

# jars
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 bin/%{pkg_name}-%{version}.jar %{buildroot}%{_javadir}/%{pkg_name}.jar

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr docs/api/* %{buildroot}%{_javadocdir}/%{name}

# data
install -d -m 755 %{buildroot}%{_datadir}/%{pkg_name}
cp -pr examples test %{buildroot}%{_datadir}/%{pkg_name}

# Maven metadata
install -pD -T -m 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{pkg_name}.pom

%add_maven_depmap -a "%{pkg_name}:%{pkg_name}"
%{?scl:EOF}


%files -f .mfiles
%doc LICENSE NOTICE README.txt

%files manual
%doc LICENSE NOTICE
%doc docs/*

%files javadoc
%doc LICENSE NOTICE
%{_javadocdir}/%{name}

%files demo
%doc LICENSE NOTICE
%{_datadir}/%{pkg_name}

%changelog
* Wed Jan 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-10.12
- Add requires on SCL filesystem package

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 0:1.7-10.11
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michal Srb <msrb@redhat.com> - 1.7-10.10
- Fix BR/R

* Wed Jan 07 2015 Michal Srb <msrb@redhat.com> - 1.7-10.9
- Migrate to .mfiles

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 0:1.7-10.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-10.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-10.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-10.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-10.4
- Remove requires on java

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 0:1.7-10.3
- SCL-ize BR/R

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-10.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-10.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 01.7-10
- Mass rebuild 2013-12-27

* Fri Sep 27 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-9
- Port from werken-xpath to jdom
- Resolves: rhbz#875817

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-8
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7-6
- Install NOTICE files
- Resolves: rhbz#879021

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 05 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7-4
- Use new tomcat-servlet-api
- Update to latest guidelines

* Fri Feb 17 2012 Deepak Bhole <dbhole@redhat.com> - 0:1.7-3
- Resolved rhbz#791045
- Added patch from Omaid Majid <omajid@redhat.com> to fix build with Java 7

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 21 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7-1
- Update to latest version
- Drop old patches

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.6.4-2
- Add compatibility depmap

* Wed Nov  3 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.6.4-1
- Rebase to latest upstream
- Fix problems from bz#226525

* Thu Oct 14 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.6.3-5
- Use apache-commons-collections instead of jakarta name
- Use tomcat6 for dependency instead of tomcat5 (bz#640660)

* Mon Jun 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.6.3-4
- Fix BR/R for jakarta-commons-rename.

* Sat Feb 13 2010 Mary Ellen Foster <mefoster at gmail.com> 0:1.6.3-3
- Get (Build)Requires right

* Sat Feb 13 2010 Mary Ellen Foster <mefoster at gmail.com> 0:1.6.3-2
- Require all of the packages in the POM
- Add dist to version

* Fri Jan 15 2010 Mary Ellen Foster <mefoster at gmail.com> 0:1.6.3-1
- Update to 1.6.3
- Remove dependency on avalon-logkit
- Add maven metadata and pom

* Sun Jan 10 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4-10.5
- Drop gcj_support.
- Fix groups and url.
- Use upstream tarball.

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 0:1.4-10.4
- Convert specfile to UTF-8.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-9.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 24 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 0:1.4-8.4
- Fix FTBFS: added velocity-enum.patch (enum is a reserved keyword in java >= 1.5)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-8.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.4-7.3
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.4-7jpp.2
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.4-7jpp.1
- Autorebuild for GCC 4.3

* Tue Aug 08 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:1.4-6jpp.1
- Resync with latest from JPP.
- Partially adopt new naming convention.

* Sat Jul 22 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:1.4-5jpp_2fc
- Rebuilt

* Sat Jul 22 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:1.4-5jpp_1fc
- Merge with latest from JPP.
- Remove fileversion and my_version macros.
- Remove notexentests patch and replace with a patch to disable
- failure on tests.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.4-3jpp_8fc
- Rebuilt

* Tue Jul 18 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.4-3jpp_7fc
- Build on all archs.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:1.4-3jpp_6fc
- rebuild

* Wed Mar  8 2006 Rafael Schloming <rafaels@redhat.com> - 0:1.4-3jpp_5fc
- excluded s390[x] and ppc64 due to eclipse

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:1.4-3jpp_4fc
- stop scriptlet spew

* Wed Dec 21 2005 Jesse Keating <jkeating@redhat.com> - 0:1.4-3jpp_3fc
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> - 0:1.4-3jpp_2fc
- rebuilt

* Tue Nov  8 2005 Vadim Nasardinov <vadimn@redhat.com> - 0:1.4-3jpp_1fc
- Converted from ISO-8859-1 to UTF-8

* Wed Jun 15 2005 Gary Benson <gbenson@redhat.com> 0:1.4-3jpp_1fc
- Build into Fedora.

* Thu Jun  9 2005 Gary Benson <gbenson@redhat.com>
- Remove jarfiles from the tarball.

* Mon Jun  6 2005 Gary Benson <gbenson@redhat.com>
- Build with servletapi5.
- Add NOTICE file as per Apache License version 2.0.
- Skip some failing tests.

* Mon Oct 18 2004 Fernando Nasser <fnasser@redhat.com> 0:1.4-3jpp_1rh
- First Red Hat build

* Thu Sep 23 2004 Ralph Apel <r.apel at r-apel.de> 0:1.4-3jpp
- Adapt to jdom-1.0-1 replacing org.jdom.input.DefaultJDOMFactory
  by org.jdom.DefaultJDOMFactory in AnakiaJDOMFactory.java
  as well as using org.jdom.output.Format in AnakiaTask.java
- Therefore require jdom >= 0:1.0-1

* Thu Sep 02 2004 Ralph Apel <r.apel at r-apel.de> 0:1.4-2jpp
- Build with ant-1.6.2

* Mon Jun 07 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.4-1jpp
- 1.4 final
- Patch #0 is unnecessary (upstream)
- We have to build velocity against servletapi3

* Wed Feb 18 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.4-0.rc1.2jpp
- Fix a few jpackage related .spec typos, oops.

* Wed Feb 18 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.4-0.rc1.1jpp
- Added Patch #0 (velocity-1.4-rc1-ServletTest.patch) from CVS which fixes
  build problems.

* Sun May 25 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:1.3.1-2jpp
- Add Epochs to dependencies.
- Add explicit defattrs.
- Add non-versioned javadoc symlinks.
- Use sed instead of bash 2 extension when symlinking jars during build.
- Use full URL in Source.
- Fix -javadoc Group tag.
- Drop patch in favour of ant options.
- BuildRequire jpackage-utils and antlr (latter needed for Anakia tests).

* Sat May 24 2003 Richard Bullington-McGuire <rbulling@pkrinternet.com> 1.3.1-1jpp
- 1.3.1 stable release

* Fri May 23 2003 Richard Bullington-McGuire <rbulling@pkrinternet.com> 1.3-1jpp
- 1.3 stable release
- Updated for JPackage 1.5
- Run JUnit regression tests as part of the build process
- Added patch file to fix test case classpath for JUnit standard locations

* Mon May 06 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.3-0.rc1.1jpp
- 1.3.0rc1
- dropped patch
- versioned dir for javadoc
- no dependencies for manual and javadoc packages
- stricter dependency for demo package

* Wed Dec 12 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2-1jpp
- 1.2
- regenerated patch and corrected manifest
- requires and buildrequires jdom >= 1.0-0.b7.1

* Wed Dec 5 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1-4jpp
- javadoc into javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.1-3jpp
- removed packager tag
- new jpp extension

* Thu Nov 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1-2jpp
- first unified release
- s/jPackage/JPackage

* Fri Sep 14 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1-1jpp
- first Mandrake release
