cmake_minimum_required(VERSION 3.12)
cmake_policy(VERSION 3.12)

file(GLOB_RECURSE novaboard_sources *.cpp *.h)

if (NOT ENABLE_AUDIO)
    list(FILTER novaboard_sources EXCLUDE REGEX "${PROJECT_SOURCE_DIR}/src/core/audio/.*" )
    list(FILTER novaboard_sources EXCLUDE REGEX "${PROJECT_SOURCE_DIR}/src/core/control/AudioController.cpp" )
endif ()
set(novaboard_include_dirs "${CMAKE_CURRENT_SOURCE_DIR}")

add_library(novaboard-core STATIC ${novaboard_sources})
target_compile_features(novaboard-core PUBLIC ${PROJECT_CXX_FEATURES})
target_compile_features(novaboard-core PUBLIC cxx_std_20)
target_link_libraries(novaboard-core
        PRIVATE xoj::util ${novaboard_LDFLAGS}
        PUBLIC xoj::external_modules
        )

if (ENABLE_AUDIO)
    target_include_directories(novaboard-core PUBLIC ${ExternalAudioModules_INCLUDE_DIRS})
    target_link_directories(novaboard-core PUBLIC ${ExternalAudioModules_LIBRARY_DIRS})
    set(AUDIO_LIBS ${ExternalAudioModules_LIBRARIES})
    if (APPLE)
        list(FILTER AUDIO_LIBS EXCLUDE REGEX "^(CoreAudio|AudioToolbox|AudioUnit|CoreFoundation|CoreServices)$")
        target_link_libraries(novaboard-core PUBLIC ${AUDIO_LIBS})
        target_link_libraries(novaboard-core PUBLIC "-framework CoreAudio" "-framework AudioToolbox" "-framework AudioUnit" "-framework CoreFoundation" "-framework CoreServices")
    else()
        target_link_libraries(novaboard-core PUBLIC ${AUDIO_LIBS})
    endif()
endif ()
target_include_directories(novaboard-core PUBLIC ${novaboard_include_dirs})
add_library(xoj::core ALIAS novaboard-core)
