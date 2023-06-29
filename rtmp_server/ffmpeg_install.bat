@echo off

echo FFmpeg Installer for Windows
echo -----------------------------
echo.
echo This script will download and install FFmpeg on your computer.
echo.

:askInstall
set /P "userInput=Do you want to continue with the installation? (Y/N): "
if /I "%userInput%"=="Y" goto :download
if /I "%userInput%"=="N" goto :exitScript
echo Invalid input. Please answer with 'Y' or 'N'.
goto askInstall

:download
echo Downloading FFmpeg...
powershell.exe -Command "Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z' -OutFile 'ffmpeg-git-essentials.7z'"
echo Download complete.

:extract
echo Extracting FFmpeg...
powershell.exe -Command "& {Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::ExtractToDirectory('ffmpeg-git-essentials.7z', '.\ffmpeg')}"
echo Extraction successful.

:addPath
echo Adding FFmpeg to the system Path variable...
setx PATH "%PATH%;%CD%\ffmpeg\bin"
echo Added FFmpeg to the system Path.

:done
echo FFmpeg Installation is complete.
echo.
echo Note: You might need to restart your Command Prompt or PowerShell sessions to have FFmpeg available as a command.
goto exitScript

:exitScript
pause
exit