-- lo.hs -- low-level CGI program

import System.Environment (getEnvironment)

main = 
    putStrLn "Content-type: text/plain\n"
    >>  getEnvironment
    >>= mapM_ printPair
    
printPair (name, value) = putStrLn $ name ++ " = " ++ value

{-  In GHCI:

    Content-type: text/plain

    USER = oak
    LANGUAGE = ru:zh_CN:en
    SSH_AGENT_PID = 1402
    SHLVL = 1
    HOME = /home/oak
    XDG_SESSION_COOKIE = e9bf5672c6670a3cf42c634500000008-1352353956.626045-854827338
    DESKTOP_SESSION = gnome-shell
    GTK_MODULES = canberra-gtk-module:canberra-gtk-module
    XDG_SEAT_PATH = /org/freedesktop/DisplayManager/Seat0
    LC_CTYPE = ru_RU.UTF-8
    DBUS_SESSION_BUS_ADDRESS = unix:abstract=/tmp/dbus-ApO3y91h9J,guid=75614cc12dcad96e69f4b37c00000012
    COLORTERM = gnome-terminal
    GNOME_KEYRING_CONTROL = /tmp/keyring-198Y10
    MANDATORY_PATH = /usr/share/gconf/gnome-shell.mandatory.path
    LOGNAME = oak
    WINDOWID = 35651590
    _ = /usr/bin/ghci
    DEFAULTS_PATH = /usr/share/gconf/gnome-shell.default.path
    TERM = xterm
    USERNAME = oak
    GNOME_DESKTOP_SESSION_ID = this-is-deprecated
    LC_COLLATE = ru_RU.UTF-8
    SESSION_MANAGER = local/oak:@/tmp/.ICE-unix/1344,unix/oak:/tmp/.ICE-unix/1344
    PATH = /usr/lib/lightdm/lightdm:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games
    XDG_SESSION_PATH = /org/freedesktop/DisplayManager/Session0
    DISPLAY = :0.0
    LANG = ru_RU.UTF-8
    XDG_CURRENT_DESKTOP = GNOME
    XAUTHORITY = /home/oak/.Xauthority
    SSH_AUTH_SOCK = /tmp/keyring-198Y10/ssh
    LC_MESSAGES = ru_RU.UTF-8
    SHELL = /bin/bash
    GDMSESSION = gnome-shell
    GPG_AGENT_INFO = /tmp/keyring-198Y10/gpg:0:1
    PWD = /home/oak/Projects/BMSTU/FP course 2012/11 fp/2 cgi
    XDG_CONFIG_DIRS = /etc/xdg/xdg-gnome-shell:/etc/xdg
    XDG_DATA_DIRS = /usr/share/gnome-shell:/usr/share/gnome:/usr/local/share/:/usr/share/

--  Via CGI (1):
    
    HTTP_HOST = debug
    HTTP_CONNECTION = keep-alive
    HTTP_USER_AGENT = Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11
    HTTP_ACCEPT = text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    HTTP_ACCEPT_ENCODING = gzip,deflate,sdch
    HTTP_ACCEPT_LANGUAGE = ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4
    HTTP_ACCEPT_CHARSET = windows-1251,utf-8;q=0.7,*;q=0.3
    PATH = /usr/local/bin:/usr/bin:/bin
    SERVER_SIGNATURE = <address>Apache/2.2.20 (Ubuntu) Server at debug Port 80</address>

    SERVER_SOFTWARE = Apache/2.2.20 (Ubuntu)
    SERVER_NAME = debug
    SERVER_ADDR = 127.0.0.1
    SERVER_PORT = 80
    REMOTE_ADDR = 127.0.0.1
    DOCUMENT_ROOT = /home/oak/Sites/debug/www
    SERVER_ADMIN = webmaster@localhost
    SCRIPT_FILENAME = /home/oak/Sites/debug/cgi-bin/lo
    REMOTE_PORT = 54850
    GATEWAY_INTERFACE = CGI/1.1
    SERVER_PROTOCOL = HTTP/1.1
!!  REQUEST_METHOD = GET
!!  QUERY_STRING = 
    REQUEST_URI = /cgi-bin/lo
    SCRIPT_NAME = /cgi-bin/lo
    
--  Via CGI (2):
    
    REQUEST_METHOD = GET
    QUERY_STRING = name1=value1&name2=value2
    REQUEST_URI = /cgi-bin/lo?name1=value1&name2=value2
    SCRIPT_NAME = /cgi-bin/lo
    
--  From forms.html, GET method:

    ...
    REQUEST_METHOD = GET
    QUERY_STRING = t=the+text&r=on&b2=on&h=hidden+text&s=Option+2
    
--  From forms.html, POST method:

    ...
    REQUEST_METHOD = POST
    QUERY_STRING =
    ...
    CONTENT_LENGTH = 3691
-}
