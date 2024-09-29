#!/bin/rbash
# author boyi.zhang
# ./deploy.sh start 启动
# ./deploy.sh stop 停止
# ./deploy.sh restart 重启
# ./deploy.sh start 状态
# bash deploy/deploy.sh start (linux启动)

AppName=xmind2testcasepro

if [ "$1" = "" ];
then
    echo -e "\033[0;31m 未输入操作名 \033[0m  \033[0;34m {start|stop|restart|status} \033[0m"
    exit 1
fi
PORT=1204
if [ x"$2" != x"" ];
then
    PORT=$2
fi
echo port:$PORT

function install_requirement() {
    echo "checkout out master:git clone https://github.com/goehls/xmind2testcasepro.git"
    git pull https://github.com/goehls/xmind2testcasepro.git
    echo "Env Configuration"
    if [ -d "venv/" ];then
      echo "skipped"
    else
      echo "create venv"
      python -m venv venv/
    fi
    . venv/bin/activate
    echo "install dependency..."
    pip install -r requirements.txt
}
#query(){
#  PID=`netstat -nlp | grep :$PORT | awk '{print $7}' | awk -F"/" '{ print $1 }'`
#  echo PID:$PID
#  return $PID
#}
function start() {
  install_requirement
  PID=`netstat -nlp | grep :$PORT | awk '{print $7}' | awk -F"/" '{ print $1 }'`
  echo "PID: $PID"
	if [ x"$PID" != x"" ]; then
	    echo "$AppName is running..."
	else
	  python -m webtool.application > logs/info.log 2>&1 &
		echo "Start $AppName success..."
	fi
}

function stop() {
    echo "Stop $AppName"

	PID=""
	query(){
		PID=`netstat -nlpp | grep :$PORT | awk '{print $7}' | awk -F"/" '{ print $1 }'`
		echo PID:$PID
	}

	query
	if [ x"$PID" != x"" ]; then
		kill -TERM $PID
		echo "$AppName (pid:$PID) exiting..."
		while [ x"$PID" != x"" ]
		do
			sleep 1
			query
		done
		echo "$AppName exited."
	else
		echo "$AppName already stopped."
	fi
}

function restart() {
    stop
    sleep 2
    start
}

function status() {
    PID=`netstat -nlp | grep :$PORT | awk '{print $7}' | awk -F"/" '{ print $1 }'`
    echo "PID: $PID"
    if [ x"$PID" != x"" ]; then
        echo "$AppName is running..."
    else
        echo "$AppName is not running..."
    fi
}

case $1 in
    start)
    start;;
    stop)
    stop;;
    restart)
    restart;;
    status)
    status;;
    *)

esac
