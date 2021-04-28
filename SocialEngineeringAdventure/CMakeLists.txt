# Copyright: (C) 2019 RBCS Robotics Brain and Cognitive Science
# Authors: Dario Pasquali
# CopyPolicy: Released under the terms of the GNU GPL v2.0.

cmake_minimum_required(VERSION 2.8)
set(CMAKE_LEGACY_CYGWIN_WIN32 0)


SET(KEYWORD "SocialEngineeringAdventure")
PROJECT(${KEYWORD})
set(CMAKE_CXX_STANDARD 11)

FIND_PACKAGE(YARP REQUIRED)
FIND_PACKAGE(ICUBcontrib REQUIRED)

list(APPEND CMAKE_MODULE_PATH ${ICUBCONTRIB_MODULE_PATH})

#search for includes
INCLUDE_DIRECTORIES(
        ${PROJECT_SOURCE_DIR}/include
        ${YARP_INCLUDE_DIRS}
)

set(CMAKE_MODULE_PATH
        ${CMAKE_MODULE_PATH}
        ${YARP_MODULE_PATH}
        ${ICUB_MODULE_PATH}
        ${ICUBCONTRIB_MODULE_PATH} # note 10/10/13 aligned to the standard Rea
        )

list(APPEND CMAKE_MODULE_PATH ${ICUBCONTRIB_MODULE_PATH})
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
add_definitions(${YARP_DEFINES})
include(YarpInstallationHelpers)

set(ICUB_APPLICATIONS_PREFIX "$ENV{ICUB_ROOT}" CACHE PATH "Application path prefix")


#add_subdirectory(src)
add_subdirectory(app)
add_subdirectory(python-scripts)
