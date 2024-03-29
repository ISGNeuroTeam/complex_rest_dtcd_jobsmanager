import re


# Class with actions for parsing OTL expression to SQL

class BaseEvalExpressions:
    def __init__(self, indices_list, fields_list):
        self.indices_list = indices_list
        self.fields_list = fields_list

    def otl_preprocess_request(self, otl):
        """Transforms all logical expressions to upper case.
        Replaces whitespaces with logical AND.

        :param otl: input OTL string
        :return: preprocessed OTL string

        """

        otl = self.otl_replace_case(otl)
        otl = self.otl_replace_ws_with_and(otl)
        return otl

    def otl_replace_case(self, otl):
        """Transforms all logical expressions to upper case

        :param otl: input OTL string
        :return: preprocessed OTL string

        """
        operators = ["NOT", "OR", "AND"]
        result = ''
        otl_list = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', otl)
        for index in range(0, len(otl_list)):
            if otl_list[index].upper() in operators:
                result = result + otl_list[index].upper() + ' '
            else:
                result = result + otl_list[index] + ' '
        return result

    def otl_replace_ws_with_and(self, otl):
        """ Replaces whitespaces with logical AND

        :param otl: input OTL string
        :return: preprocessed OTL string

        """

        operators = ["NOT", "OR", "AND"]
        result = ''
        otl_list = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', otl)
        for index in range(0, len(otl_list) - 1):
            if (otl_list[index][-1:] == ')') and (otl_list[index + 1][:1] == '('):
                result = result + otl_list[index] + ' AND '
            elif ((otl_list[index].replace('(', '').replace(')', '').upper() not in operators) and
                  (otl_list[index + 1].replace('(', '').replace(')', '').upper() not in operators)):
                result = result + otl_list[index] + ' AND '
            else:
                result = result + otl_list[index] + ' '
        result = result + otl_list[-1]
        return result

    def remove_index(self, _context, nodes):
        """Removes indices from OTL request and save index contents in self.indices_list

        :param _context: An object used to keep parser context info
        :param nodes: Nodes of the parse tree on this iteration
        :return: None

        """

        if len(nodes) == 2:
            index_string = nodes[1].replace('"', '').replace("'", '')
            self.indices_list.insert(0, index_string)
        if len(nodes) == 4:
            index_string = nodes[2].replace('"', '').replace("'", '')
            self.indices_list.insert(0, index_string)
        return

    def transform_equal(self, _context, nodes):
        """Transforms equal expressions from OTL format to SQL format

        :param _context: An object used to keep parser context info
        :param nodes: Nodes of the parse tree on this iteration
        :return: Transformed equal expression

        """

        if nodes[0] in self.fields_list:
            pass
        else:
            self.fields_list.insert(0, nodes[0])

        if len(nodes) == 5:
            result = nodes[0] + '=' + nodes[2] + nodes[3] + nodes[4]
            return result

        result = ''
        if nodes[2].find('*') >= 0:
            result = "(" + nodes[0] + ' rlike \'' + nodes[2] + '\')'
            pos = result.rfind('*')
            while pos >= 0:
                result = result[:pos] + '.' + result[pos:]
                pos = result[:pos].rfind('*')
        elif nodes[2] == '':
            result = nodes[0] + '=""'
        elif (nodes[2][:1] == '"') and (nodes[2][-1:] == '"'):
            result = nodes[0] + '=' + nodes[2]
        else:
            result = nodes[0] + "=\"" + nodes[2] + "\""
        return result

    def transform_not_equal(self, _context, nodes):
        """Transforms not equal expressions from OTL format to SQL format

        :param _context: An object used to keep parser context info
        :param nodes: Nodes of the parse tree on this iteration
        :return: Transformed not equal expression

        """

        if nodes[0] in self.fields_list:
            pass
        else:
            self.fields_list.insert(0, nodes[0])

        result = ''
        if len(nodes) == 5:
            result = '!(' + nodes[0] + '=' + nodes[2] + nodes[3] + nodes[4] + ')'
            return result

        if nodes[2].find('*') >= 0:
            result = "!(" + nodes[0] + ' rlike \'' + nodes[2] + '\')'
            pos = result.rfind('*')
            while pos >= 0:
                result = result[:pos] + '.' + result[pos:]
                pos = result[:pos].rfind('*')
        elif nodes[2] == '':
            result = '!(' + nodes[0] + '="")'
        elif (nodes[2][:1] == '"') and (nodes[2][-1:] == '"'):
            result = '!(' + nodes[0] + '=' + nodes[2] + ')'
        else:
            result = '!(' + nodes[0] + "=\"" + nodes[2] + "\"" + ')'
        return result

    def transform_and(self, _context, nodes):
        """Transforms AND expressions from OTL format to SQL format

        :param _context: An object used to keep parser context info
        :param nodes: Nodes of the parse tree on this iteration
        :return: Transformed AND expression

        """

        if nodes[0] is None:
            return nodes[2]
        elif nodes[2] is None:
            return nodes[0]
        else:
            return nodes[0] + " AND " + nodes[2]

    def transform_or(self, _context, nodes):
        """Transforms OR expressions from OTL format to SQL format

        :param _context: An object used to keep parser context info
        :param nodes: Nodes of the parse tree on this iteration
        :return: Transformed OR expression

        """

        if nodes[0] is None:
            return nodes[2]
        elif nodes[2] is None:
            return nodes[0]
        else:
            return nodes[0] + " OR " + nodes[2]

    def transform_not(self, _context, nodes):
        """Transforms NOT expressions from OTL format to SQL format

        :param _context: An object used to keep parser context info
        :param nodes: Nodes of the parse tree on this iteration
        :return: Transformed NOT expression

        """

        if nodes[1][:1] == '!':
            return nodes[1][1:]

        if nodes[1].startswith('('):
            return "!" + nodes[1]

        return "!(" + nodes[1] + ")"

    def transform_comparison(self, _context, nodes):
        """Transforms compare expressions from OTL format to SQL format

        :param _context: An object used to keep parser context info
        :param nodes: Nodes of the parse tree on this iteration
        :return: Transformed compare expression

        """

        if nodes[0] in self.fields_list:
            pass
        else:
            self.fields_list.insert(0, nodes[0])

        return nodes[0] + nodes[1] + nodes[2]

    def transform_quotes(self, _context, nodes):
        """Transforms quoted expressions from OTL format to SQL format

        :param _context: An object used to keep parser context info
        :param nodes: Nodes of the parse tree on this iteration
        :return: Transformed quoted expression

        """

        return '(_raw rlike \'' + nodes[1] + '\')'

    def transform_brackets(self, _context, nodes):
        """Transforms expressions with brackets from OTL format to SQL format

        :param _context: An object used to keep parser context info
        :param nodes: Nodes of the parse tree on this iteration
        :return: Transformed brackets expression

        """

        return "(" + nodes[1] + ")"

    def transform_comma(self, _context, nodes):
        """Transforms expressions with comma from OTL format to SQL format

        :param _context: An object used to keep parser context info
        :param nodes: Nodes of the parse tree on this iteration
        :return: Transformed comma expression

        """

        if nodes[0] is None:
            return nodes[2]
        elif nodes[2] is None:
            return nodes[0]
        else:
            return nodes[0] + " AND " + nodes[2]

    def return_value(self, _context, nodes):
        """Transforms value with optional regular expression to OTL format

        :param _context: An object used to keep parser context info
        :param nodes: Nodes of the parse tree on this iteration
        :return: Terminal value, optionally with quotes

        """

        if len(nodes) == 0:
            return ''
        elif type(nodes[0]) == list:
            return nodes[0][0]
        elif len(nodes) == 1:
            return nodes[0]
        elif len(nodes) == 3:
            if nodes[1].find('*') >= 0:
                return nodes[1]
            else:
                return nodes[0] + nodes[1] + nodes[2]

    def return_string(self, _context, nodes):
        """Transforms string to OTL format with optional '_raw like' or '_raw rlike' strings

        :param _context: An object used to keep parser context info
        :param nodes: Nodes of the parse tree on this iteration
        :return: Terminal string, optionally with '_raw like' or '_raw rlike'

        """

        if len(nodes) == 0:
            return ''
        if (nodes[0] == '"') and (nodes[len(nodes) - 1] == '"'):
            if len(nodes) == 3:
                return '(_raw rlike \'' + nodes[1] + '\')'
            else:
                return '""'
        else:
            return '(_raw like \'%' + nodes[0][0] + '%\')'
