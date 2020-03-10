# Makefile to install the st.cmd into the correctly location.
# Author: Jason Tiller

TOP = ../..
-include ./IOC_APPL_TOP
ifneq (,$(IOC_APPL_TOP))
TOP = $(IOC_APPL_TOP)
endif

include $(TOP)/configure/CONFIG
ifndef ARCH
ARCH = linux-x86_64
endif

INSTALL_LOCATION = ../..
INSTALL_LOCATION_BIN = $(TOP)/bin

TARGETS = envPaths

# Make sure these archive files are fully expanded
USR_ARCHIVEFLAGS += -V

ARCHIVE += ioc-lfe-at2l0.archive
REQ += ioc-lfe-at2l0.req

include $(TOP)/configure/RULES.ioc
-include $(TOP)/configure/RULES.archive
-include $(TOP)/configure/RULES.autosave
