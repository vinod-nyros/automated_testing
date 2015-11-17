# ZShell - (c) 2001 Jerome Alet
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#
# author: Jerome Alet - <alet@unice.fr>
#
# This is the Zope shell, an attempt at making the most common
# Unix shell commands available from within Zope.
#
# Feel free to send me any feedback about this software at: alet@unice.fr
#
# $Id: zshell.py,v 1.105 2001/08/30 13:17:04 jerome Exp $
#
# $Log: zshell.py,v $
# Revision 1.105  2001/08/30 13:17:04  jerome
# Command zope was added.
#
# Revision 1.104  2001/08/30 12:47:01  jerome
# Command exec was added
#
# Revision 1.103  2001/08/30 12:08:12  jerome
# Commands dbname, dbsize and uptime were added.
#
# Revision 1.102  2001/08/29 14:51:00  jerome
# setprop and addprop now use a cleaner syntax: --name, and --value (and --type for addprop).
# setprop and addprop now set non-string values (more) correctly.
#
# Revision 1.101  2001/07/06 16:25:14  jerome
# Added a suggestion from Jean Jordaan
#
# Revision 1.100  2001/07/06 16:02:42  jerome
# commands textarea wrapping mode changed to 'virtual' because of a reported
# bug with very long lines in 'physical' mode. Thanks to Holger Lehmann.
#
# Revision 1.99	 2001/06/22 21:54:45  jerome
# CVS conflict in CVS Log message
#
# Revision 1.98	 2001/06/13 14:36:01  jerome
# Version number changed to 1.3
# Andy McKay added to CREDITS file
#
# Revision 1.97	 2001/06/13 14:30:16  jerome
# man plain text output corrected: it contained HTML tags
# merged Andy McKay's patch for ZShellCLI
#
# Revision 1.95	 2001/06/02 22:31:53  jerome
# grep now accepts --owner, --mmin, --mtime, and --newer options
# Both find and grep now accept a --older option
# Overflow error fixed in descend()
#
# Revision 1.94	 2001/06/02 16:53:57  jerome
# Correction in match_Owner(): When no --owner option is given, objects now
# always match, which is prefectly correct, contrary to the previous behavior.
# There's still a difference in the recursive behavior of grep and find, find is
# OK, grep is not. Don't know why yet.
#
# Revision 1.93	 2001/06/02 11:16:04  jerome
# Modification for correct recursion liomit with maxdepth
#
# Revision 1.92	 2001/05/31 19:32:24  jerome
# grep now accepts a --maxdepth option when --recurse is used
#
# Revision 1.91	 2001/05/31 18:12:17  jerome
# cp/mv/cut/copy on inexistant objects doesn't raise a Zope Error anymore.
# cp/mv/paste now display more informations.
# history now accepts a --clear option to empty the .zshell_history
# DTML Document.
# history accepts multiple --user arguments to list only
# those commands run by the specified users (NOTarguments are
# allowed too).
# To modify the history document, the user needs the 'Change DTML Documents'
# permissions, he doesn't need a Manager role anymore.
#
# Revision 1.90	 2001/05/30 22:18:04  jerome
# First shot at NOTarguments. Seem to work fine.
#
# Revision 1.89	 2001/05/30 21:26:07  jerome
# Version number changed to 1.2
# Big reorganisation in command line option handling:
# we can now choose options which may be specified multiple times
# or only a single time on a particular command line:
# Some options may now be specified multiple times, and
# option arguments may use wildcards too: --type, --id, --owner, more to come.
# find's --user option was renamed to --owner
# find's --name option was renamed to --id
# ZClasses' meta_type attribute is callable, this may have raised errors
# because I didn't tested this. It is now fixed.
#
# Revision 1.88	 2001/05/28 19:21:01  jerome
# Corrected export
#
# Revision 1.87	 2001/05/25 22:00:49  jerome
# An invalid regular expression in grep doesn't cause
# a Zope Error anymore.
# adduser was renamed to addusers since it accepts multiple
# arguments.
# deluser was renamed to delusers since it accepts multiple
# arguments
# takeown now accepts --recurse instead of -R to ask for a
# recursive action.
#
# Revision 1.86	 2001/05/25 14:59:10  jerome
# Forgotten a comment to disable the test for permissions
#
# Revision 1.85	 2001/05/25 09:48:01  jerome
# setperms now works.
# locate deleted until I know enough about ZCatalog searching
# Version number changed to 1.0 !
#
# Revision 1.84	 2001/05/25 08:55:01  jerome
# The lsperms command was added.
# The lsusers command's output is now easier to read.
#
# Revision 1.83	 2001/05/25 07:06:35  jerome
# The .zshell_history DTML Document is automatically emptied if it
# still contains the default DTML Document's content.
#
# Revision 1.82	 2001/05/25 06:48:25  jerome
# More complete history command.
#
# Revision 1.81	 2001/05/24 21:38:44  jerome
# The history command now works.
#
# Revision 1.80	 2001/05/24 20:18:04  jerome
# Don't know !
#
# Revision 1.79	 2001/05/24 19:36:24  jerome
# Documentation changes wrt the GNU GPL.
#
# Revision 1.78	 2001/05/24 15:09:46  jerome
# Version number changed to 1.0pre4
#
# Revision 1.77	 2001/05/24 13:51:40  jerome
# Command dump added
#
# Revision 1.76	 2001/05/24 13:22:34  jerome
# DocStrings fixes with the help of Jason Cunliffe.
#
# Revision 1.75	 2001/05/24 11:16:32  jerome
# suckfs will not exist because wget now can do that, and more...
# Added some urls to the GNU GPL FAQ, backing my position.
# DocStrings fixes.
# ShellExpand now can expand from the filesystem too, but defaults
# to from ZODB.
#
# Revision 1.74	 2001/05/23 14:16:01  jerome
# Modification time format in ls output is shorter now
#
# Revision 1.73	 2001/05/23 13:52:15  jerome
# Version number changed to 1.0pre3
# manage, view and properties now work fine.
#
# Revision 1.72	 2001/05/23 12:28:22  jerome
# The nipltd command works
# The shell wildcards expansion mechanism is now thread safe, thanks to Toby Dickenson
# (the code is there for a long time (2 days), but this info was forgotten when
# committing in CVS.
#
# Revision 1.71	 2001/05/22 22:32:03  jerome
# Command export added.
#
# Revision 1.70	 2001/05/22 08:17:33  jerome
# The su command was added and works
#
# Revision 1.69	 2001/05/21 14:42:01  jerome
# Version number changed to 1.0pre2
# Some preliminary code put inside comments in run_su
#
# Revision 1.68	 2001/05/21 10:56:50  jerome
# DocStrings fixes
#
# Revision 1.67	 2001/05/21 10:37:44  jerome
# Version number changed to 1.0pre1 for publication
#
# Revision 1.66	 2001/05/20 13:09:38  jerome
# There's now a single method to retrieve objects' paths, so if it
# is still incorrect it will be easily fixable.
#
# Revision 1.65	 2001/05/20 08:25:59  jerome
# Urls in ls now work with SiteRoots and Apache ProxyPass/ProxyReverse
#
# Revision 1.64	 2001/05/19 08:33:10  jerome
# TODO file added to repository.
# The cd command now displays the current directory correctly
# when an error occurs.
# Security checks are now done for all commands.
# DocStrings fixes.
#
# Revision 1.63	 2001/05/18 18:16:03  jerome
# The roles command now works.
# The lrole command was renamed to lroles to be more
# consistent with the roles command.
# The lsusers command now lists both roles and local roles.
# The lsuser command was renamed to lsusers to be more
# consistent with the rest.
#
# Revision 1.62	 2001/05/18 15:40:18  jerome
# The domains command now works
# The roles command now sort-of works
#
# Revision 1.61	 2001/05/18 07:39:08  jerome
# Unexpanded quoted arguments are now unquoted before running the commands
#
# Revision 1.60	 2001/05/17 21:30:41  jerome
# Command passwd now works.
#
# Revision 1.59	 2001/05/17 20:48:26  jerome
# The wget command works again and saves retrived objects under their original
# id if possible.
#
# Revision 1.58	 2001/05/17 20:09:00  jerome
# The command line analyze now takes care of more characters: _,()
# The call command works again.
# The call command doesn't use expanded wildcards anymore.
# Added skeletons for: mkobj, lsperms, setperms
#
# Revision 1.57	 2001/05/17 13:29:30  jerome
# Version number changed to 1.0
#
# Revision 1.56	 2001/05/16 09:32:28  jerome
# Added a TODO for manage command
#
# Revision 1.55	 2001/05/16 09:31:07  jerome
# find was going too deep when maxdepth was used.
# finalisation of grep with replacing in PythonScripts as well
#
# Revision 1.54	 2001/05/15 23:57:44  jerome
# Empty line
#
# Revision 1.53	 2001/05/15 23:34:39  jerome
# Command grep added. The replace part needs some fix, and the
# rest need some more testing.
#
# Revision 1.52	 2001/05/15 09:07:57  jerome
# Precisions in NEWS
# A better message when javascript is unavailable
#
# Revision 1.51	 2001/05/14 15:09:12  jerome
# When javascript is disabled then there are links in the results instead of
# new windows openings.
#
# Revision 1.50	 2001/05/14 14:53:55  jerome
# Unused variable in import
# google now opens a new window
#
# Revision 1.49	 2001/05/14 14:47:50  jerome
# Command properties added.
# manage, view and properties now use the same code.
#
# Revision 1.48	 2001/05/14 14:31:50  jerome
# Version changed to 0.9
# Commands view and manage added
#
# Revision 1.47	 2001/05/13 22:46:33  jerome
# Commands lsuser, catalog, uncatalog and find added.
# Bug fixes on permissions.
# Links are now correct in ls output.
# ls output now includes the modification time
# access to objects from their path
# is now done using unrestrictedTraverse
# instead of my stincky previous code.
# Shell expansion is better: single quotes,
# double quotes, now work.
# deluser doesn't expand wildcards anymore.
# docstrings for deluser and adduser modified.
# doctsring for call modified to tell people to
# not use it yet.
# An unknown command is now displayed correctly.
#
# Revision 1.46	 2001/05/13 15:24:18  jerome
# Typo
#
# Revision 1.45	 2001/05/13 08:43:48  jerome
# In run_ls the object url is now relative, because otherwise url
# was very bad.
#
# Revision 1.44	 2001/05/12 19:43:05  jerome
# In whoami the result was already safe html
# Some tris to use restrictedTraverse and/or unrestrictedTraverse, but
# without luck. Some debugging code added.
#
# Revision 1.43	 2001/05/12 18:38:12  jerome
# The toObject method should be OK now, and uses restrictedTraverse,
# which seems to be severely buggy with regard to the handling of a single
# '/' as the path argument.
#
# Revision 1.42	 2001/05/12 09:54:14  jerome
# Added some comments with a code sample on how to use shlex
#
# Revision 1.41	 2001/05/11 21:45:33  jerome
# Commands catalog and uncatalog added.
# Preliminary version of the find command.
# Bug fixes on permissions.
#
# Revision 1.40	 2001/05/11 13:10:45  jerome
# about command output changed
#
# Revision 1.39	 2001/05/11 12:49:48  jerome
# Version changed to 0.7
# Commented out the last bit of "problematic" code in zshell()
# Ready for 0.7
#
# Revision 1.38	 2001/05/10 21:58:40  jerome
# Some code deactivated: still problem it seems (nothing here).
# Some skeletons added: find, locate, suckfs, history, grep, replace,
# domains, roles, passwd
# Command mkuf added.
#
# Revision 1.37	 2001/05/09 23:04:27  jerome
# Version changed to 0.6
# Now delprop, addprop, setprop and lsprop work fine
# Statically set the action modifier of the form to "zshell", hoping
# to solve the problem many have encountered.
#
# Revision 1.36	 2001/05/09 21:34:37  jerome
# Now man, lsprop and ls uses the same method to output their results.
# Bug fixes because of the above.
# Use more Class HTML tag parameter to allow an easily tunnable UI.
#
# Revision 1.35	 2001/05/09 18:04:38  jerome
# prop and ls now uses the same code to output their results
#
# Revision 1.34	 2001/05/09 15:08:34  jerome
# delprop, lsprop added
# some UI changes for better configurability
#
# Revision 1.33	 2001/05/09 12:42:24  jerome
# Some UI changes to make it more easily tunnable: Thanks to Peter Bengtsson.
#
# Revision 1.32	 2001/05/09 12:06:36  jerome
# Version number changed to 0.6beta2
# chown command replaced with takeown, and works, found a bug in AccessControl/Owned.py
# in method changeOwner
#
# Revision 1.31	 2001/05/08 23:32:13  jerome
# Bug fixes + Security checks.
# Some security checks are not done, because don't know on
# which permission to test. Some may still be incomplete if
# more than one permission is needed: needs testing and testers !
#
# Revision 1.30	 2001/05/08 20:59:49  jerome
# Some bugfixes.
# Some comments clarified.
# ShellExpand now redirects all the os module methods which are used by glob.glob
# to our own methods.
# Tests to replace toObject() code with a single call to restrictedTraverse():
# doesn't work in ShellExpand, don't know why... So back to my own code which
# works partially.
#
# Revision 1.29	 2001/05/08 15:56:14  jerome
# Some permission checks: untested
#
# Revision 1.28	 2001/05/08 07:29:40  jerome
# whoami modified following Michel@DC's advice
#
# Revision 1.27	 2001/05/07 23:33:20  jerome
# Version changed to 0.6
# Comments from Michel@DC included or corrections done.
#
# Revision 1.26	 2001/05/07 22:32:10  jerome
# Bad test on folderish objects
#
# Revision 1.25	 2001/05/07 22:20:56  jerome
# Prompt form named to zshellform
#
# Revision 1.24	 2001/05/07 22:18:07  jerome
# Version changed to 0.5
# Commands shutdown and zhelp added
# Shell expansion of wildcards
# Many bugfixes
#
# Revision 1.23	 2001/05/07 16:47:36  jerome
# Bugfixes
#
# Revision 1.22	 2001/05/07 16:37:07  jerome
# Correction on javascript, with the help of Peter Bengtsson
#
# Revision 1.21	 2001/05/07 15:01:39  jerome
# Typos
#
# Revision 1.20	 2001/05/07 14:54:38  jerome
# Modifications for new look and output channels separation
#
# Revision 1.18	 2001/05/07 13:28:05  jerome
# Look changes: looks far better now, IMHO
# Added an option to not run the commands.
#
# Revision 1.17	 2001/05/07 09:38:11  jerome
# Now the final HTML result is created correctly.
# The action field of the prompt is now set correctly to
# the calling url instead of zshell itself.
# Most of the code from the zshell method was moved to
# the class' constructor.
# Some docstrings added.
#
# Revision 1.16	 2001/05/06 22:06:43  jerome
# More methods now use the pseudo IO streams and HTML_document output
# 45 old returns last !
#
# Revision 1.15	 2001/05/06 12:49:10  jerome
# Doesn't work: big changes not finished.
#
# Revision 1.14	 2001/05/06 08:39:39  jerome
# Version number changed to 0.4
# Now needs partially the jaxml module
# Modifications for pseudo stdin, stdout and stderr
#
# Revision 1.13	 2001/05/05 22:53:54  jerome
# NEWS file added
# Command call added
#
# Revision 1.12	 2001/05/05 22:24:19  jerome
# toObject is better now
# save and discard doesn't run properly yet
#
# Revision 1.11	 2001/05/05 21:26:05  jerome
# Preparation for accepting commands as external method's arguments: needs testing.
# Commands enter and leave are OK.
# Commands save and discard don't work because of a stinky toObject method.
#
# Revision 1.10	 2001/05/05 13:34:34  jerome
# Bug corrections wrt acquisition.
# Commands mkver, enter and leave added
# Commands save and discard contents deleted: need some work.
#
# Revision 1.9	2001/05/04 15:05:03  jerome
# Version changed to 0.3
# Some preliminary methods to deal with versions
# Deprecated API replaced
#
# Revision 1.8	2001/05/04 13:48:30  jerome
# Bug corrections
# The wget command seems to work now
#
# Revision 1.7	2001/05/04 12:07:33  jerome
# Version changed to 0.2
# CREDITS file added
# Better handling of acquisition when working with the
# Folder hierarchy.
# Now remembers the current working directory from one "Run!" to the other.
#
# Revision 1.6	2001/05/04 10:51:42  jerome
# Added new methods:
#	deluser, adduser
#	lrole
#	whoami
#	about
#	google
#	wget
#	mkdir
#
# Added the possibility to use zshell.css as a stylesheet
#
# Revision 1.5	2001/05/04 07:29:54  jerome
# Man arguments are now sorted
#
# Revision 1.4	2001/05/04 07:24:29  jerome
# Help for chown added
#
# Revision 1.3	2001/05/04 07:17:32  jerome
# Docstrings added
#
# Revision 1.2	2001/05/04 06:59:08  jerome
# README and COPYING files added
# CVS tags added to zshell.py
#
#

