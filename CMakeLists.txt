project(gentoo-koam)

find_package(KDE4 REQUIRED)

include(KDE4Defaults)

install(DIRECTORY gentoo-koam/
        DESTINATION ${DATA_INSTALL_DIR}/plasma/plasmoids/gentoo-koam)

install(FILES gentoo-koam/metadata.desktop
        DESTINATION ${SERVICES_INSTALL_DIR} RENAME plasma-applet-gentoo-koam.desktop)
