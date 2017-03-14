import json


def structure_variable(s):
    return s[0].upper() + s[1:]

def print_variable(v):
    if not isinstance(v, Variable):
        return ""
    return "    %s %s %s;" % (v.access, v.type, v.name)


def print_getter(v):
    if not isinstance(v, Variable):
        return ""

    return_string = "   public %s" % v.type
    if v.type == "boolean":
        return_string = " %s is%s() {\n " % (return_string, structure_variable(v.name))
    else:
        return_string = " %s get%s() {\n " % (return_string, structure_variable(v.name))

    return "%s        return this.%s;\n" \
        "    }\n" % (return_string, v.name)


def print_setter(v):
    if not isinstance(v, Variable):
        return ""
    return "    public void set%s(%s %s) {\n " \
           "        this.%s = %s; \n" \
           "    }\n" % (structure_variable(v.name), v.type, v.name,  v.name,  v.name)


def print_getter_and_setter(v):
    if not isinstance(v, Variable):
        return ""

    output = "%s" % (print_getter(v))
    if not v.read_only:
        output = "%s\n%s" % (output, print_setter(v))

    return output


def print_to_string(c):
    if not isinstance(c, Class):
        return ""

    return_string = "" \
        "    @Override\n" \
        "    public String toString() {\n" \
        "        return MoreObjects.toStringHelper(this)\n"

    for v in c.variables:
        return_string = "%s            .add(\"%s\", %s)\n" % (return_string, v.name, v.name)

    return "%s            .toString();\n" \
           "    }\n" % return_string


def print_equals_to(c):
    if not isinstance(c, Class):
        return ""

    return_string = "" \
        "    @Override\n" \
        "    public boolean equals(Object o) {\n" \
        "        if (this == o) return true;\n" \
        "        if (o == null || getClass() != o.getClass()) return false;\n\n" \
        "        %s castedObject = (%s) o;\n" % (c.name, c.name)

    # TODO add in variables types here-> Objects.equal(second, testOne.second);
    for v in c.variables:
        return_string = "%s" \
            "        if(%s != castedObject.%s) return false;\n" % (return_string, v.name, v.name)

    return "%s" \
           "        return true;\n" \
           "   }\n" % return_string


def print_hash_code(c):
    if not isinstance(c, Class):
        return ""

    variables = ""
    for v in c.variables:
        variables = "%s,%s" % (variables, v.name)

    return "" \
        "    @Override\n" \
        "    public int hashCode() {\n" \
        "        return Objects.hashCode(%s);\n" \
        "    }\n" % variables[1:]


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
           "%s\n" \
           "" \
           "%s\n" \
           "%s\n" \
           "%s\n" \
           "}" \
        % (c.name, variable_declarations,
           getter_and_setters, print_to_string(c), print_equals_to(c), print_hash_code(c))


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