# standard modules
import sys
import os
import string
import re
import urllib
import cStringIO
import posixpath
import shlex
import rexec
import getopt
import fnmatch
import time
import popen2

# jerome's modules
try :
	import jaxml
except ImportError:
	sys.stderr.write("It seems you lack the jaxml python module, download it from:\nhttp://cortex.unice.fr/~jerome/jaxml/\n")
	sys.stderr.flush()
	raise

# Zope modules
import Globals
import AccessControl, AccessControl.SecurityManagement
from OFS.DTMLDocument import DTMLDocument
from OFS.DTMLMethod import DTMLMethod
from OFS.CopySupport import CopyError
from Products.PythonScripts.PythonScript import PythonScript
from DateTime import DateTime
from ZODB import FileStorage

__version__ = "1.3"

__doc__ = """
ZShell is an external Zope method which allows you to manipulate
the ZODB using standard unix shell's commands from within Zope's
Management Interface in your web browser.

All commands do security checks and either work or exit with a
message, depending on your current privileges.

However, you should keep in mind that ZShell is very powerful:
use it carefully, do backups often, and use Zope's Undo facility
when needed.

If the use of ZShell leads to a data loss, your dog being killed, or
your wife/husband going away, then:

		YOU HAVE BEEN WARNED !!!

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
"""                

