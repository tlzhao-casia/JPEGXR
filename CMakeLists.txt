cmake_minimum_required(VERSION 3.17)

project(jxrlib VERSION 1.0.0)

set(CMAKE_C_STANDARD 11)

set(DIR_SRC ${CMAKE_CURRENT_LIST_DIR})
set(DIR_SYS image/sys)
set(DIR_DEC image/decode)
set(DIR_ENC image/encode)

set(DIR_GLUE jxrgluelib)
set(DIR_TEST jxrtestlib)
set(DIR_EXEC jxrencoderdecoder)

include_directories(common/include
                    .
                    ${DIR_SYS}
)

add_definitions(-D__ANSI__ -DDISABLE_PERF_MEASUREMENT)

link_libraries(m)

add_compile_options(-w)

if (NOT ${CMAKE_BUILD_TYPE} STREQUAL Release)
    add_compile_options(-O0)
else()
    add_compile_options(-Ofast -DNDEBUG)
endif()

macro (patsubst var dir values)
    foreach(v ${${values}})
        list(APPEND ${var} ${dir}/${v})
    endforeach()
endmacro()

set(_SRC_SYS
    adapthuff.c
    image.c
    strcodec.c
    strPredQuant.c
    strTransform.c
    perfTimerANSI.c
)
patsubst(SRC_SYS ${DIR_SRC}/${DIR_SYS} _SRC_SYS)

set(_SRC_DEC
    decode.c
    postprocess.c
    segdec.c
    strdec.c
    strInvTransform.c
    strPredQuantDec.c
    JXRTranscode.c
)
patsubst(SRC_DEC ${DIR_SRC}/${DIR_DEC} _SRC_DEC)

set(_SRC_ENC
    encode.c
    segenc.c
    strenc.c
    strFwdTransform.c
    strPredQuantEnc.c
)
patsubst(SRC_ENC ${DIR_SRC}/${DIR_ENC} _SRC_ENC)

add_library(jpegxr ${SRC_SYS} ${SRC_DEC} ${SRC_ENC})

# Glue files
set(_GLUE_SRC
    JXRGlue.c
    JXRMeta.c
    JXRGluePFC.c
    JXRGlueJxr.c
)
patsubst(GLUE_SRC ${DIR_SRC}/${DIR_GLUE} _GLUE_SRC)

# Test files
set(_TEST_SRC
    JXRTest.c
    JXRTestBmp.c
    JXRTestHdr.c
    JXRTestPnm.c
    JXRTestTif.c
    JXRTestYUV.c
)
patsubst(TEST_SRC ${DIR_SRC}/${DIR_TEST} _TEST_SRC)

add_library(jxrglue ${GLUE_SRC} ${TEST_SRC})
target_include_directories(jxrglue PUBLIC ${DIR_SRC}/${DIR_GLUE} ${DIR_SRC}/${DIR_TEST})


# App files
macro(add_app app)
    add_executable(${app} ${DIR_SRC}/${DIR_EXEC}/${app}.c)
    target_link_libraries(${app} PUBLIC jpegxr jxrglue)
endmacro()

add_app(JxrEncApp)
add_app(JxrDecApp)
