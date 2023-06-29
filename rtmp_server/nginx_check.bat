@echo off

set "nginx_installed_flag=0"
cd 
echo Checking for Nginx installation...
if exist ".\\rtmp_server\\nginx-rtmp-win32\\nginx.exe" (
    echo Nginx is installed.
    set "nginx_installed_flag=1"
) else (
    echo Nginx is not installed.
)

:: Exit the script if Nginx is not installed
if "%nginx_installed_flag%"=="0" (
    echo Nginx is not installed, exiting with code 2.
    exit /b 2
)

:: Continue with the original script if Nginx is installed
set "nginx_running_flag=0"

tasklist /FI "IMAGENAME eq nginx.exe" 2>NUL | find /I /N "nginx.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Nginx is already running.
    set "nginx_running_flag=1"
    exit /b 1
) else (
    echo Nginx is not running. Attempting to start...
    cd rtmp_server
    cd nginx-rtmp-win32
    start nginx.exe
    timeout /t 5 /nobreak > NUL

    tasklist /FI "IMAGENAME eq nginx.exe" 2>NUL | find /I /N "nginx.exe">NUL
    if "%ERRORLEVEL%"=="0" (
        echo Nginx started successfully.
        set "nginx_running_flag=1"
        exit /b 1
    ) else (
        echo Error: Failed to start Nginx.
        exit /b 0
    )
)

:: The value of 'nginx_running_flag' is used as an indicator for success or error
:: '1' indicates success, and '0' denotes an error
echo nginx_running_flag: %nginx_running_flag%

:: The following line demonstrates how to use the 'nginx_running_flag' to execute further actions in the batch script
if "%nginx_running_flag%"=="1" (
    echo Further actions for successful Nginx execution can be placed here.
) else (
    echo Further actions for failed Nginx execution can be placed here.
)