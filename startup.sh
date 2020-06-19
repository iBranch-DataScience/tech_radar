## Startup script ##
param=$@

found_cfg=false

for var in "$@"
  do
    if [[ "$var" == *"cfg_path"* ]]
    then
        echo "Found"
        found_cfg=true
    fi
  done

if [ "$found_cfg" = false ]
then
  param="${param} -cfg_path resource/property/properties.yaml"
fi
msg='Start scraping'
startup_cmd="nohup python Radar.py $param >/dev/null 2>&1 &"
eval $startup_cmd
echo "$msg: PID: $!"