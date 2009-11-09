REM
REM UrbanSim software. Copyright (C) 1998-2004 University of Washington
REM 
REM You can redistribute this program and/or modify it under the terms of the
REM GNU General Public License as published by the Free Software Foundation
REM (http://www.gnu.org/copyleft/gpl.html).
REM 
REM This program is distributed in the hope that it will be useful, but WITHOUT
REM ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
REM FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
REM and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
REM other acknowledgments.
REM 

@echo off
for %%e in (*.rpt) do (
	echo %%e
	for /F "tokens=*" %%f in (%%e) do (
		for %%g in (%%f) do (
			if %%g==NaN (
				echo %%g in %%e at "%%f"
				exit /B 1
			)
		)	
	)
)
exit /B 0