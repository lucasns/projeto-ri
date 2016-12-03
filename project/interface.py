from easygui import *
import numpy as np
import json

class Interface(object):
    def __init__(self, fields):
        self.fields = fields

    def _get_query_from_user(self):
        msg = "Search for Movies"
        title = "Search Engine Application"

        field_names = map(lambda s: s.capitalize(), self.fields)
        field_names = [x+' (Year)' if x=='Date' else x for x in field_names]

        #runtime = int(raw_input("Runtime:\n0 - 0-1 hr\n1 - 1-2 hr\n2 - 2-3 hr\n3 - More than 4 hr\n4 - ANY\n"))

        #if runtime >= 0 and runtime < 4:
        #    runtime = utils.MovieTime(runtime * 60 + 1).quartile()
        #else:
        #    runtime = ""

        field_values = multenterbox(msg, title, field_names)

        # make sure that none of the fields was left blank
        while True:
            if field_values == None:
                break

            errmsg = ""
            one_field_provided = False

            for i in range(len(field_names)):
              if field_values[i].strip() != "":
                one_field_provided = True
                break

            if one_field_provided:
                break # no problems found
            else:
                errmsg = "At least one field should be provided."

            field_values = multenterbox(errmsg, title, field_names, field_values)

        dict_list = zip(self.fields, field_values)
        result = dict(dict_list)

        return result

    def _show_retrieved_documents(self, documents_list):
        result = ""

        for document in documents_list:
            result = result + str(json.dumps(document, indent=1)) + "\n\n"

        result = result.replace('"', '').replace('{', '').replace('}', '')

        textbox(str(len(documents_list)) + " results", "Retrieved Documents", result)
