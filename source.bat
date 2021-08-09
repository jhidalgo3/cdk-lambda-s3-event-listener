@echo off

rem The sole purpose of this script is to make the command
rem
rem     source PYTHON\bin/activate
rem
rem (which activates a Python virtualenv on Linux or Mac OS X) work on Windows.
rem On Windows, this command just runs this batch file (the argument is ignored).
rem
rem Now we don't need to document a Windows command for activating a virtualenv.

echo Executing PYTHON\Scripts\activate.bat for you
PYTHON\Scripts\activate.bat
