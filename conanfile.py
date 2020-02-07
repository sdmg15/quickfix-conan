import os
from conans import ConanFile, CMake, tools

class TrantorConan(ConanFile):
    name = "quickfix"
    version = "1.15.1"
    license = "MIT"
    author = "Quickfix"
    url = "https://github.com/sdmg15/quickfix-conan"
    homepage = "https://github.com/quickfix/quickfix"
    description = "QuickFIX C++ Fix Engine Library"
    topics = ("HFT", "FIX", "Engine")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"
    exports_sources = "CMakeLists.txt"

    requires = (
        "openssl/1.0.2t",
    )

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        sha256 = "1c4322a68704526ca3d1f213e7b0dcd30e067a8815be2a79b2ab1197ef70dcf7"
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)


    def _configure_cmake(self):
        cmake = CMake(self)
        # cmake.definitions["CMAKE_MODULE_PATH"] = ""
        # cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = os.path.join(self._build_subfolder, "conan_paths.cmake")
        # cmake.definitions["BUILD_CTL"] = False
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def _patch(self):
        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"), "include(QuickfixPlatformSettings)", "include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/QuickfixPlatformSettings.cmake)")
        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"), "include(QuickfixPrebuildSetup)", "include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/QuickfixPrebuildSetup.cmake)")
        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"), "include(FindSharedPtr)", "include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/FindSharedPtr.cmake)")
        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"), "include(FindUniquePtr)", "include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/FindUniquePtr.cmake)")
        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"), "add_subdirectory(UnitTest++)", "") 
        tools.replace_in_file(os.path.join(self._source_subfolder, "src/C++/double-conversion/diy-fp.cc"), '#include "double-conversion/diy-fp.h"', '#include "diy-fp.h"') 
        tools.replace_in_file(os.path.join(self._source_subfolder, "src/C++/double-conversion/diy-fp.h"), '#include "double-conversion/utils.h"', '#include "utils.h"') 
        
        
    def build(self):
       # self._patch()
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")