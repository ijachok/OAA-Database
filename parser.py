import sys
import re #regex
import database

whitespaces = [' ', '\t', '\r', '\n', '\0']
specialchar = ['(', ')', ',', ';', '>', '<', '=']

class Token(object):
    def __init__(self, type, text):
        self.type=type
        self.text=text

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.text)
        )

    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text=""):
        self.text=text+"\n"
        self.pos=0
        self.current_char=self.text[self.pos]

    def getinput(self, text=".. "):
        self.text=input(text)+"\n"
        self.pos=0
        self.current_char=self.text[self.pos]
        
    def advance(self):
        self.pos+=1
        if self.pos >= len(self.text):
            self.getinput()
        else:
            self.current_char = self.text[self.pos]
        
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char in whitespaces:
            self.advance()
            
    def get_next_token(self):
        text=""
        if self.current_char in whitespaces:
            self.skip_whitespace()

        if self.current_char=='"':
            self.advance()
            while self.current_char!='"':
                if self.current_char=="\n":
                    sys.stderr.write('ERROR at '+text[-10]+': a string must be written on a single line\n')
                    return Token("error", "string break")
                else:
                    text+=self.current_char
                    self.advance()
            self.advance()
            return Token("string", text)

        elif self.current_char=='>' or self.current_char=='<' or self.current_char=='=':
            text+=self.current_char
            self.advance()
            return Token("sign", text)

        elif self.current_char==',':
            self.advance()
            return Token("comma", ",")

        elif self.current_char=='(' or self.current_char==')':
            text+=self.current_char
            self.advance()
            return Token("bracket", text)

        elif self.current_char==';':
            #no need to advance past this
            return Token("end", ";")
        
        else:
            while self.current_char not in whitespaces and self.current_char not in specialchar:
                text+=self.current_char
                self.advance()
            return Token("keyword", text)

class Parser(object):
    def __init__(self):
        self.lexer=Lexer(input("> "))
        self.current_token=self.lexer.get_next_token()

    def next_token(self):
        self.current_token=self.lexer.get_next_token()

    def reset(self):
        self.lexer.getinput("> ")
        self.next_token()

    def tokenize(self):
        tokens=[]
        while self.current_token.type!="end":
            if self.current_token.type=="error":
                return []
            elif self.current_token.text.lower()=="q" or self.current_token.text.lower()=="quit":
                return [Token("end", "quit")]
            tokens.append(self.current_token)
            self.next_token()
        tokens.append(self.current_token)
        return tokens


