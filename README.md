# THE CITIES APP

The Cities App is part of a portfolio suite featured on <a href="https://mikehyland.com" target="_blank">mikehyland.com</a>

This basic app is an exercise in API consumption based on geo-location and user search criteria. The following API's are consumed in order to display city information:

* <a href="https://ipstack.com/" target="_blank">IP Stack API</a>
* <a href="https://developers.teleport.org/api/" target="_blank">Teleport Public API</a>
* <a href="https://www.countryflags.io/" target="_blank">Country Flags API</a>
* <a href="https://opentripmap.io/product/" target="_blank">Open Trip Map API</a>
* <a href="https://home.openweathermap.org/" target="_blank">Open Weather API</a>
* <a href="https://developer.here.com/" target="_blank">Developer Here API</a>
* <a href="https://pypi.org/project/Wikipedia-API/" target="_blank">Wikipedia API</a>

Since the app uses free and open API's, the data cannot be consistenlty verified. In the majority of searches, data is correct but users may find that some searches, mainly from the Open Trip Map API, may show inconsistent results.

Where data cannot be gathered, the app will error handle these scenarios depending on the nature of the data that cannot be gathered.

## Requirements

1. Python 3
2. Flask Web Framework
3. API Keys for :
 * <a href="https://ipstack.com/" target="_blank">IP Stack API</a>
 * <a href="https://home.openweathermap.org/" target="_blank">Open Weather API</a>
 * <a href="https://opentripmap.io/product/" target="_blank">Open Trip Map API</a>
 * <a href="https://developer.here.com/" target="_blank">Developer Here API</a>

## Config File for API Keys

Place a config file called config.json in the config directory with the following json:
<br>
`
{
  "api_keys": {
    "ipstack": "XXXX",
    "openweathermap": "XXXX",
    "opentripmap": "XXXX"
  }
}
`
<br>
Add the corresponding API keys. 
