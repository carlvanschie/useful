import json


def print_variable(v):
    print(v)

    if not isinstance(v, Variable):
        return ""
    return "    %s %s %s;" % (v.access,v.type, v.name)


def print_getter(v):
    if not isinstance(v, Variable):
        return ""
    return "    public %s get%s() {\n " \
           "        return %s; \n" \
           "    }\n" % (v.type, v.name.title(), v.name)


def print_setter(v):
    if not isinstance(v, Variable):
        return ""
    return "    public void set%s(%s %s) {\n " \
           "        %s = %s; \n" \
           "    }\n" % (v.name.title(), v.type, v.name,  v.name,  v.name)


def print_getter_and_setter(v):
    output = "%s" % (print_getter(v))

    if not v.read_only:
        output = "%s\n%s" % (output, print_setter(v))

    return output


def print_class(c):
    if not isinstance(c, Class):
        return ""

    variable_declarations = ""
    getter_and_setters = ""
    for v in c.variables:
        variable_declarations = "%s\n%s" % (variable_declarations, print_variable(v))
        getter_and_setters = "%s\n%s" % (getter_and_setters, print_getter_and_setter(v))

    return "public class %s {\n" \
           "" \
           "%s\n" \
           "%s" \
           "" \
           "\n}" \
        % (c.name, variable_declarations, getter_and_setters)


class Variable:
    def __init__(self, json):
        self.name = json["name"]
        self.type = json["type"]
        self.access = "private" if "access" not in json else json["access"]
        self.read_only = False if "read_only" not in json or json["read_only"] == "false" else True

    def __repr__(self):
        return "%s(name=%r, type=%r, access=%r, readOnly=%r)" \
               % (self.__class__.__name__,
                  self.name,
                  self.type,
                  self.access,
                  self.read_only)

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
    main()