class Interpreter(object):

    def __init__(self):
        self.parser=Parser()
        self.tokens=self.parser.tokenize()
        self.pos=0
        if(len(self.tokens)>0):
            self.current_token=self.tokens[0]

    def reset(self):
        self.parser.reset()
        self.pos=0
        self.tokens=self.parser.tokenize()
        self.current_token=self.tokens[self.pos]

    def next_token(self):
        self.pos+=1
        self.current_token=self.tokens[self.pos]
    
    def interpret_create(self):
        self.next_token()
        columns=[]
        if self.current_token.type!="keyword":
            sys.stderr.write('Unexpected argument "'+self.current_token.text+'": expected the table\'s name\n')
            return
        if (re.fullmatch("[a-zA-Z][a-zA-Z0-9_]*", self.current_token.text)):
            tablename=self.current_token.text
            self.next_token()
            if self.current_token.type!="bracket" or self.current_token.text!="(":
                sys.stderr.write('Unexpected argument "'+self.current_token.text+'": expected the list of columns enclosed in brackets\n')
                return
            self.next_token()
            while True:
                columns.append(self.current_token.text)
                self.next_token()
                if(self.current_token.type=="keyword"):
                    if self.current_token.text.upper()=="INDEXED":
                        self.next_token() #unused
                    else:
                        sys.stderr.write('Unknown keyword '+self.current_token.text.upper())
                        return
                if(self.current_token.type=="comma"):
                    self.next_token()
                    continue
                if(self.current_token.type=="bracket"):
                    if self.current_token.text==")":
                        self.next_token()
                        break
                    else:
                        sys.stderr.write('Unexpected bracket "'+self.current_token.text+'": expected the closing bracket\n')
                else:
                    sys.stderr.write('Unexpected argument "'+self.current_token.text+'": did you separate the names with commas properly?\n')
                    return
            if(self.current_token.type!="end"):
                sys.stderr.write('Error: expected the command to end after the list of column names\n')
                return
            else:
                database.create_table(tablename, columns)
                return
            
        else:
            sys.stderr.write('ERROR: invalid table name "'+self.current_token.text+'"\n')
            return

    def interpret_insert(self):
        values=[]
        self.next_token()
        if(self.current_token.type!="keyword"):
            sys.stderr.write('ERROR: expected a table name or the INTO keyword after INSERT')
            return
        if(self.current_token.text.upper()=="INTO"):
            self.next_token()
        tablename=self.current_token.text
        self.next_token()
        if self.current_token.type!="bracket" or self.current_token.text!="(":
            sys.stderr.write('Unexpected argument "'+self.current_token.text+'": expected the list of values enclosed in brackets\n')
            return
        self.next_token()
        while True:
            if(self.current_token.type!="string"):
                sys.stderr.write('Values must be enclosed in double quotes.\n')
                return
            values.append(self.current_token.text)
            self.next_token()
            if(self.current_token.type=="comma"):
                self.next_token()
                continue
            if(self.current_token.type=="bracket"):
                if self.current_token.text==")":
                    self.next_token()
                    break
                else:
                    sys.stderr.write('Unexpected bracket "'+self.current_token.text+'": expected the closing bracket\n')
            else:
                sys.stderr.write('Unexpected argument "'+self.current_token.text+'": did you separate the values with commas properly?\n')
                return
        if(self.current_token.type!="end"):
            sys.stderr.write('Error: expected the command to end after the list of column names\n')
            return
        else:
            database.insert_into_table(tablename, values)
            return

    def interpret_select(self):
        self.next_token()
        condition=None
        order_by=None
        column=True
        if self.current_token.type!="keyword" or self.current_token.text.upper()!="FROM":
            sys.stderr.write('Error: do not put anything between SELECT and FROM, this command only supports selecting all columns.\n')
            return
        self.next_token()
        if self.current_token.type!="keyword":
            sys.stderr.write('Error: expected the table name after FROM.\n')
            return
        tablename=self.current_token.text
        self.next_token()
        if self.current_token.type=="keyword" and self.current_token.text.upper()=="WHERE":
            condition=[]
            self.next_token()
            if self.current_token.type!="keyword":
                sys.stderr.write('Error: expected the column name after WHERE.\n')
                return
            condition.append(self.current_token.text)
            self.next_token()
            if self.current_token.type!="sign":
                sys.stderr.write('Error: the sign after the column name in WHERE.\n')
                return
            if self.current_token.text!=">":
                sys.stderr.write('Error: only the ">" operator is supported.\n')
                return
            else:
                condition.append(">")
            self.next_token()
            if self.current_token.type=="keyword":
                column=True
            elif self.current_token.type=="string":
                column=False
            else:
                sys.stderr.write('Error: expected a value or a column name after the comparison operator.\n')
                return
            condition.append(self.current_token.text)
            self.next_token()
        if self.current_token.type=="keyword" and self.current_token.text.upper()=="ORDER_BY":
            order_by=[]
            self.next_token()
            while True:
                sort="ASC"
                if self.current_token.type!="keyword":
                    sys.stderr.write('Error: expected a comma-separated list of columns after ORDER BY.\n')
                    return
                column=self.current_token.text
                self.next_token()
                if self.current_token.type=="keyword":
                    if self.current_token.text.upper()=="DESC":
                        sort="DESC"
                        self.next_token()
                    elif self.current_token.text.upper()=="ASC":
                        sort="ASC"
                        self.next_token()
                    else:
                        sys.stderr.write('Error: Unknown keyword '+self.current_token.text.upper()+', expected ASC or DESC.\n')
                        return
                order_by.append((column, sort))
                if self.current_token.type=="comma":
                    self.next_token()
                    continue
                if self.current_token.type=="end":
                    break
                else:
                    sys.stderr.write('Error: Unexpected argument '+self.current_token.text+'\n')
                    return
        database.print_table(database.database[tablename]['columns'], database.select_from_table(database.database[tablename], condition, order_by, column))
        return

    def interpret(self):
        if len(self.tokens)==0:
            self.reset()
            self.interpret()
        if self.current_token.text.lower() == "q" or self.current_token.text.lower() == "quit":
            return
        elif self.current_token.text.upper() == "CREATE":
            self.interpret_create()
        elif self.current_token.text.upper() == "INSERT":
            self.interpret_insert()
        elif self.current_token.text.upper() == "SELECT":
            self.interpret_select()
        self.reset()
        self.interpret()
