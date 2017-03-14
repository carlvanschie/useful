from __future__ import print_function
import json

PRIMITIVES = ['long', 'int', 'short', 'byte',
              'float', 'double', 'boolean', 'char']


def uppercase_first_letter(string):
    return string[0].upper() + string[1:]


def print_variable(variable):
    if not isinstance(variable, Variable):
        return ""
    return "    %s %s %s;" % (variable.access, variable.type, variable.name)


def print_getter(variable):
    if not isinstance(variable, Variable):
        return ""

    return_string = "   public %s" % variable.type
    if variable.type == "boolean":
        return_string = " %s is%s() {\n " \
                        % (return_string, uppercase_first_letter(variable.name))
    else:
        return_string = " %s get%s() {\n " \
                        % (return_string, uppercase_first_letter(variable.name))

    return "%s        return this.%s;\n" \
           "    }\n" % (return_string, variable.name)


def print_setter(variable):
    if not isinstance(variable, Variable):
        return ""
    return "    public void set%s(%s %s) {\n " \
           "        this.%s = %s; \n" \
           "    }\n" \
           % (uppercase_first_letter(variable.name), variable.type,
              variable.name, variable.name, variable.name)


def print_getter_and_setter(variable):
    if not isinstance(variable, Variable):
        return ""

    output = "%s" % (print_getter(variable))
    if not variable.read_only:
        output = "%s\n%s" % (output, print_setter(variable))

    return output


def print_to_string(current_class):
    if not isinstance(current_class, Class):
        return ""

    return_string = "" \
        "    @Override\n" \
        "    public String toString() {\n" \
        "        return MoreObjects.toStringHelper(this)\n"

    for variable in current_class.variables:
        return_string = "%s" \
            "            .add(\"%s\", %s)\n" \
                        % (return_string, variable.name, variable.name)

    return "%s            .toString();\n" \
           "    }\n" % return_string


def print_equals_to(current_class):
    if not isinstance(current_class, Class):
        return ""

    return_string = "" \
        "    @Override\n" \
        "    public boolean equals(Object o) {\n" \
        "        if (this == o) return true;\n" \
        "        if (o == null || getClass() != o.getClass()) " \
                    "return false;\n\n" \
        "        %s castedObject = (%s) o;\n" \
                    % (current_class.name, current_class.name)

    for variable in current_class.variables:
        if variable.type in PRIMITIVES:
            return_string = "%s" \
                            "        if(%s != castedObject.%s) " \
                            "return false;\n" \
                            % (return_string, variable.name, variable.name)
        else:
            return_string = "%s" \
                            "        if(!Objects.equal(%s, castedObject.%s)) " \
                            "return false;\n" \
                            % (return_string, variable.name, variable.name)

    return "%s" \
           "        return true;\n" \
           "   }\n" % return_string


def print_hash_code(current_class):
    if not isinstance(current_class, Class):
        return ""

    variables = ""
    for variable in current_class.variables:
        variables = "%s,%s" % (variables, variable.name)

    return "" \
           "    @Override\n" \
           "    public int hashCode() {\n" \
           "        return Objects.hashCode(%s);\n" \
           "    }\n" % variables[1:]


def print_class(current_class):
    if not isinstance(current_class, Class):
        return ""

    variable_declarations = ""
    getter_and_setters = ""
    for variable in current_class.variables:
        variable_declarations = "%s\n%s" \
                                % (variable_declarations,
                                   print_variable(variable))
        getter_and_setters = "%s\n%s" \
                             % (getter_and_setters,
                                print_getter_and_setter(variable))

    return "public class %s {\n" \
           "" \
           "%s\n" \
           "%s\n" \
           "" \
           "%s\n" \
           "%s\n" \
           "%s\n" \
           "}" \
           % (current_class.name, variable_declarations, getter_and_setters,
              print_to_string(current_class), print_equals_to(current_class),
              print_hash_code(current_class))


class Variable(object):
    def __init__(self, input_json):
        self.name = input_json["name"]
        self.type = input_json["type"]
        self.access = "private" \
            if "access" not in input_json \
            else input_json["access"]
        self.read_only = False \
            if "read_only" not in input_json \
               or input_json["read_only"] == "false" \
            else True

    def __repr__(self):
        return "%s(name=%r, type=%r, access=%r, readOnly=%r)" \
               % (self.__class__.__name__,
                  self.name,
                  self.type,
                  self.access,
                  self.read_only)


class Class(object):
    def __init__(self, input_json):
        self.name = input_json['name']
        self.variables = []

        if 'variables' in input_json:
            for variable_json in input_json["variables"]:
                self.variables.append(Variable(variable_json))

    def __repr__(self):
        return "%s(name=%r, variables=%s)" \
               % (self.__class__.__name__,
                  self.name,
                  self.variables)


def main():
    with open('example.json') as data_file:
        data = json.load(data_file)

    classes = []
    for class_json in data["classes"]:
        classes.append(Class(class_json))

    for class_json in classes:
        print(print_class(class_json))


if __name__ == "__main__":
    main()