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
    options = {"shared": [True, False], "fPIC": [True, False], "ssl": [True, False], "mysql": [True, False], "postgresql": [True, False], "emx": [True, False]}
    default_options = {"shared": False, "fPIC": True, "ssl": True, "mysql": False, "postgresql": False, "emx": False}
    generators = "cmake"
    exports_sources = "CMakeLists.txt"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        if self.options.ssl:
            self.requires("openssl/1.0.2u")
        if self.options.mysql:
            self.requires("libmysqlclient/8.0.17")
        if self.options.postgresql:
            self.requires("libpq/11.5")

    def source(self):
        sha256 = "1c4322a68704526ca3d1f213e7b0dcd30e067a8815be2a79b2ab1197ef70dcf7"
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)


    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["HAVE_SSL"] = self.options.ssl
        cmake.definitions["HAVE_MYSQL"] = self.options.mysql
        cmake.definitions["HAVE_POSTGRESQL"] = self.options.postgresql
        cmake.definitions["HAVE_EMX"] = self.options
        cmake.configure(build_folder=self._build_subfolder, source_folder=self._source_subfolder)
        return cmake

    def _patch(self):
        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"), "add_subdirectory(test)", "")
        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"), "add_subdirectory(examples)", "")
        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"), 'message("-- Project name ${CMAKE_PROJECT_NAME}")', """
message("-- Project name ${CMAKE_PROJECT_NAME}")
include("${CMAKE_SOURCE_DIR}/../conanbuildinfo.cmake")
conan_basic_setup()
""")

    def build(self):
        self._patch()
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.append("pthread")