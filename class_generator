import json

def print_variable(v):
    print(v)

    if not isinstance(v, Variable):
        return ""
    return "    %s %s %s;" % (v.access,v.type, v.name)

def print_class(c):
    if not isinstance(c, Class):
        return ""

    variable_declarations = "";
    for v in c.variables:
        variable_declarations = "%s\n%s" % (variable_declarations, print_variable(v))

    return "public class %s {\n" \
           "" \
           "%s\n" \
           "" \
           "" \
           "\n}" \
        % (c.name, variable_declarations)


class Variable:
    def __init__(self, json):
        self.name = json["name"]
        self.type = json["type"]
        self.access = "private" if "access" not in json else json["access"]
        self.getter = "getter" not in json or json["getter"] == "true"
        self.setter = "setter" not in json or json["setter"] == "true"

    def __repr__(self):
        return "%s(name=%r, type=%r, access=%r, getter=%r, setter=%r)" \
               % (self.__class__.__name__,
                  self.name,
                  self.type,
                  self.access,
                  self.getter,
                  self.setter)

class Class:
    def __init__(self, json):
        self.name = json['name']
        self.variables = []

        if 'variables' in json:
            for v in json["variables"]:
                self.variables.append(Variable(v))

    def __repr__(self):
        return "%s(name=%r, variables=%s)" \
               % (self.__class__.__name__,
                  self.name,
                  self.variables)


def main():
    with open('example.json') as data_file:
        data = json.load(data_file)

    classes = []
    for c in data["classes"]:
        classes.append(Class(c))

    for c in classes:
        print(print_class(c))



if __name__ == "__main__":
    # execute only if run as a script
    main()