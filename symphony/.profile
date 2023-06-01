# $Id: dot_profile,v 1.1 2019/01/05 20:05:01 root Exp $
# $Source: /project/EIS/MKACCT/current/lib/dot_profile,v $
#
# default mkacct .profile

umask 022
stty erase  intr  kill 

for dir in \
	/usr/local/bin /usr/local/sbin /usr/local/etc \
	/usr/sbin /usr/bin \
	/sbin /bin \
	/usr/local/X11R6/bin /usr/X11R6/bin /use/openwin/bin \
	/usr/openwin/bin /usr/ucb /usr/ccs/bin \
	/opt/sfw/bin \
	/opt/fedex/mkacct/bin \
	/opt/VRTS/bin \
	/usr/symcli/bin \
	/opt/compaq/hpacucli/bld \
	$HOME/bin
do
	[ -d $dir ] || continue
	case "$PATH" in
	$dir)		: ;;
	*:$dir)		: ;;
	$dir:*)		: ;;
	*:$dir:*)	: ;;
	*)		PATH="$PATH:$dir" ;;
	esac
done
export PATH

SHELLTYPE="${SHELL##*/}"
if [ "bash" = "$SHELLTYPE" ]
then
	[ -f "${HOME}/.bashrc" ] &&
	. "${HOME}/.bashrc"
else
	if [ -f "$HOME/.shrc" ]
	then
		ENV='${HOME}'/.shrc
		export ENV
	fi
	HISTFILE=~/.history
	export HISTFILE
fi
