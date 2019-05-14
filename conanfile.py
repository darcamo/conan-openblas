import os
import shutil
from conans import ConanFile, CMake, tools


class OpenblasConan(ConanFile):
    name = "openblas"
    version = "0.3.6"
    license = "https://raw.githubusercontent.com/xianyi/OpenBLAS/develop/LICENSE"
    author = "Darlan Cavalcante Moreira (darcamo@gmail.com)"
    url = "https://github.com/darcamo/conan-openblas"
    description = "OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "DYNAMIC_ARCH": [True, False],
               "DYNAMIC_OLDER": [True, False],
               "BUILD_WITHOUT_LAPACK": [True, False],
               "BUILD_RELAPACK": [True, False],
               "USE_THREAD": [True, False]
    }
    default_options = {
        "shared": False,
        "DYNAMIC_ARCH": False,
        "DYNAMIC_OLDER": False,
        "BUILD_WITHOUT_LAPACK": False,
        "BUILD_RELAPACK": False,
        "USE_THREAD": False
    }
    generators = "cmake"

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("cmake_installer/3.11.3@conan/stable")
            self.build_requires("strawberryperl/5.26.0@conan/stable")

    def system_requirements(self):
        if tools.os_info.is_linux:
            installer = tools.SystemPackageTool()
            if tools.os_info.linux_distro == "arch":
                installer.install("gcc-fortran")
            else:
                installer.install("gfortran")
        if tools.os_info.is_macos:
            installer = tools.SystemPackageTool()
            installer.install("gcc", update=True, force=True)

    def configure(self):
        # Openblas does not use C++
        del self.settings.compiler.libcxx

    def source(self):
        openblas_git = tools.Git(folder="openblas")
        openblas_git.clone(url="https://github.com/xianyi/OpenBLAS.git",
                           branch="v{0}".format(self.version))

        tools.replace_in_file(
            "openblas/CMakeLists.txt", "project(OpenBLAS C ASM)",
            '''project(OpenBLAS C ASM)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Verify if ccache exists, if yes, then use it to speedup the compilation
find_program(CCACHE_FOUND ccache)
if(CCACHE_FOUND)
    set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE ccache)
    set_property(GLOBAL PROPERTY RULE_LAUNCH_LINK ccache)
endif(CCACHE_FOUND)''')

    def build(self):
        cmake = CMake(self)
        os.mkdir("build")
        shutil.move("conanbuildinfo.cmake", "build/")

        cmake.definitions["DYNAMIC_ARCH"] = self.options.DYNAMIC_ARCH
        cmake.definitions["DYNAMIC_OLDER"] = self.options.DYNAMIC_OLDER
        cmake.definitions["BUILD_RELAPACK"] = self.options.BUILD_RELAPACK
        cmake.definitions["BUILD_WITHOUT_LAPACK"] = self.options.BUILD_WITHOUT_LAPACK
        cmake.definitions["USE_THREAD"] = self.options.USE_THREAD

        if self.settings.os == "Windows":
            cmake.definitions["NO_LAPACK"] = True # No fortran compiler

        if self.settings.compiler == "Visual Studio":
            cmake.definitions["MSVC_STATIC_CRT"] = "MT" in str(self.settings.compiler.runtime)

        cmake.configure(source_folder="openblas", build_folder="build")
        cmake.build()
        cmake.install()

    def package_info(self):
        # By default conan has the 'lib' folder in self.cpp_info.libdirs
        # In case cmake.install in the build step generated a lib64 folder
        # instead of lib, we move it to lib
        try:
            shutil.move("lib64", "lib")
        except Exception:
            pass

        self.cpp_info.includedirs = ["include/openblas"]

        # The openblas library has different names depending if it is a release
        # of a debug build
        if self.settings.build_type == "Debug" and self.options.shared:
            # The name is different only for Debug build with shared libraries
            self.cpp_info.libs = ["openblas_d"]
        else:
            self.cpp_info.libs = ["openblas"]

        # In case of static library we need to also link with pthread
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
