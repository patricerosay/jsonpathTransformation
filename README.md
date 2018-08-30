# jsonpath transformation

This script is based on [jsonpath_ng](https://github.com/h2non/jsonpath-ng)


## Use it to transform a file
This json to json transformation script transforms one json into a second json, using a third json file that contains the mapping and the structure of the desired third json.

```
jpt -i input.json -t transfo.json -o output.json
input.json
{
    "creationDate": "2018-05-29T12:41:08,306+02:00",
    "id": "7edb06eb-2298-34b9-a9f5-cf47f645a6b6", 
    "smartdata":
    {
        "producer": "r2d2"
    }
    "versionSchema": "null"
}
transfo.json
{
    "data": 
        {
            "uuid": "$.id",
            "producer": "$.smartData.producer"
        }
}
```
will generate the file:

```
output.json
{
    "data": 
        {
            "uuid": "7edb06eb-2298-34b9-a9f5-cf47f645a6b6", 
            "producer": "r2d2"
        }
} 
```
## Use it to check your jsonpath syntax
Executing the command line
```
jpe -i input.json -e $.smartData.producer
```
will return
```
r2d2
