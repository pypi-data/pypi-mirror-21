# Nautilus-python

Python SDK to help Developers for creating and accessing Nautilus API Model, It facilates user by providing sample interface for ease use of Maps APIs. 

#Code Structure <br />
NautilusPy/ <br />
  LocationHelper.py <br />
  TrackingHelper.py <br />
  core/ <br />
    Helper.py <br />
    HTTPInterface.py <br />
  <br />
LocationHelper helps you finding device location or track the path or getting nearby devices list. <br />
TrackingHelper helps you in assigning or releasing devices for tracking purposes. <br />

#Sample Path 
https://github.com/digitreck/nautilus-py-samples/ <br />

#json objects as param <br />
Dump Array without any whitespace and in sorted error <br />
jsonObj = json.dumps(dataDict, sort_keys=True, separators=(',', ':'))
