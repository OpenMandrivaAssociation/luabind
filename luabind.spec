%global debug_package %{nil}

%define major 0.9.0
%define libname %mklibname luabind %{major}
%define devname %mklibname luabind -d

Name: luabind
Version: 0.9.1
Release: 1
Source0: https://downloads.sourceforge.net/project/luabind/luabind/%{version}/luabind-%{version}.tar.gz
Summary: Library that helps create bindings between C++ and Lua
URL: http://www.rasterbar.com/products/luabind.html
License: MIT
Group: System/Libraries
BuildRequires: boost-build >= 1.63.0-2
BuildRequires: boost-devel
BuildRequires: pkgconfig(luajit)
Patch0: luabind-0.9.1-luajit.patch
# Stolen from Fedora
Patch100: https://src.fedoraproject.org/cgit/rpms/luabind.git/plain/luabind-0.9.1-boost149fix.patch
Patch101: https://src.fedoraproject.org/cgit/rpms/luabind.git/plain/001-luabind-use-lua_compare.patch
Patch102: https://src.fedoraproject.org/cgit/rpms/luabind.git/plain/002-luabind-deprecated-LUA_GLOBALSINDEX.patch
Patch103: https://src.fedoraproject.org/cgit/rpms/luabind.git/plain/003-luabind-use-lua_rawlen.patch
Patch104: https://src.fedoraproject.org/cgit/rpms/luabind.git/plain/004-luabind-getsetuservalue.patch
Patch105: https://src.fedoraproject.org/cgit/rpms/luabind.git/plain/005-luabind-lua_resume_extra_param.patch
Patch106: https://src.fedoraproject.org/cgit/rpms/luabind.git/plain/006-luabind-luaL_newstate.patch
Patch107: https://src.fedoraproject.org/cgit/rpms/luabind.git/plain/007-luabind-lua-52-fix-test.patch
Patch108: https://src.fedoraproject.org/cgit/rpms/luabind.git/plain/008-luabind-lua_pushglobaltable.patch
Patch109: https://src.fedoraproject.org/cgit/rpms/luabind.git/plain/luabind-0.9.1-boost157fix.patch

%description
Luabind is a library that helps you create bindings between C++ and Lua.
It has the ability to expose functions and classes, written in C++,
to Lua.
It will also supply the functionality to define classes in lua and let
them derive from other lua classes or C++ classes. Lua classes can override
virtual functions from their C++ baseclasses.

It is implemented utilizing template meta programming. That means that you
don't need an extra preprocess pass to compile your project (it is done by
the compiler). It also means you don't (usually) have to know the exact
signature of each function you register, since the library will generate
code depending on the compile-time type of the function (which includes
the signature). The main drawback of this approach is that the compilation
time will increase for the file that does the registration, it is therefore
recommended that you register everything in the same cpp-file.

%package -n %{libname}
Summary: Library that helps create bindings between C++ and Lua
Group: System/Libraries

%description -n %{libname}
Luabind is a library that helps you create bindings between C++ and Lua.
It has the ability to expose functions and classes, written in C++,
to Lua.
It will also supply the functionality to define classes in lua and let
them derive from other lua classes or C++ classes. Lua classes can override
virtual functions from their C++ baseclasses.

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

Luabind is a library that helps you create bindings between C++ and Lua.
It has the ability to expose functions and classes, written in C++,
to Lua.
It will also supply the functionality to define classes in lua and let
them derive from other lua classes or C++ classes. Lua classes can override
virtual functions from their C++ baseclasses.

%prep
%setup -q
%apply_patches
%if "%{_lib}" != "lib"
sed -i -e "s,/lib ,/%{_lib} ,g" Jamroot
%endif

%build
bjam %{?_smp_mflags} -d+2 "cxxflags=%{optflags}" release

%install
bjam %{?_smp_mflags} -d+2 --prefix=%{buildroot}%{_prefix} --libdir=%{buildroot}%{_libdir} "cxxflags=%{optflags}" release install

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
