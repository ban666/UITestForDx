@REM @Author: anchen
@REM @Date:   2016-11-08 10:20:45
@REM @Last Modified by:   anchen
@REM Modified time: 2016-11-08 10:21:12


@echo off
setlocal enabledelayedexpansion
rem %1传入端口号
for /f "delims=  tokens=1" %%i in ('netstat -aon ^| findstr %1 ') do (
set a=%%i
goto js
)
:js
taskkill /f /pid "!a:~71,5!"
rem pause>nul