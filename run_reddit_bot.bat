@REM This simple Batch file is to make running the bot easier on Windows.
@echo off

@REM The program is executed, it will run this command in the command line.
:start_marker
python reddit_notification_bot.py %*

echo Process stopped. Close command prompt? (y/n)
set/p restart=
if %restart%==n goto start_marker
if %restart%==y goto terminate_marker

:terminate_marker
exit