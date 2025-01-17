import json, unittest, datetime

with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)


def convertFromFormat1 (jsonObject):

    # IMPLEMENT: Conversion From Type 1
    # device information is in the same category as location
    # break down location (subcategories)
    # data is separate (create subcategories)
    # data is operationstatus and temp
    resultFromFormat1 = {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],
        "location": {},
        "data": {}
    }
    locationSplit = jsonObject["location"].split("/")
    resultFromFormat1["location"] ={
        "country": locationSplit[0],
        "city": locationSplit[1],
        "area": locationSplit[2],
        "factory": locationSplit[3],
        "section": locationSplit[4]
    }
    resultFromFormat1["data"] = {
        "status": jsonObject["operationStatus"],
        "temperature": jsonObject["temp"]
    }
    return resultFromFormat1


def convertFromFormat2 (jsonObject):

    # IMPLEMENT: Conversion From Type 1
    # convert to milliseconds
    # first part of data is separate ( id and device needs to be separated out)
    # create location category (already separated)
    dt = datetime.datetime.strptime(jsonObject["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
    new_timestamp = int(dt.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000)
    # new_timestamp = int(datetime.datetime.strptime(jsonObject["timestamp"],"%Y-%m-%dT%H:%M:%S.%fZ").timestamp() * 1000)
    resultFromFormat2 = {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": new_timestamp,
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"]
        },
        "data": {
            "status": jsonObject["data"]["status"],
            "temperature": jsonObject["data"]["temperature"]
        }
    }
    return resultFromFormat2


def main (jsonObject):

    result = {}

    if (jsonObject.get('device') == None):
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):

    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):

        result = main (jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):

        result = main (jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__':
    unittest.main()
