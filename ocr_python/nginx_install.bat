@echo off
echo Setting up Nginx with RTMP Server...
powershell.exe -Command "Invoke-WebRequest -Uri 'https://github.com/illuspas/nginx-rtmp-win32/archive/refs/heads/master.zip' -OutFile 'nginx-rtmp-win32.zip'"
powershell.exe -Command "Expand-Archive -Path 'nginx-rtmp-win32.zip' -DestinationPath '.'"
move nginx-rtmp-win32-master nginx-rtmp-win32
copy nginx-rtmp-win32\conf\nginx.conf nginx-rtmp-win32\conf\nginx.conf.bak

(
echo worker_processes  1;
echo;
echo error_log  logs/error.log info;
echo;
echo events {
echo     worker_connections  1024;
echo }
echo;
echo rtmp {
echo     server {
echo         listen 1935;
echo;
echo         application live {
echo             live on;
echo         }
echo;
echo         application hls {
echo             live on;
echo             hls on;
echo             hls_path temp/hls;
echo             hls_fragment 8s;
echo         }
echo     }
echo }
echo;
echo http {
echo     server {
echo         listen      8080;
echo;
echo         location / {
echo             root html;
echo         }
echo;
echo         location /stat {
echo             rtmp_stat all;
echo             rtmp_stat_stylesheet stat.xsl;
echo         }
echo;
echo         location /stat.xsl {
echo             root html;
echo         }
echo;
echo         location /hls {
echo             types {
echo                 application/vnd.apple.mpegurl m3u8;
echo                 video/mp2t ts;
echo             }
echo             alias temp/hls;
echo             expires -1;
echo         }
echo     }
echo }
) > nginx-rtmp-win32\conf\nginx.conf

echo Run Nginx with RTMP server and wait for any output or error messages.
echo Press any key to continue.
pause>nul
cd nginx-rtmp-win32
nginx.exe
pause