# spansExtractor

Used libraries: csv, json, re

Known issues (in combination with FriPa csv file):
json 23148 29april (J298) - fixed symbol coding, more cases of corruption may appear in the csv file
json 25750 - corrupted json (no "text" body)
json 23265 does not exist - exists in FriPa 27May part 9
json 23271 does not exist - in FriPa 27May part 21
json 20866 15april (J317) - response_text does not correlate with the json
json 20887 15april (J320) - response_text is different from json
4March (E343) - extra resp_part removed from csv
