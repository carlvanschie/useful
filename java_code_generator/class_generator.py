"""
Module doc string to be done.
"""
from __future__ import print_function
import json

PRIMITIVES = ['long', 'int', 'short', 'byte',
              'float', 'double', 'boolean', 'char']


def uppercase_first_letter(string):
    """
    or the given string return the same string but with the
    first letter converted to upper case.
    :param string: String to work on
    :return: String with a first letter as upper case.
    """
    return string[0].upper() + string[1:]


def print_variable_declaration(variable):
    """
    For a given Variable return the java deceleration text.
    :param variable: Variable to work on, must be of type Variable
    :return: The definition string for this variable in a class, "" if not a
    Variable type.
    """
    if not isinstance(variable, Variable):
        return ""
    return "    %s %s %s;" % (variable.access, variable.type, variable.name)


def print_getter(variable):
    """
    For a given variable return the getter java text.
    :param variable: Variable Of which to create the getter text for.
    :return: String getter text, "" if not Variable type
    """
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
    """
    For a given variable return the setter java text.
    :param variable: Variable Of which to create the setter text for.
    :return: String setter text, "" if not Variable type
    """
    if not isinstance(variable, Variable):
        return ""
    return "    public void set%s(%s %s) {\n " \
           "        this.%s = %s; \n" \
           "    }\n" \
           % (uppercase_first_letter(variable.name), variable.type,
              variable.name, variable.name, variable.name)


def print_getter_and_setter(variable):
    """
    For a given variable return the getter and setter java text.
    :param variable: Variable of which to create the getter and setter text for.
    :return: String getter and setter text, "" if not Variable type.
    """
    if not isinstance(variable, Variable):
        return ""

    output = "%s" % (print_getter(variable))
    if not variable.read_only:
        output = "%s\n%s" % (output, print_setter(variable))

    return output


def print_class_to_string(current_class):
    """
    For a given Class type, create the java toString text.
    :param current_class: Class type which to write the toString for.
    :return: String toString java text, "" if not Class type.
    """
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


def print_class_equals_to(current_class):
    """
    For a given Class type, create the java equalsTo text.
    :param current_class: Class type which to write the equals to for
    :return: String equals to java text, "" if not Class type.
    """
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


def print_class_hash_code(current_class):
    """
    For a given Class type, create the java hasCode text.
    :param current_class: Class type which to write the hashCode for
    :return: String hashCode to java text, "" if not Class type.
    """
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
    """
    For a given Class type, create the java class text.
    :param current_class: Class type which to write the class for
    :return: String class code java text, "" if not Class type.
    """
    if not isinstance(current_class, Class):
        return ""

    variable_declarations = ""
    getter_and_setters = ""
    for variable in current_class.variables:
        variable_declarations = "%s\n%s" \
                                % (variable_declarations,
                                   print_variable_declaration(variable))
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
              print_class_to_string(current_class),
              print_class_equals_to(current_class),
              print_class_hash_code(current_class))


class Variable(object):
    """
    Variable Class used to describe a class variable.
    """
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
    """
    Class Class used to describe a class.
    """
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
    """
    Used to take a given json file to describe java classes and generate the
    Java code.
    :return: main methord stuff.
    """
    with open('example.json') as data_file:
        data = json.load(data_file)

    classes = []
    for class_json in data["classes"]:
        classes.append(Class(class_json))

    for class_json in classes:
        print(print_class(class_json))


if __name__ == "__main__":
    main()