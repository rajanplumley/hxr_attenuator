#!/reg/g/pcds/package/epics/3.14/ioc/common/pvNotepad/R1.3.1/bin/rhel7-x86_64/pvNotepad

epicsEnvSet( "EPICS_NAME", "IOC:LFE:AT2L0" )
epicsEnvSet( "ENGINEER",  "Rajan Plumley (rajan-01)" )
epicsEnvSet( "LOCATION",  "SLAC:LCLS:FEE:LFE" )
epicsEnvSet( "IOCSH_PS1", "ioc-lfe-at2l0> ")

< envPaths

# Run common startup commands for linux soft IOC's
< /reg/d/iocCommon/All/pre_linux.cmd

# Register all support components
dbLoadDatabase("$(TOP)/dbd/pvNotepad.dbd")
pvNotepad_registerRecordDeviceDriver(pdbbase)

# Load record instances
dbLoadRecords("$(TOP)/db/iocSoft.db",            "IOC=$(EPICS_NAME)" )
dbLoadRecords("$(TOP)/db/save_restoreStatus.db", "IOC=$(EPICS_NAME)" )

#Standard array option

dbLoadRecords("$(TOP)/db/specials.db",     "PV=LCLS:HXR:BEAM:EV,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:01:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:02:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:03:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:04:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:05:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:06:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:07:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:08:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:09:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:10:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:11:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:12:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:13:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:14:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:15:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:16:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:17:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:18:THICKNESS,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:01:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:02:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:03:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:04:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:05:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:06:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:07:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:08:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:09:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:10:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:11:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:12:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:13:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:14:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:15:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:16:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:17:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:18:MATERIAL,RECTYPE=stringin")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:01:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:02:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:03:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:04:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:05:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:06:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:07:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:08:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:09:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:10:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:11:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:12:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:13:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:14:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:15:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:16:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:17:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:FILTER:18:IS_STUCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:SYS:T_ACTUAL,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:SYS:T_HIGH,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:SYS:T_LOW,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:SYS:T_DESIRED,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:SYS:T_3OMEGA,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:SYS:ENERGY,RECTYPE=ao")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:SYS:LOCKED,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:SYS:UNLOCK,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:SYS:MOVING,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:SYS:RUN,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:SYS:SET_MODE,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:SYS:MIRROR_IN,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:SYS:CONFIG,RECTYPE=,NELM=18,FTYPE=ENUM")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:01:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:02:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:03:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:04:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:05:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:06:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:07:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:08:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:09:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:10:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:11:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:12:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:13:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:14:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:15:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:16:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:17:GET_RBV,RECTYPE=bo")
dbLoadRecords("$(TOP)/db/specials.db",     "PV=AT2L0:XTES:MMS:18:GET_RBV,RECTYPE=bo")

# Setup autosave
save_restoreSet_status_prefix("$(EPICS_NAME):" )
save_restoreSet_IncompleteSetsOk( 1 )
save_restoreSet_DatedBackupFiles( 1 )

set_requestfile_path( "$(PWD)/../../autosave"             )
set_savefile_path   ( "$(IOC_DATA)/ioc-lfe-at2l0/autosave" )

set_pass0_restoreFile( "ioc-lfe-at2l0.sav" )        #just restore the settings
set_pass1_restoreFile( "ioc-lfe-at2l0.sav" )        #just restore the settings


# Initialize the IOC and start processing records
iocInit()

# Start autosave backups
create_monitor_set( "ioc-lfe-at2l0.req", 30, "" )

# All IOCs should dump some common info after initial startup.
< /reg/d/iocCommon/All/post_linux.cmd

