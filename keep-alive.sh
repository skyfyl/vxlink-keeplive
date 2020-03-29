#!/bin/bash
# author:kobe

echo "启动ss";
sslocal -s $1 -p $2 -l 1081 -k YjFkNDg0NW -m aes-256-cfb -d start

echo "server: $1";
echo "port: $2";

curl --socks5-hostname 127.0.1:1081 http://httpbin.org/ip
echo "查询iP";

sslocal -d stop
echo "停止ss";