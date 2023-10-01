import csv
import json
import re


def extract_node_ids(s):
    pattern = r'id="node(\d+_\d+)"'
    matches = re.findall(pattern, s)
    return matches


def find_indexes(lst, target, current_indexes=[]):
    indexes = []
    for index, item in enumerate(lst):
        if isinstance(item, list):
            # If the item is a sublist, recursively call the function
            sub_indexes = find_indexes(item, target, current_indexes + [index])
            indexes.extend(sub_indexes)
        elif item.lower() == target:
            # If the item is the target string, add the current index
            indexes.append(current_indexes[-1])
    return list(set(indexes))


#  Read CSV file
with open("FriPa_new.csv") as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')
    csv_FriPa = [row for row in reader]
    fripa_rows = list(reader)

with open("qt30.csv") as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')
    csv_qt30 = [row for row in reader]

for i in csv_FriPa[1:]:  # first two rows are examples (20.08.2023)
    date_fripa = "cutietestrun" + i[0].lower()
    date_fripa_s = "cutiestestrun" + i[0].lower()  # used to search for appearances named with S
    response_part = i[4]
    response_text = i[9]
    response_json_ID = ""
    # looking for corpus in qt30 map
    date_indexes_qt30 = find_indexes(csv_qt30, date_fripa)
    # some of the rows have cutieStestrun in them. Next line calls a function again in that case
    if not date_indexes_qt30:
        date_indexes_qt30 = find_indexes(csv_qt30, date_fripa_s)
    for d in date_indexes_qt30:
        # search for json_ids using parts for answers
        if (csv_qt30[d][9] == response_part or csv_qt30[d][9] == "part " + response_part) and response_part != "":
            if len(csv_qt30[d][11]) <= 6:  # there are texts instead of corpus numbers sometimes in the column
                json_corpus = csv_qt30[d][11]
                print("Corpus: " + json_corpus)
                response_json_ID = json_corpus  # writing to outer scope
                try:
                    with open("jsons/" + json_corpus + ".json", encoding='utf-8-sig') as f:
                        json_data = json.load(f)
                except FileNotFoundError:
                    print("File " + json_corpus + " does not exist.")
                json_text = json_data["text"]
                node_list = extract_node_ids(json_text)  # extracted all nodes referring to text
                relevant_nodes = []
                for node in json_data["AIF"]["nodes"]:
                    if node["nodeID"] in node_list:
                        regex = re.findall(r'^(?:[^:]*:)?\s*(?:[^:]*:)?\s*(.+)$', node["text"])[0]
                        # the RegEx will look for the text after a colon, so that the name of the speaker is omited
                        # in some instances this will skip some of the text before the colon, but that should not pose an issue
                        if len(regex.split()) > 3:
                            regex = regex.split(' ', 1)[1]
                        if regex in response_text:
                            relevant_nodes.append(node["nodeID"])
                i[11] = str(relevant_nodes)

with open('FriPa_new_dub.csv', 'w', encoding='utf-8') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerows(csv_FriPa)
