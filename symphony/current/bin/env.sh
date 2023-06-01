#!/bin/sh

ITG_HOME=/opt/fedex/itg
LOG_LOC=$ITG_HOME/server/kintana/log
JAVA=/opt/java/hotspot/8/64_bit/jdk1.8.0_261/java
SYM_LIB=$ITG_HOME/lib/jms

export CLASSPATH=\
$SYM_LIB/jms.jar:\
$SYM_LIB/fedexjms.jar:\
$SYM_LIB/slf4j-simple-1.4.2.jar:\
$SYM_LIB/slf4j-api-1.4.2.jar:\
$SYM_LIB/tibjms.jar:\
$SYM_LIB/xbean.jar:\
$SYM_LIB/Schemas.jar:\
$SYM_LIB/symphony16.jar:\
$SYM_LIB/oracle_jdbc.jar:\
$SYM_LIB/dynachainproxy.jar:\
$SYM_LIB/sf_soap44_sdk.jar:\
$SYM_LIB/jaxrpc.jar:\
$SYM_LIB/axis.jar:\
$SYM_LIB/activation.jar:\
$SYM_LIB/commons-logging.jar:\
$SYM_LIB/commons-discovery.jar:\
$SYM_LIB/saaj.jar:\
$SYM_LIB/log4j.jar:\
$SYM_LIB/mail.jar:\
$ITG_HOME/server/kintana/deploy/itg.war/WEB-INF/classes:\
$SYM_LIB/xmlbeans.jar:
