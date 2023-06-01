#!/bin/bash
export TNS_ADMIN=/opt/fedex/symphony/tns_admin
export PATH="/opt/oracle/product/12.1.0.2_64/bin:$PATH"
export ORACLE_HOME=/opt/oracle/product/12.1.0.2_64

echo $PATH
echo $ORACLE_HOME
echo $TNS_ADMIN
echo ~

tnsping ITEG_ARCH_PRD