class ZopeShell :
	# Just to be sure
	__context = None
	__version = None
	__status = None
	__stdin = None
	__stdout = None
	__stderr = None
	__htmlfinal = None
	__temphtml = None
	__olderror = None

	# User Interface:
	__prompt_cols = 50		# prompt columns
	__prompt_rows = 10		# prompt rows
	__prompt_percent = 66		# prompt width in percent
	__available_columns = 3		# number of columns on which to display available commands
	__theadercolor = "gold"		# table header color
	__thead_bgcolor = "#4169e1"	# table headings color
	__trow_evencolor = "white"	# even rows' color
	__trow_oddcolor = "#dedede"	# odd rows' color

	def __init__(self, context, zshellscript = None) :
		# the current working Folder may be stored in
		# an hidden field in the form: check if it is or not
		# and set private context accordingly
		if hasattr(context, "REQUEST") and context.REQUEST.has_key("zshellpwd") :
			pwdobj = self.toObject(context, context.REQUEST["zshellpwd"])
			if pwdobj is not None :
				self.__context = pwdobj
			else :
				self.__context = context
		else :
			self.__context = context

		# get active version, if any
		if self.__context.REQUEST.cookies.has_key(Globals.VersionNameName) :
			self.__version = self.__context.REQUEST.cookies[Globals.VersionNameName]
		else :
			self.__version = None

		# set initial status to None, meaning no running command
		self.__status = None

		# now we open the standard IO channels
		self.__stdin = cStringIO.StringIO()
		self.__stdout = cStringIO.StringIO()
		self.__stderr = cStringIO.StringIO()

		# create an empty HTML document for final result
		self.__htmlfinal = jaxml.HTML_document()

		# create an empty HTML document for commands results
		self.__temphtml = jaxml.HTML_document()

		# put intial content in the html final output
		self.initHTML()

		# get commands either from parameters or from REQUEST
		commands = self.getCommands(zshellscript)

		# we execute commands before displaying the prompt
		# to be able to take care of a change of the current working directory.
		# but we only execute them if zshelldontrun is not in the REQUEST, because
		# this would mean that probably the user just wants the help
		# and the insertion of an empty command in the textarea
		if not self.__context.REQUEST.has_key("zshelldontrun") :
			status = self.execCommands(commands)
		else :
			# only executes the man commands, ignore the rest
			status = self.execCommands(filter(lambda f: f[:4] == "man ", commands))

		# displays the prompt
		self.showPrompt(commands)

	def __del__(self) :
		# try to take care of closing and freeing the IO channels
		if self.__stdin is not None :
			self.__stdin.close()
			del self.__stdin
		if self.__stdout is not None :
			self.__stdout.close()
			del self.__stdout
		if self.__stderr is not None :
			self.__stderr.close()
			del self.__stderr

	def getContext(self) :
		return self.__context

	def get_stdin(self) :
		"""Returns the stdin stream's contents"""
		if self.__stdin is not None :
			# probably no flush
			return self.__stdin.getvalue()

	def get_stdout(self) :
		"""Returns the stdout stream's contents"""
		if self.__stdout is not None :
			self.__stdout.flush()
			return self.__stdout.getvalue()

	def get_stderr(self) :
		"""Returns the stderr stream's contents"""
		if self.__stderr is not None :
			self.__stderr.flush()
			return self.__stderr.getvalue()

	def get_HTML(self) :
		"""Returns the final HTML output"""
		# the final result is composed of two parts: the prompt and the results.
		# we can "pseudo" concatenate them with the jaxml "+" operator:
		if (self.__htmlfinal is not None) and (self.__temphtml is not None):
			self.__htmlfinal = self.__htmlfinal + self.__temphtml
		return str(self.__htmlfinal)

	def getStatus(self) :
		return self.__status

	def initHTML(self) :
		x = self.__htmlfinal
		if x is not None :
			x.html()
			x._push()
			x.head().title("The Zope Shell")
			if hasattr(self.__context, "zshell.css") :
				x._push()
				x.link(rel="stylesheet", type="text/css", href="%s" % self.ObjectPath(getattr(self.__context, "zshell.css")))
				x._pop()
			x.script("function setfocus() { document.zshellform['zshellscript:lines'].focus(); document.zshellform['zshellscript:lines'].select(); }")
			x._pop()
			x.body(bgcolor = "white", onLoad="setfocus()")

	def errormessage(self, msg) :
		"""outputs an error message both to the screen and to the pseudo stderr stream
		   don't output anything if the previous message was the same.
		"""
		if msg != self.__olderror :
			self.__stderr.write("%s\n" % msg)
			self.htmlmessage(msg)
		self.__olderror = msg[:]
		return -1

	def permissionProblem(self, object, perm) :
		msg = "You don't have permission '%s' on"
		path = self.ObjectPath(object)
		if path is not None :
			return self.errormessage((msg + " %s") % (perm, path))
		else :
			return self.errormessage((msg + " object %s") % (perm, repr(object)))

	def roleProblem(self, object, role) :
		msg = "You don't have role '%s' on"
		path = self.ObjectPath(object)
		if path is not None :
			return self.errormessage((msg + " %s") % (role, path))
		else :
			return self.errormessage((msg + " object %s") % (role, repr(object)))

	def htmlstr(self, unsafe) :
		"""Formats a string to be shown safely in HTML"""
		unsafe = string.replace(unsafe, '&', '&amp;')
		unsafe = string.replace(unsafe, '<', '&lt;')
		return string.replace(unsafe, '>', '&gt;')

	def htmlmessage(self, msg, safe = 0, printable = 0) :
		"""prints a message in the html output and optionally in stdout too"""
		if printable :
			self.printf(msg)
		if not safe :
			msg = self.htmlstr(msg)
		self.__temphtml._text("%s" % msg)
		self.__temphtml._br()

	def printf(self, msg) :
		"""outputs a message only in stdout"""
		self.__stdout.write("%s" % msg)

	def newwindow(self, url) :
		self.__temphtml._push()
		self.__temphtml.script("window.open('%s')" % url).noscript().a("Please follow this link to see the result of your command", href="%s" % url)
		self.__temphtml._pop()
		return 0

	def tableDisplay(self, name, labels, table) :
		if table :
			x = self.__temphtml
			x._push()
			x.table(border=1)
			x._push()
			x.tr(bgcolor=self.__theadercolor, Class="%stheader" % name)
			for label in labels :
				x.th(label, Class="%stheaderlabel" % name)
			x._pop()
			curcolor = -1
			for item in table :
				x._push()
				if curcolor < 0 :
					x.tr(bgcolor = self.__trow_oddcolor, Class="%srow" % name)
				else :
					x.tr(bgcolor = self.__trow_evencolor, Class="%srow" % name)
				curcolor = -curcolor
				for key in labels :
					x._push()
					x.td(("%s" % item[key]) or "&nbsp;", Class="%s%s" % (name, key), align="left", valign="top")
					x._pop()
				x._pop()
			x._pop()

	def ShellExpand(self, path, zodb=1) :
		"""Simulates a shell expansion using glob.glob and redirecting some of the os module functions to our own"""
		def mylistdir(path, zopeshell = self) :
			# the original os.listdir accepts only one argument, but we need
			# both the path to scan, and a reference to the current object,
			# so we "cheat" using a default argument which is never used
			# by os.listdir.
			obj = zopeshell.toObject(zopeshell.getContext(), path)
			if (obj is not None) and hasattr(obj, "isPrincipiaFolderish") \
			    and obj.isPrincipiaFolderish and hasattr(obj, "objectIds") :
				if zopeshell.HasPerms(obj, 'Access contents information', verbose = 0) :
					return obj.objectIds()
			return []

		def myexists(path, zopeshell = self) :
			# see above
			return zopeshell.toObject(zopeshell.getContext(), path) is not None

		def myisdir(path, zopeshell = self) :
			# see above
			while path and (path[-1] == '/') :
				path = path[:-1]
			obj = zopeshell.toObject(zopeshell.getContext(), path or '/')
			if (obj is not None) and hasattr(obj, "isPrincipiaFolderish") :
				return obj.isPrincipiaFolderish
			else :
				return 0

		# builds a restricted execution environment.
		# this way we are thread safe. Thanks to Toby Dickenson.
		r_env = rexec.RExec()
		osmodule = r_env.add_module('os')
		for name,value in os.__dict__.items():
		    setattr(osmodule,name,value)
		ospathmodule = r_env.add_module('os.path')
		for name,value in os.path.__dict__.items():
		    setattr(ospathmodule,name,value)

		if zodb :
			# we want to expand wildcards from the ZODB
			# so we plug in our own methods
			osmodule.listdir = mylistdir
			ospathmodule.join = posixpath.join
			ospathmodule.split = posixpath.split
			ospathmodule.exists = myexists
			ospathmodule.isdir = myisdir

		# do globbing using our own methods
		# or the normal ones if zodb==0
		r_env.s_exec('import glob')
		result = r_env.r_eval('glob.glob')(path)
		if not result :
			result = [path] # returns the argument unmodified
		return result

	def ObjectPath(self, object) :
		if hasattr(object, "absolute_url") :
			url = object.absolute_url()
			return '/' + string.join(string.split(url, '/')[3:], '/')

	def getcwd(self):
		return self.ObjectPath(self.__context)

	def toObject(self, curdir, path) :
		# Michel@DC: ouch, it looks like you go about doing your own
		# traversal over Zope objects here, this is bad.
		# because of many layers of history, traversal is a
		# delicate process that you will probably get wrong if
		# you try to do it yourself.  Instead of doing your
		# own traversal, use
		# self.__context.restrictedTraverse() to do the
		# traversal for you (assuming __context is a Zope
		# container) as a bonus, restrictedTraverse will
		# enforce security for you.

		# Jerome: Here's my try, but with unrestrictedTraverse.
		# it seems that restrictedTraverse is a bit, hmmm..., too restricted !
		path = posixpath.normpath(path)
		try :
			if path == '.' :
				return self.__context
			elif path == '..' and hasattr(self.__context,'aq_parent') :
				if hasattr(self.__context, "isTopLevelPrincipiaApplicationObject") and self.__context.isTopLevelPrincipiaApplicationObject :
					return self.__context
				else :
					return self.__context.aq_parent
			else :
				return curdir.unrestrictedTraverse(path)
		except IndexError:
			# BUG in Zope 2.3.2 ! => doesn't take care correctly of the / folder
			# when the path argument contains only '/'
			return curdir.getPhysicalRoot()
		except AttributeError:
			return None	# nothing, e.g. acl_users/*
		except KeyError:
			return None	# empty folder it seems
		except TypeError:
			return None	# What the hell is this ?

	def showPrompt(self, cmds) :
		x = self.__htmlfinal
		x._push()
		x.p()
		if self.__version :
			x._push()
			x.font(color="red").em("You're currently working in version %s" % self.__version)
			x._pop()
			x._br()

		x.table(border=0, width="100%")
		x._push()
		x.tr(bgcolor="silver").th("Enter your commands below:", width="%i%%" % self.__prompt_percent, align="left", valign="middle").th("Available commands:", align="center", valign="middle")
		x._pop()
		x.tr()
		x._push()
		x.td(width="%i%%" % self.__prompt_percent, align="left", valign="top")

		# Maybe the following line was causing problems,
		# so its commented out for now
		# x.form(name="zshellform", action = self.__context.REQUEST.URL0, method="POST")
		# and replaced with this one:
		x.form(name="zshellform", action = "%s" % self.__context.REQUEST.URL0, method="POST")

		x.textarea("%s" % string.join(cmds, '\n'), Class="prompt", rows=self.__prompt_rows, cols=self.__prompt_cols, wrap="virtual", name="zshellscript:lines")
		x._br().em("Use the man command")._br()._submit(name="run", value="Run !")

		# the line below explains why we must first run the commands: we must take
		# care of the eventually new current folder
		x._hidden(name="zshellpwd", value="%s" % self.getcwd())

		x._pop()
		x.td(align="left", valign="top")
		x.font(size="-1")
		x.table(border=0, cellpadding=0, cellspacing=0, width="100%")
		methodslist = map(lambda n: n[4:], filter(lambda f: f[:4] == 'run_', self.__class__.__dict__.keys()))
		methodslist.sort()
		nbmethods = len(methodslist)
		for m in range(0, nbmethods, self.__available_columns) :
			x._push()
			x.tr(Class="availablerow")
			for i in range(self.__available_columns) :
				methodindex = m + i
				if methodindex < nbmethods :
					x._push()
					x.td(Class="availablemethod", align="left", valign="top")
					x.a("%s" % methodslist[methodindex], href="%s?zshellscript=man%%20%s&&zshellscript=%s&zshelldontrun=1" % (self.__context.REQUEST.URL0, methodslist[methodindex], methodslist[methodindex]))._br()
					x._pop()
			x._pop()
		x._pop()

	def getCommands(self, script = None) :
		if script is None :
			# no argument, get them from REQUEST
			if self.__context.REQUEST.has_key("zshellscript") :
				script = self.__context.REQUEST["zshellscript"]
			else :
				script = []
		if type(script) != type([]) :
			script = [script]
		return map(string.strip, filter(None, script))

	def execCommands(self, cmds) :
		x = self.__temphtml
		self.__status = 0
		if cmds :
			x._push()
			x.p().table(width="100%", border=0)
			x._push()
			x.tr(Class="resultstheader").th("Results:", Class="resultstheaderlabel", bgcolor="silver", colspan=2)
			x._pop()
			x.tr(Class="resultsbodyrow").td(Class="resultsbody", align="left", valign="top", colspan=2)
			for command in cmds :
				status = self.execCommand(command)
				if status is not None :
					self.__status = self.__status + status
			if self.__status :
				x._br().b("WARNING: %i errors were encountered" % abs(self.__status))
			x._pop()
		return self.__status

	def execCommand(self, cmdline) :
		# Unfortunately shlex.shlex needs a file object, not a buffer.
		# tokenize the command line
		fcmdline = cStringIO.StringIO("%s" % cmdline)
		tokenizer = shlex.shlex(fcmdline)
		tokenizer.wordchars = tokenizer.wordchars + r".:,?!~/\_$*-+={}[]()"
		tokenizer.quotes = tokenizer.quotes + "`"
		unexpanded = []
		while 1 :
			token = tokenizer.get_token()
			if token :
				unexpanded.append(token)
			else :
				break
		fcmdline.close()
		del tokenizer
		del fcmdline

		# the command is the first element
		cmd = unexpanded[0]
		cmdname = "run_" + cmd
		if not hasattr(self, cmdname) :
			return self.errormessage("Unknown command: %s" % cmd)

		# skip the command
		unexpanded = unexpanded[1:]
		# then build a wildcards expanded list of arguments
		expanded = []
		for i in range(len(unexpanded)) :
			# if quoted, then add it without the quotes
			# and modify the unexpanded arg accordingly
			uarg = unexpanded[i]
			if (uarg[0] == uarg[-1] == "'") \
			   or (uarg[0] == uarg[-1] == '"') :
				expanded.append(uarg[1:-1])
				unexpanded[i] = uarg[1:-1]
			else :
				# if not quoted then try to expand wildcards
				# and add the result
				expanded.extend(self.ShellExpand(uarg) or [uarg])

		# Update the history if available
		self.UpdateHistory(cmdline)

		# then launch the command: we don't do it before updating
		# the history because we would miss shutdowns and restarts
		return getattr(self, cmdname)(expanded, unexpanded)

	def getHistory(self) :
		"""Returns the history document: .zshell_history"""
		if hasattr(self.__context, ".zshell_history") \
		   and (self.getMetaType(getattr(self.__context, ".zshell_history")) == 'DTML Document') :
			return getattr(self.__context, ".zshell_history")

	def UpdateHistory(self, cmdline, clear=0) :
		"""Updates the command history"""
		# we try to find a DTML Document which id is ".zshell_history"
		# and save commands into it.
		# BUT we don't test for permissions to modify it because
		# a Manager may want to keep an history in a place that's usually
		# not writable by anyone.
		# I dont know if this is a good thing or not, maybe time will tell...
		# if there's no history document, then don't do anything.
		history = self.getHistory()
		if history is not None :
			(username, dummy) = self.WhoAmI()
			historyline = "%s,%s,%s" % (DateTime().strftime("%Y-%m-%d %H:%M:%S %Z"), username, cmdline)
			oldsrc = history.document_src()
			if clear :
				if self.HasPerms(history, 'Change DTML Documents') :
					oldsrc = "" # we clear the history, and log the history --clear command
				else :
					# the user doesn't have the correct permissions to clear
					# the history, so his history --clear was already logged:
					# there's no need to log it a second time.
					historyline = ""
			else :
				if oldsrc[0] == '<' :
					# this is probably a non empty .zshell_history DTML Document
					# I mean a DTML Document which was not emptied before being
					# used as the history document, so it still contains the
					# default DTML Document tags: all we have to do is to
					# empty it by ourselves: MAY BE DANGEROUS !
					oldsrc = ""
				else :
					oldsrc = oldsrc[:-1]	# we want to eat the last '\n'
			src = oldsrc + historyline + '\n\n'  # Zope eats the last \n character too
			history.manage_edit(src, history.title)

	def HasPerms(self, object, perms, verbose = 1) :
		"""Checks if the user has all the perms permissions on an object"""
		if type(perms) != type([]) :
			perms = [perms]
		SecurityManager = AccessControl.getSecurityManager()
		for perm in perms :
			if not SecurityManager.checkPermission(perm, object) :
				if verbose :
					self.permissionProblem(object, perm)
				return 0
		return 1

	def HasRoles(self, object, roles, verbose = 1) :
		"""Checks if the user has at least one role in roles in the context of an object"""
		if type(roles) != type([]) :
			roles = [roles]
		ctxtroles = AccessControl.getSecurityManager().getUser().getRolesInContext(object)
		for role in roles :
			if role in ctxtroles :
				return 1
		if verbose :
			self.roleProblem(object, role)
		return 0

	def WhoAmI(self) :
		"""Returns the current user's name"""
		user = AccessControl.getSecurityManager().getUser()
		return (user.getUserName(), user.getRoles())

	def getMetaType(self, object) :
		"""Returns an object's meta type"""
		if callable(object.meta_type) :
			# at least ZClasses
			return object.meta_type()
		else :
			# the rest
			return object.meta_type

	def getArgsAndNot(self, allargs) :
		"""Splits a list of arguments into two sublists:
			- a list of arguments
			- a list of NOTarguments
		   a NOTargument is an argument which begins with '!'
		"""
		args = []
		notargs = []
		for arg in allargs :
			if arg[0] == '!' :
				# add it to the notargs list but we
				# don't want the '!' character
				notargs.append(arg[1:])
			else :
				args.append(arg)
		if notargs and not args :
			# args still empty, we want all of them
			# before matching negatively
			args = ["*"]
		return (args, notargs)

	def descend(self, root, func, maxdepth = 0, curdepth = 0) :
		status = 0
		if root is not None :
			if not self.HasPerms(root, 'View') :
				status = -1
			else :
				status = status + func(root)
				if (not (maxdepth and (curdepth >= maxdepth))) and hasattr(root, "isPrincipiaFolderish") and root.isPrincipiaFolderish :
					curdepth = curdepth + 1
					if not self.HasPerms(root, 'Access contents information') :
						status = status - 1
					for object in root.objectValues() :
						status = status + self.descend(object, func, maxdepth, curdepth)
		return status

	def getopt(self, longs, argv) :
		"""Analyses command line options, only long options are recognized"""
		# analyse the arguments to extract those which may be lists
		# from those which must be single values
		# we put them into lists, since not so many options
		# will generally be used, this should be at least as fast
		# as putting them in mappings
		single = []
		multiple = []
		for l in range(len(longs)) :
			long = longs[l]
			if long[-1] == '+' :
				# this option may be specified multiple times
				# but we must modify it for getopt.getopt to
				# work correctly
				longs[l] = long[:-1] + '='
				multiple.append(long[:-1])
			elif long[-1] == '=' :
				single.append(long[:-1])
			else :
				single.append(long)
		try :
			result = {}
			options,args = getopt.getopt(argv, '', longs)
			if options :
				for (o, v) in options :
					o = o[2:]
					if o in single :
						if not result.has_key(o) :
							result[o] = v
						else :
							raise getopt.error, "Option --%s can't be specified more than one time on this command line" % o
					elif o in multiple :
						if not result.has_key(o) :
							result[o] = []
						result[o].append(v)
					else :
						# there's a very big problem !
						raise getopt.error, "ZShell internal error while parsing command line arguments"
			elif not args :
				args = argv	# no option and no argument, return argv inchanged
			return (result, args)
		except getopt.error, msg :
			self.errormessage("%s" % msg)
			return (None, None)

	def match_anystring(self, option, value, options) :
		if options.has_key(option) :
			if value :
				(vals, notvals) = self.getArgsAndNot(options[option])
				ok = 0
				for val in vals :
					if fnmatch.fnmatchcase(value, val) :
						ok = 1
						break
				oknot = 0
				for notval in notvals :
					if fnmatch.fnmatchcase(value, notval) :
						oknot = 1
						break
				return ok and (not oknot)
			return 0
		return 1

	def match_MetaType(self, object, options) :
		"""Returns 1 if an object meta type matches optional --type options.
		   If no --type option is given, then the object always matches.
		"""
		return self.match_anystring("type", self.getMetaType(object), options)

	def match_Id(self, object, options) :
		"""Returns 1 if an object's id matches optional --id options.
		   If no --id option is given, then the object always matches.
		"""
		return self.match_anystring("id", object.getId(), options)

	def match_Owner(self, object, options) :
		"""Returns 1 if an object's owner matches optional --owner options.
		   If no --owner option is given, then the object always matches.
		"""
		if options.has_key("owner") :
			ownerinfo = object.owner_info()
			if ownerinfo is not None :
				# at least /Control_Panel/Products[/*] doesn't satisfy the following test
				if hasattr(ownerinfo, "has_key") and ownerinfo.has_key('id') :
					return self.match_anystring("owner", ownerinfo['id'], options)
			return 0 # Not owned or no owner: never match
		return 1	 # No owner option: always match

	def match_Newer(self, object, options) :
		"""Returns 1 if an object is newer than an optional --newer option.
		   Returns -1 if the --newer option argument doesn't exist
		   Returns 0 if the object is not newer
		   if modification times are equal then the object matches.
		   If no --newer option is given, then the object always matches.
		"""
		if options.has_key("newer") :
			objnewer = self.toObject(self.__context, options["newer"])
			if objnewer is not None :
				if object.bobobase_modification_time() <= objnewer.bobobase_modification_time() :
					return 0
			else :
				return self.errormessage("Object %s doesn't exist" % options["newer"])
		return 1

	def match_Older(self, object, options) :
		"""Returns 1 if an object is older than an optional --older option.
		   Returns -1 if the --older option argument doesn't exist
		   Returns 0 if the object is not older
		   if modification times are equal then the object matches.
		   If no --older option is given, then the object always matches.
		"""
		if options.has_key("older") :
			objolder = self.toObject(self.__context, options["older"])
			if objolder is not None :
				if object.bobobase_modification_time() >= objolder.bobobase_modification_time() :
					return 0
			else :
				return self.errormessage("Object %s doesn't exist" % options["older"])
		return 1

	def match_Time(self, object, options) :
		"""Returns 1 if an object is newer than an optional --mmin or --mtime option.
		   Returns -1 if the --mmin or --mtime option argument is an invalid value.
		   --mmin expects a duration in minutes.
		   --mtime expects a duration in days.
		   Returns 0 if the object is not newer.
		   If none of --mmin or --mtime option is given, then the object always matches.
		"""
		if options.has_key("mmin") or options.has_key("mtime") :
			if options.has_key("mmin") and options.has_key("mtime") :
				return self.errormessage("Options --mmin and --mtime are incompatible")
			if options.has_key("mmin") :
				timestr = options["mmin"]
			else :
				timestr = options["mtime"]
			try :
				if options.has_key("mmin") :
					modtime = int(timestr) * 60
				else :
					modtime = int(timestr) * 60 * 60 * 24
			except ValueError :
				return self.errormessage("Invalid time %s" % timestr)
			testtime = DateTime(int(time.time()) - modtime)
			if object.bobobase_modification_time() <= testtime :
				return 0
		return 1

	def match_Many(self, object, options) :
		"""Returns 1 if an object matches all criterias.
		   Returns 0 if it doesn't match some of them.
		   Returns -1 if there's an error somewhere.
		"""
		# if id doesn't match then skip
		if not self.match_Id(object, options) :
			return 0

		# if meta type doesn't match then skip
		if not self.match_MetaType(object, options) :
			return 0

		# if owner doesn't match then skip
		if not self.match_Owner(object, options) :
			return 0

		# if not newer than another object then skip
		newer = self.match_Newer(object, options)
		if newer <= 0 :
			return newer

		# if not older than another object then skip
		older = self.match_Older(object, options)
		if older <= 0 :
			return older

		# if modification time doesn't match options
		# --mmin or --mtime then skip
		matchtime = self.match_Time(object, options)
		if matchtime <= 0 :
			return matchtime
		return 1

	def getMaxDepth(self, options, default=0) :
		mx = default
		if options.has_key("maxdepth") :
			try :
				mx = int(options["maxdepth"])
			except ValueError :
				return self.errormessage("the --maxdepth option's argument must be a numeric")
		return mx

	def mv_or_cp(self, cmd, expanded) :
		if len(expanded) < 2 :
			return self.errormessage("Incorrect number of arguments")
		else :
			status = 0
			dst = expanded[-1]
			srcs = expanded[:-1]
			objids = []
			for src in srcs :
				if '/' in src :
					status = status + self.errormessage('Paths in source objects are not allowed at this time: %s' % src)
				else :
					objids.append(src)
			dsto = self.toObject(self.__context, dst)
			if dsto is None :
				return status + self.errormessage("Incorrect destination argument: %s" % dst)
			if not dsto.isPrincipiaFolderish :
				return status + self.errormessage("Not a folderish object: %s" % dst)

			# Michel@DC: here you should do a
			# SecurityManager.checkPermission('View
			# management screens', self.__context) to make
			# sure the user has permission to copy or
			# paste.

			# Jerome: In fact we must test this perm on both
			# the source and the destination.
			if not self.HasPerms(self.__context, 'View management screens') :
				return status - 1
			if not self.HasPerms(dsto, 'View management screens') :
				return status - 1

			# All is fine, do it now.
			try :
				if cmd == 'cp' :
					self._clipboard = self.__context.manage_copyObjects(ids = objids)
					action = 'copied'
				else :
					self._clipboard = self.__context.manage_cutObjects(ids = objids)
					action = 'moved'
				dsto.manage_pasteObjects(cb_copy_data = self._clipboard)
				for oid in objids :
					self.htmlmessage('%s %s to %s' % (oid, action, self.ObjectPath(dsto)))
			except AttributeError, msg:
				status = status + self.errormessage("Object %s doesn't exist" % msg)
			except CopyError :
				status = status + self.errormessage("Objects can't be %s to %s" % (action, self.ObjectPath(dsto)))
			return status

	def manage_view_properties(self, expanded, unexpanded, action, perms = None, roles = None) :
		"""Called by run_manage, run_view and run_properties"""
		if not expanded :
			return self.errormessage("Needs at least one object id")
		status = 0
		for arg in expanded :
			object = self.toObject(self.__context, arg)
			if object is None :
				status = status + self.errormessage('Incorrect path: %s' % arg)
			else :
				if (perms is not None) and not self.HasPerms(object, perms) :
					status = status - 1
				elif (roles is not None) and not self.HasRoles(object, roles) :
					status = status - 1
				else :
					status = status + self.newwindow("%s%s" % (object.absolute_url(), action))
		return status

	def run_exec(self, expanded, unexpanded) :
		"""Executes an external command

		   exec ls -la /

		   Hint: the external command is launched as the user
			 who launched Zope (usually user nobody)

		   Caveats: things like 'telnet' need more work ;-)

		   WARNING: like with the find command, you will become
			    addicted quick.
		"""
		process = popen2.Popen3(string.join(unexpanded, " "), capturestderr=1)
		retcode = process.wait()
		output = process.fromchild.read()
		errors = process.childerr.read()
		if errors :
			# self.errormessage already outputs a final \n
			if errors[-1] == '\n' :
				errors = errors[:-1]
			self.errormessage(errors)
		self.htmlmessage(string.replace(output, '\n', '<BR>'), safe=1, printable=1)
		del process
		if errors :
			return -1

	# Michel@DC: all methods below here need to validate their operations
	# with SecurityManager.checkPermission

	def run_su(self, expanded, unexpanded) :
		"""Run a command as another user

		   Accepts a --user xxxx option
		   and a --password yyyy option.

		   If the current user has a Manager role in the current context,
		   then no password is required, else the correct password for
		   user xxxx must be entered.
		   If there's no --user option, then an su to user 'admin' is tried:

		   su --user jerome --password x./32 "rm /QuickStart"

		   Nota Bene: Both the password and domains must validate for
			      the new user.

		   Caveats: su state is not preserved, it's done voluntarily
			    this way, but just tell me if you prefer another behavior.
		"""
		options, args = self.getopt(["user=", "password="], unexpanded)
		if (options is None) and (args is None) :
			return -1	# message was already displayed in self.getopt()
		if not args :
			return self.errormessage("Needs a command to run as another user")
		# we display the same message in all cases to prevent
		# a brute force attack to learn existing usernames
		incorrect_user_or_password = "You must supply a correct username and password"
		if not self.HasRoles(self.__context, 'Manager', verbose=0) :
			# not an admin, password is required
			if not options.has_key("password") :
				return self.errormessage("%s" % incorrect_user_or_password)
			else :
				password = options["password"]
		else :
			password = None
		if not options.has_key("user") :
			newusername = "admin"
		else :
			newusername = options["user"]

		newuser = self.__context.acl_users.getUser(newusername)
		if (newuser is None) or ((password is not None) and not (newuser.authenticate(password, self.__context.REQUEST))) :
			return self.errormessage("%s" % incorrect_user_or_password)
		olduser = AccessControl.getSecurityManager().getUser()
		oldusername = olduser.getUserName()
		AccessControl.SecurityManagement.newSecurityManager(None, newuser)
		self.htmlmessage("User '%s' does a su to '%s'" % (oldusername, newusername))
		status = self.execCommand(string.join(args, ' '))
		if oldusername == 'Anonymous User' :
			AccessControl.SecurityManagement.noSecurityManager()
		else :
			AccessControl.SecurityManagement.newSecurityManager(None, olduser)
		self.htmlmessage("Current user '%s' was reset to '%s'" % (newusername, oldusername))
		return status

	def run_manage(self, expanded, unexpanded) :
		"""Manages objects

		   Accepts multiple arguments

		   Caveats: Nicer in a browser with JavaScript support
		"""
		return self.manage_view_properties(expanded, unexpanded, "/manage", roles = "Manager")

	def run_properties(self, expanded, unexpanded) :
		"""Manages objects properties 

		   Accepts multiple arguments

		   Caveats: Nicer in a browser with JavaScript support
		"""
		return self.manage_view_properties(expanded, unexpanded, "/manage_propertiesForm", perms = "Manage properties")

	def run_view(self, expanded, unexpanded) :
		"""Views objects

		   Accepts multiple arguments

		   Caveats: Nicer in a browser with JavaScript support
		"""
		return self.manage_view_properties(expanded, unexpanded, "", perms = "View")

	def run_grep(self, expanded, unexpanded) :
		"""Search and optionally replace regexps in objects contents

		   Accepts many options:

			--recurse	recursive search
			--maxdepth n	descend at most n levels
			--type metatype search only objects of meta type xxx
			--owner xxxx	objects owned by user xxxx
			--newer /other/object	objects modified more recently than other
			--older /other/object	objects modified less recently than other
			--mmin n	objects modified less than n minutes ago
			--mtime n	objects modified less than n days ago
			--properties	search in properties too
			--replace xxxx	replaces each occurence of the pattern
					with the string xxx.
			--invert	invert the search: objects that don't match
							   the regexp are selected
			--ignorecase	ignore case: this is just for convenience since
					it's always possible to use a pattern which
					explicitly asks for ignoring case.

		   e.g.:

		     grep --recurse --ignorecase ¨^word" *_html

		     this one will search recursively for each document which
		     id ends in "_html" and which has "word" at the beginning of
		     a line, ignoring differences between UPPER and lower case.

		     grep --properties --type "DTML*" --type Folder somestring *

		     This one will search for "somestring" in all objects which
		     meta type is Folder or begins with "DTML" and their
		     properties.

		     The string to search for and the optionally replacing
		     string could be any regular expression defined by the
		     standard re python module.

		   Hint: You may use multiple --type or --owner arguments
			 and each can contain wildcards.

		   WARNING: don't forget to enclose your regexps between
			    single or double quotes or else some regexps
			    won't work as expected.

		   Caveats: If not given the --properties option, only
			    searches in the document_src() and title
			    attributes of objects that have a document_src
			    attribute (if not clear email me).
		"""   
		options, args = self.getopt(["recurse", "maxdepth=", "owner+", "mmin=", "mtime=", "newer=", "older=", "type+", "replace=", "properties", "invert", "ignorecase"], expanded)
		if (options is None) and (args is None) :
			return -1	# message was already displayed in self.getopt()
		if len(args) < 2 :
			return self.errormessage("Needs one pattern and one object id to grep")
		if options.has_key("invert") and options.has_key("replace") :
			return self.errormessage("Options replace and invert are incompatible")
		try :
			if options.has_key("ignorecase") :
				pattern = re.compile("%s" % args[0], re.I)
			else :
				pattern = re.compile("%s" % args[0])
		except re.error :
			return self.errormessage("You probably entered an invalid regular expression: %s" % args[0])
		def do_grep(obj, zopeshell = self, options=options, pattern=pattern) :
			if obj is not None:
				# tests if the object matches the present options
				if not zopeshell.match_Many(obj, options) :
					return 0

				url = zopeshell.ObjectPath(obj)
				# in the following lines the absence of an _updateProperty
				# attribute indicates an object without properties (e.g. a method)
				# which indicates an object in which we can't search or replace
				# in properties.
				ok = 0
				if options.has_key("replace") :
					if options.has_key("properties") and hasattr(obj, "propertyMap") \
					   and hasattr(obj, "_updateProperty") :
						if not zopeshell.HasPerms(obj, "Access contents information") :
							return 0
						for prop in obj.propertyMap() :
							value = str(obj.getProperty(prop["id"]))
							(newstring, number) = pattern.subn(options["replace"], value)
							# we test permissions only when needed:
							# it is not quick, but prevent dummy error messages
							if number and zopeshell.HasPerms(obj, "Manage properties") :
								obj._updateProperty(prop["id"], newstring)
								ok = ok + number

					if hasattr(obj, "document_src") :
						if zopeshell.HasPerms(obj, "View management screens") :
							src = obj.document_src()
							title = obj.title
							(newsrc, numbersrc) = pattern.subn(options["replace"], src)
							(newtitle, numbertitle) = pattern.subn(options["replace"], title)
							if numbersrc :
								src = newsrc
							if numbertitle :
								title = newtitle
							# we test permissions only when needed:
							# it is not quick, but prevent dummy error messages
							if numbersrc or numbertitle :
								ok = ok + numbersrc + numbertitle
								if (((obj.__class__ == DTMLDocument) or (DTMLDocument in obj.__class__.__bases__)) \
								      and zopeshell.HasPerms(obj, "Change DTML Documents")) \
								   or \
								   (((obj.__class__ == DTMLMethod) or (DTMLMethod in obj.__class__.__bases__)) \
								      and zopeshell.HasPerms(obj, "Change DTML Methods")) :
									obj.manage_edit(src, title)
								elif (((obj.__class__ == PythonScript) or (PythonScript in obj.__class__.__bases__)) \
								      and zopeshell.HasPerms(obj, "Change Python Scripts")) :
									obj.write(src)
								else :
									zopeshell.errormessage("Don't know how to modify object %s" % (url or repr(obj)))
				else :
					if options.has_key("properties") and hasattr(obj, "propertyMap") \
					   and hasattr(obj, "_updateProperty") :
						if not zopeshell.HasPerms(obj, "Access contents information") :
							return 0
						for prop in obj.propertyMap() :
							value = str(obj.getProperty(prop["id"]))
							result = pattern.findall(value)
							if result is not None :
								ok = ok + len(result)

					if hasattr(obj, "document_src") :
						if zopeshell.HasPerms(obj, "View management screens") :
							result = pattern.findall(obj.document_src())
							if result is not None :
								ok = ok + len(result)
							result = pattern.findall(obj.title)
							if result is not None :
								ok = ok + len(result)
				if url is not None :
					if (ok and not options.has_key("invert")) or \
					   ((not ok) and options.has_key("invert")) :
						zopeshell.htmlmessage("%s" % url)
						zopeshell.printf("%s\n" % url)
				else :
					return zopeshell.errormessage("Error while accessing to object %s" % repr(obj))
			return 0
		mx = 1	# default = no recursivity
		if options.has_key("recurse") :
			mx = self.getMaxDepth(options, default=0)	# default full recursivity
			if mx < 0 :
				# an error occured, message already displayed
				return -1
		elif options.has_key("maxdepth") :
			return self.errormessage("Option --maxdepth was given, but there's no --recurse option")
		status = 0
		for arg in args[1:] :
			# current depth is already 1.
			status = status + self.descend(self.toObject(self.__context, arg), do_grep, maxdepth=mx, curdepth=1)
		return status

	def run_find(self, expanded, unexpanded) :
		"""Search objects in the Folder hierarchy

		   Accepts a top Folder from which doing the search as
		   its first argument, and options as its other arguments:

			--maxdepth n	descend at most n levels
			--id xxxx	objects which id matchs xxxx
			--type metatype objects which meta_type is metatype
			--owner xxxx	objects owned by user xxxx
			--newer /other/object	objects modified more recently than other
			--older /other/object	objects modified less recently than other
			--mmin n	objects modified less than n minutes ago
			--mtime n	objects modified less than n days ago
			--exec cmd	exec command for each object found
					you can use {} to match the current full object id
					and single or double quotes around the command itself.

		   e.g.:

		     find / --owner jerome --id "*_html" --maxdepth 2 --exec "addprop author/string {}"

		   Hint: You may use multiple --id, --type and --owner arguments
			 and each can contain wildcards.

		   WARNING: You may very well become addicted to this command ;-)
		"""   
		if not expanded :
			return self.errormessage("Needs one Folder to find from")
		options, args = self.getopt(["id+", "maxdepth=", "owner+", "mmin=", "mtime=", "newer=", "older=", "type+", "exec="], expanded[1:])
		if (options is None) and (args is None) :
			return -1	# message was already displayed in self.getopt()
		def do_find(obj, zopeshell = self, options=options, args=args) :
			if obj is not None:
				# tests if the object matches the present options
				many = zopeshell.match_Many(obj, options)
				if many <= 0 :
					return many

				url = zopeshell.ObjectPath(obj)
				if options.has_key("exec") :
					if url is not None :
						return zopeshell.execCommand(string.replace(options["exec"], "{}", url))
					else :
						return zopeshell.errormessage("Error while accessing to object %s" % repr(obj))

				if url is not None :
					zopeshell.htmlmessage(url)
					zopeshell.printf("%s\n" % url)
				else :
					return zopeshell.errormessage("Error while accessing to object %s" % repr(obj))
			return 0

		mx = self.getMaxDepth(options, default=0)
		if mx < 0 :
			# an error occured, message already displayed
			return -1
		return self.descend(self.toObject(self.__context, expanded[0]), do_find, maxdepth=mx)

	def run_catalog(self, expanded, unexpanded) :
		"""Catalogs objects in the nearest ZCatalog

		   Accepts many arguments:

		   catalog *_dtml MyFolder/*gif [...]

		   WARNING: All objects may not end in the same
			    ZCatalog, because the choice of
			    the nearest ZCatalog is done for each
			    object.
		"""
		if not expanded :
			return self.errormessage("Needs at least one object id")
		status = 0
		for arg in expanded :
			object = self.toObject(self.__context, arg)
			if object is None :
				status = status + self.errormessage('Incorrect path: %s' % arg)
			else :
				# finds all available Catalogs up through the acquisition path
				zcatalog = self.__context.superValues(["ZCatalog"])
				if not zcatalog :
					status = status + self.errormessage("No ZCatalog available for object %s" % self.ObjectPath(object))
				else :
					zcatalog = zcatalog[0]	# we take the first one, which is the nearest
					if not self.HasPerms(zcatalog, 'Manage ZCatalog Entries') :
						status = status - 1
					else :
						zcatalog.catalog_object(object, "%s" % self.ObjectPath(object))
						self.htmlmessage('%s added to ZCatalog %s' % (self.ObjectPath(object), self.ObjectPath(zcatalog)))
		return status

	def run_uncatalog(self, expanded, unexpanded) :
		"""Uncatalogs objects from the nearest ZCatalog

		   Accepts many arguments:

		   uncatalog *_dtml MyFolder/*gif [...]

		   Caveats: Uncatalogging an object which is not
			    present in the ZCatalog is accepted.

		   WARNING: All objects may not be uncatalogged from
			    the same ZCatalog, because the choice of
			    the nearest ZCatalog is done for each
			    object.
		"""
		if not expanded :
			return self.errormessage("Needs at least one object id")
		status = 0
		for arg in expanded :
			object = self.toObject(self.__context, arg)
			if object is None :
				status = status + self.errormessage('Incorrect path: %s' % arg)
			else :
				# finds all available Catalogs up through the acquisition path
				zcatalog = self.__context.superValues(["ZCatalog"])
				if not zcatalog :
					status = status + self.errormessage("No ZCatalog available for object %s" % self.ObjectPath(object))
				else :
					zcatalog = zcatalog[0]	# we take the first one, which is the nearest
					if not self.HasPerms(zcatalog, 'Manage ZCatalog Entries') :
						status = status - 1
					else :
						# WARNING: we don't verify if the object was really in the ZCatalog
						zcatalog.uncatalog_object("%s" % self.ObjectPath(object))
						self.htmlmessage('%s removed from ZCatalog %s' % (self.ObjectPath(object), self.ObjectPath(zcatalog)))
		return status

	def run_lsperms(self, expanded, unexpanded) :
		"""Lists permissions on an object

		   Accepts an object id as its first argument.

		   Accepts the permissions to list as its other
		   arguments:

		   lsperms /QuickSart Change*

		   This will list all permissions which name matches
		   Change* on the /QuickStart object
		"""   
		if not unexpanded :
			return self.errormessage("Needs at least one object id")
		object = self.toObject(self.__context, unexpanded[0])
		if object is None :
			return self.errormessage("Object %s doesn't exist" % unexpanded[0])
		if not self.HasPerms(object, "Change permissions") :
			return -1
		if len(unexpanded) == 1:
			# no permission name, we want all of them
			unexpanded.append("*")
		result = []
		psettings = object.permission_settings()
		for perm in object.ac_inherited_permissions(all=1) :
			pname = perm[0]
			for pattern in unexpanded[1:] :
				# I'd prefer to have an fnmatch.fnmatchUNcase()
				# to be less strict...
				if fnmatch.fnmatchcase(pname, pattern) :
					roles = filter(None, map(lambda r: (r["selected"] == 'SELECTED') and r["name"], object.rolesOfPermission(pname)))
					acquired = ((filter(lambda p, pn=pname: p["name"] == pn, psettings)[0]["acquire"] == 'CHECKED') and 'Yes') or 'No'
					result.append({ "Permission": pname, "Roles": string.join(roles, ', '), "Acquired": acquired })
					break
		self.tableDisplay("lsperms", ["Permission", "Roles", "Acquired"], result)

	def run_setperms(self, expanded, unexpanded) :
		"""Sets permissions on an object

		   Accepts a --noacquire option to not acquire
		   permissions from the parent object.

		   Accepts an object id as its following argument.

		   Accepts a comma separated list of roles to which
		   give this permission. Each role not in the list
		   will have this permission removed.

		   Accepts a list of permissions as its following
		   arguments:

		   setperms --noacquire /MyForum Manager,Editor *Postings*

		   This will give all permissions which name contains Postings
		   to roles Manager and Editor on the object /MyForum
		   For other roles this permission will be removed, and will
		   not be acquired from the parent object.
		"""   
		options, args = self.getopt(["noacquire"], unexpanded)
		if (options is None) and (args is None) :
			return -1	# message was already displayed in self.getopt()
		if len(args) == 2 :
			# no permission name, we want all of them
			args.append("*")
		if len(args) < 3 :
			return self.errormessage("Needs an object id, a comma separated list of roles and a list of permissions")
		object = self.toObject(self.__context, args[0])
		if object is None :
			return self.errormessage("Object %s doesn't exist" % args[0])
		if not self.HasPerms(object, "Change permissions") :
			return -1
		roles = filter(None, map(string.strip, string.split(args[1], ',')))
		acquire = not options.has_key("noacquire")
		for perm in object.ac_inherited_permissions(all=1) :
			pname = perm[0]
			for pattern in unexpanded[1:] :
				# I'd prefer to have an fnmatch.fnmatchUNcase()
				# to be less strict...
				if fnmatch.fnmatchcase(pname, pattern) :
					object.manage_permission(permission_to_manage=pname, roles=roles, acquire=acquire)
					self.htmlmessage("Permission '%s' on object %s was given to roles %s and %s acquired otherwise" % (pname, self.ObjectPath(object), roles, (((not acquire) and 'not') or '')))
					break

	def run_passwd(self, expanded, unexpanded) :
		"""Change or set a user's password

		   Accepts a user name as its first argument.
		   Accepts a password as its second argument.

		   If only one argument is given, then the
		   current user's password is changed:

		   passwd 67G.FDKea

		   or:

		   passwd jerome ùlD31

		   Caveats: Expects the user to exist in the nearest user folder.
		"""   
		if len(unexpanded) == 1 :
			username = None
			passwd = unexpanded[0]
		elif len(unexpanded) == 2 :
			username = unexpanded[0]
			passwd = unexpanded[1]
		else :
			return self.errormessage("Needs a password or an username + password")
		if not self.HasPerms(self.__context.acl_users, 'Manage users') :
			return -1
		if username is None :
			# no username: get the logged in user's one
			username = AccessControl.getSecurityManager().getUser().getUserName()
		user = self.__context.acl_users.getUser(username)
		if user is None :
			return self.errormessage("User %s doesn't exist" % username)
		roles = user.getRoles()
		domains = user.getDomains()
		self.__context.acl_users._changeUser(username, passwd, passwd, roles, domains)
		self.htmlmessage("Password changed for user %s" % username)

	def run_domains(self, expanded, unexpanded) :
		"""Changes/delete allowed domains for a user

		   Accepts a user name as its first argument.
		   If no other argument is given, then allowed
		   domains for this user are deleted: the user
		   can connect from anywhere.
		   Any other argument is treated as a list of
		   domains to be ADDED to the existing list of domains
		   allowed for this user:

		   domains jerome unice.fr

		   Caveats: Expects the user to exist in the nearest user folder.
		"""   
		if not unexpanded :
			return self.errormessage("Needs at least an username")
		if not self.HasPerms(self.__context.acl_users, 'Manage users') :
			return -1
		username = unexpanded[0]
		user = self.__context.acl_users.getUser(username)
		if user is None :
			return self.errormessage("User %s doesn't exist" % username)
		roles = list(user.getRoles())
		domains = list(user.getDomains())
		if len(unexpanded) > 1 :
			# there are domains arguments
			# so we add them
			domains.extend(unexpanded[1:])
			msg = "changed to %s" % repr(domains)
		else :
			# there's no domain argument
			# so we delete all domains
			domains = []
			msg = "deleted"

		self.__context.acl_users._changeUser(username, None, None, roles, domains)
		self.htmlmessage("Domains for user %s %s" % (username, msg))

	def run_roles(self, expanded, unexpanded) :
		"""Changes/delete roles for a user

		   Accepts a user name as its first argument.
		   If no other argument is given, then roles
		   for this user are deleted: the user has no
		   role.
		   Any other argument is treated as a list of
		   roles to be ADDED to this user:

		   roles jerome Manager Editor

		   Caveats: Expects the user to exist in the nearest user folder.
		"""   
		if not unexpanded :
			return self.errormessage("Needs at least an username")
		if not self.HasPerms(self.__context.acl_users, 'Manage users') :
			return -1
		username = unexpanded[0]
		user = self.__context.acl_users.getUser(username)
		if user is None :
			return self.errormessage("User %s doesn't exist" % username)
		roles = list(user.getRoles())
		domains = list(user.getDomains())
		if len(unexpanded) > 1 :
			# there are roles arguments
			# so we add them
			roles.extend(unexpanded[1:])
			msg = "changed to %s" % repr(roles)
		else :
			# there's no role argument
			# so we delete all roles
			roles = []
			msg = "deleted"
		self.__context.acl_users._changeUser(username, None, None, roles, domains)
		self.htmlmessage("Roles for user %s %s" % (username, msg))

	def run_history(self, expanded, unexpanded) :
		"""Displays the commands history.

		   Accepts an optional --clear argument to empty
		   the history, which must exist.

		   Commands stored in a .zshell_history
		   DTML Document are printed. This document
		   must be created manually for the history
		   of commands to be saved.

		   If the current user has the 'Change DTML Documents'
		   permission on the .zshell_history document, then he
		   can either list all commands, along with their
		   execution date, and the username who launched
		   them, or list only commands launched by some users.

		   Otherwise, only the commands launched
		   by the current user are shown, with no additional
		   information.

		     history

		   or:

		     history --clear

		   or:

		     history --user "jer*" --user !jerome

		     This one will list all commands launched by
		     users which name begins with 'jer' but not those
		     from user 'jerome'.

		   WARNING: No security check is done to update the
			    history. However the user needs sufficient
			    permissions to clear the history.
			    This may allow a manager to
			    keep an history of commands run by
			    other users, but in a place where these
			    users normally has no write access, in
			    order to forbid them to modify this
			    history to hide launched commands
			    from the manager. Just tell me
			    if this is not OK, and I'll change it.
		"""   
		options, args = self.getopt(["clear", "user+"], unexpanded)
		if (options is None) and (args is None) :
			return -1	# message was already displayed in self.getopt()
		if args :
			return self.errormessage("Doesn't need any other argument")
		history = self.getHistory()
		if history is not None :
			if options.has_key("clear") :
				# we want to clear it, UpdateHistory will take care of permissions
				self.UpdateHistory("history --clear", clear=1)
			else :
				# we just want to see it.
				# Someone who can modify the .zshell_history can see all commands
				newhistory = history.document_src()
				if not self.HasPerms(history, "Change DTML Documents", verbose=0) :
					if options.has_key("user") :
						return self.errormessage("You're not allowed to use this option")
					# a non-Manager user can only see its commands
					(username, dummy) = self.WhoAmI()
					lines = filter(lambda line, u=username: line and (string.split(line, ',')[1] == u), string.split(newhistory, '\n'))
					newhistory = string.join(map(lambda line: string.split(line, ',')[2], lines), "\n")
				else :
					# The person has sufficient permissions
					# to list only some username's commands
					newh = []
					for line in filter(None, string.split(newhistory, '\n')) :
						cmduser = string.split(line, ',')[1]
						# not optimal, but works:
						if self.match_anystring("user", cmduser, options) :
							newh.append(line)
					newhistory = string.join(newh, '\n')
				self.htmlmessage(string.replace(newhistory, '\n', '<BR>\n'), safe=1)
				self.printf("%s\n" % newhistory)
		else :
			return self.errormessage("No history available")

	def run_call(self, expanded, unexpanded) :
		"""Calls an object with optional parameters

		   The object name may be specified with its full path with dots or slashes:

		   call MyFolder.MyObject(_,_.REQUEST,arg1="thisarg"[,arg2="anotherarg"][,...])

		   or:

		   call MyFolder.MyObject(context,context.REQUEST,arg1="thisarg"[,arg2="anotherarg"][,...])

		   another example:

		   call index_html

		   This last one will return the unrendered version of index_html

		   Both _ and context may be used if needed.

		   Hint: Don't use any space in your command, or else enclose your
			 command between single or double quotes.

		   WARNING: Calling zshell itself is a Very Bad Idea (tm) and can kill Zope
		"""   
		if not expanded :
			return self.errormessage("Needs an object id to call")

		# Michel@DC: you should factor the object out of this eval and
		# validate it with
		# SecurityManager.checkPermission('View', object).
		# Also, 'eval' without an namespace qualifying 'in'
		# clause can be bad!  Try and do this without eval.

		# Jerome: Don't know how without eval !
		# new code looks very ugly and accessing to object's
		# properties doesn't work anymore, unfortunately.

		objectstr = string.join(unexpanded, ' ')
		pos = string.find(objectstr, '(')
		if pos == -1 :
			# called without arguments
			objpath = objectstr
			objargs = ""
		else :
			# called with arguments, skip them
			# because we only want the object name
			objpath = objectstr[:pos]
			objargs = objectstr[pos:]

		objpath = string.replace(objpath, '.', '/')
		object = self.toObject(self.__context, objpath)
		if object is None :
			# maybe should do something to re-allow properties to be used
			return self.errormessage("Object %s not found" % objectstr)
		else :
			if not self.HasPerms(object, 'View') :
				return -1
			else :
				_ = context = self.__context
				callresult = str(eval("object%s" % objargs))
				self.printf("%s" % callresult)
				self.htmlmessage(callresult, safe=1)

	def run_lsusers(self, expanded, unexpanded) :
		"""Lists users in the nearest User Folder

		   Accepts multiple user names as its arguments,
		   wildcards are accepted:

		   lsusers user1 [jer*] [...]
		"""
		if not unexpanded :
			unexpanded = ["*"]	# List all users
		if not self.HasPerms(self.__context.acl_users, 'Manage users') :
			return -1
		result = []
		for username in self.__context.acl_users.getUserNames() :
			for uname in unexpanded :
				if fnmatch.fnmatchcase(username, uname) :
					user = self.__context.acl_users.getUser(username)
					result.append({ "UserName": username, "Roles": string.join(user.getRoles(), ', '), "InContext": string.join(user.getRolesInContext(self.__context), ', '), "Domains": string.join(user.getDomains(), ', ') })
		self.tableDisplay("lsusers", ["UserName", "Roles", "InContext", "Domains"], result)

	def run_delusers(self, expanded, unexpanded):
		"""Delete users from the nearest User Folder

		   Accepts multiple user names as its arguments:

		   delusers user1 [user2] [...]

		   WARNING: No wildcard is expanded, for security reasons.
		"""
		if not expanded :
			return self.errormessage('Needs an userid as the first argument')
		if not self.HasPerms(self.__context.acl_users, 'Manage users') :
			return -1
		status = 0
		usernames = []
		for username in unexpanded :
			if username not in self.__context.acl_users.getUserNames() :
				status = status + self.errormessage("User %s doesn't exists" % username)
			else :
				usernames.append(username)

		self.__context.REQUEST.set("names", usernames)
		self.__context.acl_users.manage_users("Delete", REQUEST=self.__context.REQUEST)
		if usernames :
			self.htmlmessage('Users %s deleted' % string.join(usernames, ", "))

		# don't be fucked by Zope's automatic redirection
		self.__context.REQUEST.RESPONSE.setStatus(200)
		return status

	def run_addusers(self, expanded, unexpanded) :
		"""Adds users into the nearest User Folder

		   The users added have no role, and no domain.
		   Accepts multiple arguments, each argument must be
		   made of a username, a slash character, and a password:

		   addusers jerome/kyx.ud34 [john/9!AZce] [...]
		"""
		if not unexpanded :
			return self.errormessage('Needs an userid/password as the first argument')
		if not self.HasPerms(self.__context.acl_users, 'Manage users') :
			return -1
		status = 0
		for arg in unexpanded :
			split = string.split(arg, '/')
			if len(split) != 2 :
				status = status + self.errormessage('Incorrect username/password: %s' % arg)
			else :
				(username, password) = split
				if username in self.__context.acl_users.getUserNames() :
					status = status + self.errormessage("User %s already exists" % username)
				else :
					self.__context.REQUEST.set("name", username)
					self.__context.REQUEST.set("password", password)
					self.__context.REQUEST.set("confirm", password)
					self.__context.REQUEST.set("domains", "")
					self.__context.REQUEST.set("roles", [])
					self.__context.acl_users.manage_users("Add", REQUEST=self.__context.REQUEST)
					self.htmlmessage('User %s added with password %s' % (username, password))
		# don't be fucked by Zope's automatic redirection
		self.__context.REQUEST.RESPONSE.setStatus(200)
		return status

	def run_lroles(self, expanded, unexpanded) :
		"""Sets local roles for an user in the local Folder

		   Accepts the user's name as its first argument
		   Accepts a list of local roles to give to this user
		   as its remaining arguments, if no role name is given,
		   then all local roles for this user are deleted:

		   lroles jerome Manager [Moderator] [...]
		"""
		if not unexpanded :
			return self.errormessage('Needs an userid as the first argument')
		username = unexpanded[0]
		if len(unexpanded) > 1 :
			roles = unexpanded[1:]
			# Zope accepts even if user and roles don't exist at all
			# so we have to test it ourselves
			if username not in self.__context.acl_users.getUserNames() :
				return self.errormessage("Unknown user %s" % username)
			if not self.HasPerms(self.__context, "Change permissions") :
				return -1
			# should we also test if roles exits ?
			self.__context.manage_setLocalRoles(userid=username, roles=roles)
			self.htmlmessage('User %s now has local roles: %s' % (username, string.join(roles, ', ')))
		else :
			self.__context.manage_delLocalRoles(userids=[username])
			self.htmlmessage('User %s now has no local role' % username)

	def run_whoami(self, expanded, unexpanded) :
		"""Shows the current username"""
		if expanded :
			return self.errormessage("Doesn't need any argument")
		(username, roles) = self.WhoAmI()
		self.htmlmessage('Username: %s &nbsp;&nbsp;&nbsp;&nbsp; Roles: %s' % (username, string.join(roles, ', ')), safe=1)
		self.printf("%s\n" % username)

	def run_pack(self, expanded, unexpanded) :
		"""Packs the ZODB

		   Accepts a number of days as its single argument:

		   pack 3
		"""
		if not self.HasRoles(self.__context.Control_Panel, 'Manager') :
			return -1
		if len(unexpanded) > 1 :
			return self.errormessage('Needs a number of days as an argument')
		elif not unexpanded :
			ndays = 0
		else :
			ndays = int(unexpanded[0])
		try:
			self.__context.Control_Panel.manage_pack(days = ndays)
		except FileStorage.FileStorageError :
			pass	# no pack needed, but we don't want the error message
		self.htmlmessage("Database packed")

	def run_restart(self, expanded, unexpanded) :
		"""Restarts Zope

		   Works fine but unfortunately Zope redirects
		   us automatically to zshell/manage_main
		"""
		if not self.HasRoles(self.__context.Control_Panel, 'Manager') :
			return -1
		if expanded :
			return self.errormessage("Doesn't need any argument")
		self.__context.Control_Panel.manage_restart(self.__context.REQUEST.URL0)

	def run_shutdown(self, expanded, unexpanded) :
		"""Shutdowns Zope

		   Works fine but unfortunately looks ugly.
		"""
		if not self.HasRoles(self.__context.Control_Panel, 'Manager') :
			return -1
		if expanded :
			return self.errormessage("Doesn't need any argument")
		self.__context.Control_Panel.manage_shutdown()

	def run_dbname(self, expanded, unexpanded) :
		"""Returns Zope's DataBase name
		"""
		if expanded :
			return self.errormessage("Doesn't need any argument")
		self.htmlmessage(self.__context.Control_Panel.db_name(), printable=1)

	def run_dbsize(self, expanded, unexpanded) :
		"""Returns Zope's DataBase size
		"""
		if expanded :
			return self.errormessage("Doesn't need any argument")
		self.htmlmessage(self.__context.Control_Panel.db_size(), printable=1)

	def run_uptime(self, expanded, unexpanded) :
		"""Returns Zope's uptime
		"""
		if expanded :
			return self.errormessage("Doesn't need any argument")
		self.htmlmessage(self.__context.Control_Panel.process_time(), printable=1)

	def run_mkver(self, expanded, unexpanded) :
		"""Create versions

		   Accepts multiple arguments:

		   mkver debug [stable] [...]
		"""
		if not unexpanded :
			return self.errormessage('Needs a version id as the first argument')
		if not self.HasPerms(self.__context, 'Add Versions') :
			return -1
		status = 0
		for vid in unexpanded :
			if vid in self.__context.objectIds() :
				status = status + self.errormessage('Object %s already exists' % vid)
			else :
				self.__context.manage_addProduct["OFSP"].manage_addVersion(id = vid, title = vid)
				self.htmlmessage('Version %s created' % vid)
		return status

	def run_enter(self, expanded, unexpanded) :
		"""Enter into a version

		   Accepts a version id (with an optional path) as its only argument

		   enter debug

		   Caveats: it seems you're not really in the version until the end of the
			    transaction, so commands entered after 'enter' will work outside
			    of this version.
		"""
		if not expanded :
			return self.errormessage('Needs a version id as an argument')
		vexist = self.toObject(self.__context, expanded[0])
		if not vexist :
			return self.errormessage("Version <em><b>%s</b></em> doesn't exist" % expanded[0])
		else :
			if not self.HasPerms(vexist, 'Join/leave Versions') :
				return -1
			vexist.enter(self.__context.REQUEST, self.__context.REQUEST.RESPONSE)

			# get_transaction().commit(1) doesn't seem to do it !

			# don't be fucked by Zope's automatic redirection
			self.__context.REQUEST.RESPONSE.setStatus(200)
			self.htmlmessage("You'll be working in version %s at the end of the current transaction" % self.ObjectPath(vexist))

	def run_leave(self, expanded, unexpanded) :
		"""Quits a version

		   Accepts a version id as its only argument

		   leave debug

		   Caveats: it seems you're not really outside of the version until the end of the
			    transaction, so commands entered after 'leave' will work inside
			    this version.
		"""
		if not expanded :
			return self.errormessage('Needs a version id as an argument')
		vexist = self.toObject(self.__context, expanded[0])
		if not vexist :
			return self.errormessage("Version <em><b>%s</b></em> doesn't exist" % expanded[0])
		else :
			if not self.HasPerms(vexist, 'Join/leave Versions') :
				return -1
			vexist.leave(self.__context.REQUEST, self.__context.REQUEST.RESPONSE)

			# get_transaction().commit(1) doesn't seem to do it !

			# don't be fucked by Zope's automatic redirection
			self.__context.REQUEST.RESPONSE.setStatus(200)
			self.htmlmessage("You'll not be working in version %s anymore at the end of the current transaction" % self.ObjectPath(vexist))

	def run_save(self, expanded, unexpanded) :
		"""Commits a version's changes

		   Accepts a commit message as its optional argument:

		   save The new version seems to be OK

		   WARNING: Needs testers
		"""
		if not self.__version :
			return self.errormessage("Not in a version")
		else :
			objver = self.toObject(self.__context, self.__version)
			if objver is None :
				return self.errormessage("Error while accessing version %s" % self.__version)
			else :
				if not self.HasPerms(objver, 'Save/discard Version changes') :
					return -1
				# for save, remark doesn't have a default value (according to Zope 2.3.0 sources)
				objver.save(remark = (string.join(expanded, ' ') or 'No comment'))
				self.htmlmessage("Version %s saved" % self.ObjectPath(objver))

	def run_discard(self, expanded, unexpanded) :
		"""Discards a version's changes

		   Accepts a discard message as its optional argument:

		   discard I was doing completely wrong

		   WARNING: Needs testers
		"""
		if not self.__version :
			return self.errormessage("Not in a version")
		else :
			objver = self.toObject(self.__context, self.__version)
			if objver is None :
				return self.errormessage("Error while accessing version %s" % self.__version)
			else :
				if not self.HasPerms(objver, 'Save/discard Version changes') :
					return -1
				# for discard, remark's default value is an empty string
				objver.discard(remark = string.join(expanded, ' '))
				self.htmlmessage("Version %s discarded" % self.ObjectPath(objver))

	def run_copy(self, expanded, unexpanded) :
		"""Copy objects to the clipboard

		   Accepts multiple objects ids as its arguments, but
		   each object must be in the current Folder:

		   copy obj1 [obj2] [...]
		"""
		if not expanded :
			return self.errormessage("Needs some objects ids to copy")
		if not self.HasPerms(self.__context, 'View management screens') :
			return -1
		status = 0
		objids = []
		for objid in expanded :
			if '/' in objid :
				status = status + self.errormessage('Paths for objects ids are not allowed at this time: %s' % objid)
			else :
				objids.append(objid)
		try :
			self._clipboard = self.__context.manage_copyObjects(ids = objids)
			for objid in objids :
				self.htmlmessage('%s copied to clipboard' % objid)
		except AttributeError, msg :
			status = status + self.errormessage("Object %s doesn't exist" % msg)
		return status

	def run_cut(self, expanded, unexpanded) :
		"""Cut objects to the clipboard

		   Accepts multiple objects ids as its arguments, but
		   each object must be in the current Folder:

		   cut obj1 [obj2] [...]
		"""
		if not expanded :
			return self.errormessage("Needs some objects ids to cut")
		if not self.HasPerms(self.__context, 'View management screens') :
			return -1
		status = 0
		objids = []
		for objid in expanded :
			if '/' in objid :
				status = status + self.errormessage('Paths for objects ids are not allowed at this time: %s' % objid)
			else :
				objids.append(objid)
		try :
			self._clipboard = self.__context.manage_cutObjects(ids = objids)
			for objid in objids :
				self.htmlmessage('%s cut to clipboard' % objid)
		except AttributeError, msg :
			status = status + self.errormessage("Object %s doesn't exist" % msg)
		return status

	def run_paste(self, expanded, unexpanded) :
		"""Paste the clipboard's contents into the current Folder"""
		if expanded :
			return self.errormessage("Doesn't need any argument")
		if not self.HasPerms(self.__context, 'View management screens') :
			return -1
		if not hasattr(self, '_clipboard') :
			return self.errormessage("Clipboard is empty")
		try :
			self.__context.manage_pasteObjects(cb_copy_data = self._clipboard)
			self.htmlmessage("Clipboard's content pasted into %s" % self.getcwd())
		except CopyError :
			return self.errormessage("Impossible to paste clipboard's content into %s" % self.getcwd())

	def run_dump(self, expanded, unexpanded) :
		"""Exports objects source to a directory on the server

		   Accepts a destination directory as its first
		   argument. The destination directory must exist
		   on the server.

		   Accepts multiple objects ids to export as its
		   following arguments.

		   dump /home/jerome/dtml /*_html /*_dtml

		   Hint:    Be careful to give sufficient permissions to
			    the user which Zope runs as on the destination
			    directory.

		   Caveats: Only objects which have a callable
			    document_src attribute can be exported this way.
		"""         
		if len(expanded) < 2 :
			return self.errormessage("Needs at least a destination directory and one object id to dump")
		destination = os.path.normpath(os.path.expanduser(expanded[0])) # in case there's a ~username
		if not os.path.isdir(destination) :
			return self.errormessage("%s is not a directory" % destination)
		status = 0
		for arg in expanded[1:] :
			object = self.toObject(self.__context, arg)
			if object is None :
				status = status + self.errormessage("Object %s doesn't exist" % arg)
			elif not self.HasPerms(object, 'View management screens') :
				status = status - 1
			elif not hasattr(object, "document_src") or not callable(object.document_src) :
				status = status + self.errormessage("Doesn't know how to dump object %s" % arg)
			else :
				fname = os.path.join(destination, object.getId())
				try :
					fout = open(fname, "wb")
					fout.write(object.document_src())
					fout.close()
					self.htmlmessage("Object %s dumped to server as %s" % (self.ObjectPath(object), fname))
				except IOError, msg :
					status = status + self.errormessage('Error %s, occured while dumping %s' % (msg, arg))
		return status

	def run_export(self, expanded, unexpanded) :
		"""Exports objects to the server

		   Accepts a --xml option to export as xml
		   data.

		   Accepts multiple objects ids to export

		   export --xml MyPath/Myobject /QuickStart

		   Caveats: Exports exclusively to the server.
			    The Root Folder is exported as .zexp or .xml
		"""         
		options, args = self.getopt(["xml"], expanded)
		if (options is None) and (args is None) :
			return -1	# message was already displayed in self.getopt()
		if not args :
			return self.errormessage("Needs at least one object id to export")
		status = 0
		for arg in args :
			object = self.toObject(self.__context, arg)
			if object is None :
				status = status + self.errormessage("Object %s doesn't exist" % arg)
			elif not hasattr(object, "aq_parent") :
				status = status + self.errormessage("Object %s is not exportable" % arg)
			elif not self.HasPerms(object.aq_parent, 'Import/Export objects') :
				status = status - 1
			else :
				toxml = 0
				download = 0	# TODO: Zope 2.3.2 is buggy, so don't allow downloads yet
				if options.has_key("xml") :
					toxml = 1
				object.aq_parent.manage_exportObject(id=object.getId(), download=download, toxml=toxml)
				fname = "%s.%s" % (object.getId(), (toxml and 'xml') or 'zexp')
				self.htmlmessage("Object %s exported to server as %s" % (self.ObjectPath(object), fname))
		return status

	def run_import(self, expanded, unexpanded) :
		"""Imports objects into the current Folder

		   Accepts multiple filenames to import:

		   import one.zexp [two.zexp] [...]
		"""   
		if not unexpanded :
			return self.errormessage("Needs some filenames to import")
		if not self.HasPerms(self.__context, 'Import/Export objects') :
			return -1
		for filename in unexpanded :
			self.__context.manage_importObject(filename)
			self.htmlmessage('%s imported successfully' % filename)

	def run_takeown(self, expanded, unexpanded) :
		"""Take ownership

		   Optionally accepts --recurse as an option to ask for a recursive action.
		   Accepts multiple pathnames as its other arguments:

		   takeown [--recurse] path/to/obj1 [otherpath/obj2] [...]

		   Caveats: Due to a bug in Zope 2.3.2, taking ownership
			    recursively from a folderish object you already own
			    does nothing, even if you don't already own the full
			    subtree. You should try to do it with the find command
			    instead if you don't want Zope's default buggy behavior.
		"""
		options, args = self.getopt(["recurse"], expanded)
		if (options is None) and (args is None) :
			return -1	# message was already displayed in self.getopt()
		recursive = 0
		recursive_msg = ""
		if options.has_key("recurse") :
			recursive = 1
			recursive_msg = "recursively "
		if not args :
			return self.errormessage("Needs at least one object id")
		chownto = AccessControl.getSecurityManager().getUser()
		status = 0
		for objpath in args :
			object = self.toObject(self.__context, objpath)
			if object is None :
				status = status + self.errormessage('Incorrect path: %s' % objpath)
			elif not self.HasPerms(object, 'Take ownership') :
				status = status - 1
			else :
				object.changeOwnership(chownto, recursive = recursive)
				self.htmlmessage('%s owner %schanged to %s' % (self.ObjectPath(object), recursive_msg, chownto.getUserName()))
		return status

	def run_man(self, expanded, unexpanded) :
		"""Displays command's man pages

		   Accepts several commands' names as its arguments
		   or none to list all commands:

		   man [cmd1] [...]
		"""   
		methodslist = map(lambda n: n[4:], filter(lambda f: f[:4] == 'run_', self.__class__.__dict__.keys()))
		if not unexpanded :
			unexpanded = methodslist
		unexpanded.sort()

		results = []
		for method in unexpanded :
			if results :
				# more than one command to display help for
				# so we separate them in the plain text output
				self.printf("\n--------\n\n")
			if not hasattr(self, 'run_' + method) :
				help = helphtml = "Invalid command"
			else :
				help = getattr(self, 'run_' + method).__doc__
				if not help :
					help = helphtml = "Undocumented command"
				else :
					helplines = map(string.strip, string.split(help, '\n'))
					help = string.join(helplines, '\n')
					helphtml = string.join(helplines, '<br />')
			command = '<a href="%s?zshellscript=man%%20%s&zshellscript=%s&zshelldontrun=1">%s</a>' % (self.__context.REQUEST.URL0, method, method, method)
			results.append({"Command": command, "Help": helphtml})
			self.printf("%s: %s\n" % (method, help))
		self.tableDisplay("man", ["Command", "Help"], results)

	def run_whatis(self, expanded, unexpanded) :
		"""An alias to man"""
		return self.run_man(expanded, unexpanded)

	def run_help(self, expanded, unexpanded) :
		"""An alias to man"""
		return self.run_man(expanded, unexpanded)

	def run_apropos(self, expanded, unexpanded) :
		"""An alias to man"""
		return self.run_man(expanded, unexpanded)

	def run_about(self, expanded, unexpanded) :
		"""About this software"""
		msg =  "ZShell v%s" % __version__
		url = "http://cortex.unice.fr/~jerome/zshell/"
		who = "Jerome Alet"
		email = "alet@unice.fr"
		self.__stdout.write("%s (%s) (C) 2001 %s - %s\n%s\n" % (msg, url, who, email, __doc__))
		x = self.__temphtml
		x._text("%s (" % msg)
		x.a(url, href="url", target="top")
		x._text(") by ")
		x.a(who, href="mailto:%s" % email)
		x._br().pre("%s" % __doc__)

	def run_zhelp(self, expanded, unexpanded) :
		"""Search terms in Zope's internal help

		   Accepts multiple arguments which are concatenated together:

		   zhelp ZClass
		"""
		self.__context.REQUEST.set("SearchableText", string.join(unexpanded, " "))
		results = self.__context.HelpSys.results(self.__context, self.__context.REQUEST)
		# we just want the result lines begining with an <a href=" tag, the rest is uninteresting
		self.htmlmessage(string.join(filter(lambda r: r[:9] == '<a href="', string.split(results, "\n")), "\n"), safe=1)

	def run_google(self, expanded, unexpanded) :
		"""Search a phrase on Google

		   google zope

		   Caveats: Nicer in a browser with JavaScript support
		"""
		# we need a way to display it correctly in our page
		# unfortunately links in google's results are relative
		# so while the display is correct, link to previous and next results
		# are incorrect.
		# current solution: opens a new windows with javascript
		self.newwindow('http://www.google.com/search?q=%s' % string.join(unexpanded, '%20'))

	def run_nipltd(self, expanded, unexpanded) :
		"""Search a phrase on NIP Ltd Zope's archives

		   nipltd subtransactions

		   Caveats: Nicer in a browser with JavaScript support
		"""
		# see the google command
		self.newwindow('http://zope.nipltd.com/public/lists/zope-archive.nsf/Main?SearchView&Query=%s' % string.join(unexpanded, '%20'))

	def run_zope(self, expanded, unexpanded) :
		"""Search terms on Zope.org

		   zope ZShell

		   Caveats: Nicer in a browser with JavaScript support
		"""
		# see the google command
		self.newwindow('http://www.zope.org/SiteIndex/search?text_content=%s' % string.join(unexpanded, '%20'))

	def run_wget(self, expanded, unexpanded) :
		"""Sucks documents from the web and import them in the current Folder

		   Accepts multiple arguments, and can retrieve files from the
		   filesystem, or even complete directories.

		   wget http://www.zope.org/ http://www.gnu.org/graphics/gnu-head-sm.jpg

		   or:

		   wget ~jerome/mydirectory/*.html /home/*/public_html http://localhost

		   Caveats: Maybe needs a recursive option, but I'm not sure:
			    it's already very powerful.
		"""
		if not unexpanded:
			return self.errormessage('Needs at least one argument')
		if not self.HasPerms(self.__context, 'Add Documents, Images, and Files') :
			return -1

		# expand arguments from the filesystem, not the ZODB
		# in the case there's a file: scheme or no scheme at all.
		expanded = []
		for uarg in unexpanded :
			if uarg[:5] == 'file:' :
				uarg = uarg[5:]
			uarg = os.path.expanduser(uarg) # in case of a ~username
			if os.path.isdir(uarg) : # it's a filesystem directory, so we want all its files
				uarg = os.path.join(uarg, '*')
			expanded.extend(self.ShellExpand(uarg, zodb=0) or [uarg])

		status = 0
		for arg in expanded :
			try :
				# WARNING: both urlopen and object.read may
				# raise an IOError, in the latter case that's when
				# object is a filesystem directory
				object = urllib.urlopen(arg)
				info = object.info()
				ctype = info.gettype()
				mtype = info.getmaintype()
				stype = info.getsubtype()
				data = object.read()
				realurl = object.geturl()
				if realurl[-1] == '/' :
					fname = 'index' + '_' + stype
				else :
					fname = filter(None, string.split(realurl, '/'))[-1]
				if fname in self.__context.objectIds() :
					status = status + self.errormessage('Object %s already exists' % fname)
				else :
					if mtype == "image" :
						# Image
						self.__context.manage_addImage(id = fname, file = data, title = realurl, precondition = '', content_type = ctype)
					elif ctype == 'text/html' :
						# DTML Document
						self.__context.manage_addDTMLDocument(id = fname, title = realurl, file = data)
					else :
						# normal File
						self.__context.manage_addFile(id = fname, file = data, title = realurl, precondition = '', content_type = ctype)
					self.htmlmessage('%s added as %s, size is %ld bytes' % (realurl, fname, len(data)))
				del data
				object.close()
				del object
			except IOError,msg :
				status = status + self.errormessage('Error %s, occured while retrieving %s' % (msg, arg))
		return status

	def run_mkuf(self, expanded, unexpanded) :
		"""Creates User Folders

		   Accepts multiple folders as its arguments:

		   mkuf /Folder1/Folder2 [...]

		   Remark: The User Folder is only created in the deepest
			   folderish object, e.g. in the example above
			   the User Folder will be created in Folder1/Folder2
			   but not in Folder1.
		"""   
		if not expanded :
			return self.errormessage("Needs at least a folder id")

		status = 0
		for arg in expanded :
			object = self.toObject(self.__context, arg)
			if object is not None :
				if not object.isPrincipiaFolderish :
					status = status + self.errormessage("%s is not a Folderish object" % self.ObjectPath(object))
				elif 'acl_users' in object.objectIds() :
					status = status + self.errormessage("%s already contains an User Folder or an object named acl_users" % self.ObjectPath(object))
				elif not self.HasPerms(object, 'Add User Folders') :
					status = status - 1
				else :
					object.manage_addUserFolder()
					self.htmlmessage("User Folder added in object %s" % self.ObjectPath(object))
		return status

	def run_mkdir(self, expanded, unexpanded) :
		"""Create Folders

		   Accepts multiple pathnames as its arguments,
		   and creates Folders recursively:

		   mkdir path/to/folder/to/create [...]
		"""
		if not expanded:
			return self.errormessage('Needs at least one argument')
		status = 0
		for foldername in expanded :
			exist = self.toObject(self.__context, foldername)
			if exist is not None :
				status = status + self.errormessage('Folder %s already exists' % self.ObjectPath(exist))
				continue

			if foldername[0] == '/' :
				c = '/'
				foldername = foldername[1:]
			else :
				c = ''
			components = filter(None, string.split(foldername, '/'))
			curpath = c[:]
			oldcurpath = curpath[:]
			error = 0
			for component in components :
				if curpath != c :
					curpath = curpath + '/' + component
				else :
					curpath = curpath + component
				if self.toObject(self.__context, curpath) is None :
					parent = self.toObject(self.__context, oldcurpath)
					if parent is None :
						status = status + self.errormessage('Unknown error on %s' % foldername)
						error = 1
						break
					if component not in parent.objectIds() :
						if not self.HasPerms(parent, "Add Folders") :
							status = status - 1
							error = 1
							break
						else :
							parent.manage_addFolder(id = component)
				oldcurpath = curpath[:]
			if not error :
				self.htmlmessage('Folder %s created' % foldername)
		return status

	def run_pwd(self, expanded, unexpanded) :
		"""Returns the current working Folder"""
		if expanded :
			return self.errormessage("Doesn't need any argument")
		self.printf("%s" % self.getcwd())
		self.htmlmessage("Current folder is: %s" % self.getcwd())

	def run_cd(self, expanded, unexpanded) :
		"""Change Directory

		   Accepts a full pathname as its single argument:

		   cd SubFolder/SubSubFolder
		""" 
		if len(expanded) != 1 :
			return self.errormessage('Needs one and only one argument')
		newdir = self.toObject(self.__context, expanded[0])
		if (newdir is not None) and newdir.isPrincipiaFolderish :
			self.__context = newdir
			self.htmlmessage("Current folder is: %s" % self.ObjectPath(newdir))
		else :
			self.errormessage("Incorrect path: %s" % expanded[0])
			self.run_pwd([], [])
			return -1

	def run_rm(self, expanded, unexpanded) :
		"""Deletes objects

		   Accepts multiple pathnames as its arguments:

		   rm path1/object1 [...]

		   WARNING: deletion is recursive and you can even delete the
		   current Folder. USE AT YOUR OWN RISK !
		"""
		if not expanded :
			return self.errormessage('Needs at least one argument')
		status = 0
		for objpath in expanded :
			object = self.toObject(self.__context, objpath)
			if object is None :
				status = status + self.errormessage("Incorrect path: %s" % objpath)
			else :
				objurl = self.ObjectPath(object)
				if hasattr(object, 'aq_parent') :
					if not self.HasPerms(object.aq_parent, 'Delete objects') :
						status = status - 1
					else :
						if not hasattr(object.aq_parent, "manage_delObjects") or not callable(object.aq_parent.manage_delObjects) :
							status = status + self.errormessage("manage_delObjects: operation not supported on %s" % self.ObjectPath(object.aq_parent))
						else :
							object.aq_parent.manage_delObjects(ids = [object.getId()])
							self.htmlmessage("%s removed" % objurl)
				else :
					status = status + self.errormessage("Unknown error on: %s" % objurl)
		return status

	def run_mv(self, expanded, unexpanded) :
		"""Moves objects

		   Accepts multiple source arguments
		   Each source argument must be an object id and
		   each object should be in the current Folder.
		   The last argument is the destination Folder,
		   and may be a slash delimited pathname:

		   mv obj1 [obj2] [...] destination

		   Caveats: can't rename objects yet
		"""
		return self.mv_or_cp("mv", expanded)

	def run_cp(self, expanded, unexpanded) :
		"""Copy objects objects

		   Accepts multiple source arguments
		   Each source argument must be an object id and
		   each object should be in the current Folder.
		   The last argument is the destination Folder,
		   and may be a slash delimited pathname:

		   cp obj1 [obj2] [...] destination

		   Caveats: destination must be a Folder
		"""
		return self.mv_or_cp("cp", expanded)

	def run_ls(self, expanded, unexpanded) :
		"""List objects

		   Accepts multiple arguments:

		   ls Contr?l_Pan*/Products/Sq* MyFolder/*
		"""
		if not expanded :
			expanded = self.ShellExpand("*") # no argument: list all

		if expanded :
			status = 0
			results = []
			for arg in expanded :
				object = self.toObject(self.__context, arg)
				if object is not None :
					if hasattr(object, 'aq_parent') :
						if not self.HasPerms(object.aq_parent, 'Access contents information') :
							status = status - 1
							continue

					objurl = self.ObjectPath(object)
					urls = '<a href="%s/manage" target="top">Manage</a>/<a href="%s" target="top">View</a>' % (objurl, objurl)
					ownerinfo = object.owner_info()
					if (ownerinfo is not None) :
						if hasattr(ownerinfo, "has_key") and ownerinfo.has_key('id') :
							owner = ownerinfo['id']
						else :
							# at least for /Control_Panel/Products[/*]
							owner = repr(ownerinfo)
					else :
						owner = 'Not owned'

					try :
						modtime = object.bobobase_modification_time().strftime("%Y-%m-%d %H:%M:%S %Z")
					except :
						modtime = "Unknown"

					results.append({"Id": object.getId(), "Title": object.title, "MetaType": self.getMetaType(object), "Mod. Time": modtime, "Owner": owner, "SubObj": len(object.objectValues()), "Actions": urls })
					self.printf("%s\n" % objurl)
			self.tableDisplay("ls", ["Id", "Title", "MetaType", "Mod. Time", "Owner", "SubObj", "Actions"], results)
			return status
		else :
			self.htmlmessage("Empty")

	def run_setprop(self, expanded, unexpanded) :
		"""Sets an object's property value

		   Accepts mandatory --name and --value options, each with an argument,
		   and multiple objects ids as its remaining arguments:

		   setprop --name author --value "William Shakespeare" Hamlet_dtml Othello_?tml

		   This sets the property 'author' value to 'William Shakespeare'
		   to the objects Hamlet_dtml and Othello_?tml in the
		   current Folder.
		"""
		options, args = self.getopt(["name=", "value="], expanded)
		if (options is None) and (args is None) :
			return -1	# message was already displayed in self.getopt()
		if not args :
			return self.errormessage("Needs at least one object to change this property")
		if not (options.has_key("name") and options.has_key("value")) :
			return self.errormessage("You must supply a property name and value")
		property = options["name"]
		if options.has_key("value") :
			propvalue = options["value"]
			try :
				# maybe it's a list in a string, e.g. "['e', 'f']"
				# or something like that
				newvalue = eval(propvalue)
				if (type(newvalue) != type(0)) and (type(newvalue) != type(0.0)) :
					# we mustn't convert numeric to string
					propvalue = newvalue
			except NameError :
				pass	# normal string
		else :
			propvalue = ""

		status = 0
		for arg in args :
			object = self.toObject(self.__context, arg)
			if object is not None :
				if not self.HasPerms(object, 'Manage properties') :
					status = status - 1
				elif hasattr(object, 'hasProperty') :
					if not object.hasProperty(property) :
						status = status + self.errormessage("Object %s has no property %s" % (self.ObjectPath(object), property))
					else :
						# in the following lines the absence of a _updateProperty
						# attribute indicates an object without properties (e.g. a method)
						# which indicates an object for which setting properties is a nonsense
						if hasattr(object, "_updateProperty") :
							object._updateProperty(property, propvalue)
							self.htmlmessage("Object %s property %s was modified to %s" % (self.ObjectPath(object), property, str(propvalue)))
		return status

	def run_addprop(self, expanded, unexpanded) :
		"""Adds a property to objects

		   Accepts --name and --type mandatory options with arguments,
		   and an optional --value option with an argument.

		   Accepts multiple objects ids as its other arguments:

		   addprop --name description --type string .

		   This adds a property named 'description' and type 'string'
		   to the current Folder, leaving this property's value empty.

		   addprop --name author --type string --value Shakespeare /QuickStart/*_html

		   This adds a property named 'author' of type 'string'
		   and which value is 'Shakespeare' to all objects
		   which id match *_html in the /QuickStart Folder

		   Caveats: No check is done to verify that the property type is valid.
		"""   
		options, args = self.getopt(["name=", "type=", "value="], expanded)
		if (options is None) and (args is None) :
			return -1	# message was already displayed in self.getopt()
		if not args :
			return self.errormessage("Needs at least one object to add a property to")
		if not (options.has_key("name") and options.has_key("type")) :
			return self.errormessage("A property needs a name, a type and an optional value")
		property = options["name"]
		proptype = options["type"]
		if options.has_key("value") :
			propvalue = options["value"]
			try :
				# maybe it's a list in a string, e.g. "['e', 'f']"
				# or something like that
				newvalue = eval(propvalue)
				if (type(newvalue) != type(0)) and (type(newvalue) != type(0.0)) :
					# we mustn't convert numeric to string
					propvalue = newvalue
			except NameError :
				pass	# normal string
		else :
			propvalue = ""
		status = 0
		for arg in args :
			object = self.toObject(self.__context, arg)
			if object is not None :
				if not self.HasPerms(object, 'Manage properties') :
					status = status - 1
				elif hasattr(object, 'hasProperty') :
					if object.hasProperty(property) :
						status = status + self.errormessage("Object %s already has property %s" % (self.ObjectPath(object), property))
					else :
						# in the following lines the absence of a _setProperty
						# attribute indicates an object without properties (e.g. a method)
						# which indicates an object for which setting properties is a nonsense
						if hasattr(object, "_setProperty") :
							object._setProperty(property, propvalue, proptype)
							self.htmlmessage("Property %s of type %s and value %s was added to object %s" % (property, proptype, str(propvalue), self.ObjectPath(object)))
		return status

	def run_delprop(self, expanded, unexpanded) :
		"""Deletes objects properties

		   Accepts a property name as its first argument.
		   Accepts multiple objects ids as its other arguments:

		   delprop MyProperty MyFolder/* *html
		"""   
		if len(expanded) < 2 :
			return self.errormessage("Needs at least a property name and one object id")

		property = expanded[0]
		status = 0
		for arg in expanded[1:] :
			object = self.toObject(self.__context, arg)
			if object is not None :
				if not self.HasPerms(object, 'Manage properties') :
					status = status - 1
				elif hasattr(object, 'hasProperty') :
					if not object.hasProperty(property) :
						status = status + self.errormessage("Object %s has no property %s" % (self.ObjectPath(object), property))
					else :
						# in the following lines the absence of a _delProperty
						# attribute indicates an object without properties (e.g. a method)
						# which indicates an object for which deleting properties is a nonsense
						if hasattr(object, "_delProperty") :
							object._delProperty(property)
							self.htmlmessage("Property %s deleted from object %s" % (property, self.ObjectPath(object)))
		return status

	def run_lsprop(self, expanded, unexpanded) :
		"""List objects properties

		   Accepts multiple arguments:

		   lsprop Contr?l_Pan*/Products/Sq* MyFolder/*

		   Caveats: Not sure that the result is correct wrt acquisition,
			    please report problems.
		"""
		if not expanded :
			return self.errormessage("Needs at least one object id")

		status = 0
		results = []
		for arg in expanded :
			object = self.toObject(self.__context, arg)
			if object is not None :
				if not self.HasPerms(object, 'Access contents information') :
					status = status - 1
				elif not hasattr(object, "propertyMap") :
					status = status + self.errormessage("Object %s doesn't have any property" % self.ObjectPath(object))
				else :
					# in the following lines the absence of an _updateProperty
					# attribute indicates an object without properties (e.g. a method)
					# which indicates an object for which listing properties is a nonsense
					if hasattr(object, "_updateProperty") :
						for prop in object.propertyMap() :
							propid = "%s.%s" % (object.getId(), prop["id"])
							proptype = prop["type"]
							propmode = prop.get("mode", "")
							propvalue = repr(object.getProperty(prop["id"], 'Error'))

							results.append({"Property": propid, "Type": proptype, "Value": propvalue, "Mode": propmode})
							self.printf("%s\n" % propid)
		self.tableDisplay("lsprop", ["Property", "Type", "Value", "Mode"], results)
		return status


def zshell(self, zshellscript=None, xmlrpcstuff=None) :
    # so we can check for the type of data coming in to see
    # if this being called by xmlrpc
    from types import DictType

    # ok we need to be a little more helpful in what we are passing through
    # xmlrpc doesnot allow key = value args, so we will pass through a
    # hash for the moment and sort it all out.
    r = None
    if type(xmlrpcstuff)==DictType:
	self.REQUEST['zshellscript'] = xmlrpcstuff['command']
	self.REQUEST['zshellpwd'] = xmlrpcstuff['path']
	r = xmlrpcstuff['result_type']

    MyShell = ZopeShell(self)

    # well we dont want to return html to command line,
    # plus if you do a cd, we want to know the path.
    # so lets pass this back in a dict that xml rpc knows how to marshal
    if r == 'text':
	output = { 'data':MyShell.get_stdout(), 'path':MyShell.getcwd() }
	return output
    else:
	return MyShell.get_HTML()
