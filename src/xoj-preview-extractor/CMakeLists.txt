## novaboard-thumbnailer executable ##

if (WIN32)
  # Windows does not support the thumbnailer like this
  return ()
endif ()

add_definitions (-DBUILD_THUMBNAILER)

if (DEV_ENABLE_GCOV)
  add_compile_options("--coverage")
  add_link_options("--coverage")
endif (DEV_ENABLE_GCOV)

add_executable (novaboard-thumbnailer
        novaboard-thumbnailer.cpp
        "${PROJECT_SOURCE_DIR}/src/util/GzUtil.cpp"
        "${PROJECT_SOURCE_DIR}/src/util/PlaceholderString.cpp"
        "${PROJECT_SOURCE_DIR}/src/util/StringUtils.cpp"
        "${PROJECT_SOURCE_DIR}/src/util/PathUtil.cpp"
        "${PROJECT_SOURCE_DIR}/src/util/Stacktrace.cpp"
        "${PROJECT_SOURCE_DIR}/src/util/XojPreviewExtractor.cpp"
        )

target_compile_features (novaboard-thumbnailer PRIVATE cxx_std_20)
target_link_libraries (novaboard-thumbnailer
  util
  ${ZLIB_LIBRARIES}
  ${librsvg_LDFLAGS}
  ${Glib_LDFLAGS}
  ${ZIP_LDFLAGS}
  )

target_include_directories (novaboard-thumbnailer PRIVATE ${librsvg_INCLUDE_DIRS})

set (THUMBNAILER_BIN "novaboard-thumbnailer")

add_custom_command (TARGET novaboard-thumbnailer POST_BUILD
  COMMAND ${CMAKE_STRIP} ${THUMBNAILER_BIN}
)

## Install ##

install (TARGETS novaboard-thumbnailer
  RUNTIME DESTINATION bin
  COMPONENT novaboard-thumbnailer
)

## Desktop install targets ##

configure_file (xournalpp-thumbnailer-xoj.schemas xournalpp-thumbnailer-xoj.schemas COPYONLY)

add_custom_target (desktop-install-thumbnailer
  COMMAND "${PROJECT_SOURCE_DIR}/src/xoj-preview-extractor/desktop-install.sh" install

  COMMENT "Install novaboard-thumbnailer as xoj file thumbnail generator"
  SOURCES novaboard-thumbnailer.cpp xournalpp-thumbnailer-xoj.schemas desktop-install.sh
)

add_custom_target (desktop-uninstall-thumbnailer
  COMMAND "${PROJECT_SOURCE_DIR}/src/xoj-preview-extractor/desktop-install.sh" uninstall

  COMMENT "Uninstall novaboard-thumbnailer as xoj file thumbnail generator"
  SOURCES novaboard-thumbnailer.cpp xournalpp-thumbnailer-xoj.schemas desktop-install.sh
)
