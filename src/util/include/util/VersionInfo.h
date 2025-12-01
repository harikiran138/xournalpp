/*
 * Novaboard
 *
 * get version info on various components and libraries
 *
 * @author Novaboard Team
 * https://github.com/novaboard/novaboard
 *
 * @license GNU GPLv2 or later
 */
#pragma once

#include <string>

namespace xoj::util {
/// Get the running GDK backend (or nullptr if none)
const char* getGdkBackend();

/// Get a string "Novaboard a.b.c + commit info"
std::string getNovaboardVersion();

/// Get a string describing the OS
std::string getOsInfo();

/// Get a paragraph with all version info
std::string getVersionInfo();
};  // namespace xoj::util
