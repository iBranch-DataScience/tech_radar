
pid=$(ps aux | grep '[R]adar.py'| awk '{print $2}')

if [ -z "$pid" ]
then
  echo "Scraping server is not running!"
else
  kill $pid
echo "Shutdown complete: PID: $pid"
fi
