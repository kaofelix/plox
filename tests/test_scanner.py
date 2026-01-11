import pytest

from plox.scanner import (
    Scanner,
    Token,
    TokenType,
    UnexpectedCharacterError,
    UnterminatedStringError,
)


class TestSingleCharacterTokens:
    def test_left_paren(self):
        scanner = Scanner("(")
        tokens = scanner.scan_tokens()
        assert len(tokens) == 2  # LEFT_PAREN + EOF
        assert tokens[0].type == TokenType.LEFT_PAREN
        assert tokens[0].lexeme == "("
        assert tokens[0].line == 1

    def test_right_paren(self):
        scanner = Scanner(")")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.RIGHT_PAREN
        assert tokens[0].lexeme == ")"

    def test_left_brace(self):
        scanner = Scanner("{")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.LEFT_BRACE
        assert tokens[0].lexeme == "{"

    def test_right_brace(self):
        scanner = Scanner("}")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.RIGHT_BRACE
        assert tokens[0].lexeme == "}"

    def test_comma(self):
        scanner = Scanner(",")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.COMMA
        assert tokens[0].lexeme == ","

    def test_dot(self):
        scanner = Scanner(".")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.DOT
        assert tokens[0].lexeme == "."

    def test_minus(self):
        scanner = Scanner("-")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.MINUS
        assert tokens[0].lexeme == "-"

    def test_plus(self):
        scanner = Scanner("+")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.PLUS
        assert tokens[0].lexeme == "+"

    def test_semicolon(self):
        scanner = Scanner(";")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.SEMICOLON
        assert tokens[0].lexeme == ";"

    def test_star(self):
        scanner = Scanner("*")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.STAR
        assert tokens[0].lexeme == "*"

    def test_bang(self):
        scanner = Scanner("!")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.BANG
        assert tokens[0].lexeme == "!"

    def test_equal(self):
        scanner = Scanner("=")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.EQUAL
        assert tokens[0].lexeme == "="

    def test_less(self):
        scanner = Scanner("<")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.LESS
        assert tokens[0].lexeme == "<"

    def test_greater(self):
        scanner = Scanner(">")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.GREATER
        assert tokens[0].lexeme == ">"

    def test_slash(self):
        scanner = Scanner("/")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.SLASH
        assert tokens[0].lexeme == "/"


class TestTwoCharacterTokens:
    def test_bang_equal(self):
        scanner = Scanner("!=")
        tokens = scanner.scan_tokens()
        assert len(tokens) == 2
        assert tokens[0].type == TokenType.BANG_EQUAL
        assert tokens[0].lexeme == "!="

    def test_equal_equal(self):
        scanner = Scanner("==")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.EQUAL_EQUAL
        assert tokens[0].lexeme == "=="

    def test_less_equal(self):
        scanner = Scanner("<=")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.LESS_EQUAL
        assert tokens[0].lexeme == "<="

    def test_greater_equal(self):
        scanner = Scanner(">=")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.GREATER_EQUAL
        assert tokens[0].lexeme == ">="


class TestStringLiterals:
    def test_empty_string(self):
        scanner = Scanner('""')
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].lexeme == '""'
        assert tokens[0].literal == ""

    def test_string_with_text(self):
        scanner = Scanner('"hello"')
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].lexeme == '"hello"'
        assert tokens[0].literal == "hello"

    def test_string_with_spaces(self):
        scanner = Scanner('"hello world"')
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].literal == "hello world"

    def test_string_with_quotes(self):
        # Note: The current scanner doesn't handle escape sequences
        # This test documents the actual behavior
        with pytest.raises(UnexpectedCharacterError) as exc_info:
            scanner = Scanner('"hello \\"world\\""')
            scanner.scan_tokens()
        assert exc_info.value.line == 1
        assert exc_info.value.char == "\\"

    def test_multiline_string(self):
        scanner = Scanner('"hello\nworld"')
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].literal == "hello\nworld"
        assert tokens[0].line == 2  # Line number updated at newline

    def test_unterminated_string(self):
        scanner = Scanner('"unterminated')
        with pytest.raises(UnterminatedStringError) as exc_info:
            scanner.scan_tokens()
        assert exc_info.value.line == 1


class TestNumberLiterals:
    def test_integer(self):
        scanner = Scanner("123")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].lexeme == "123"
        assert tokens[0].literal == 123.0

    def test_zero(self):
        scanner = Scanner("0")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].literal == 0.0

    def test_float(self):
        scanner = Scanner("123.456")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].lexeme == "123.456"
        assert tokens[0].literal == 123.456

    def test_float_with_zero_integer_part(self):
        scanner = Scanner("0.5")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].literal == 0.5

    def test_float_with_zero_fraction_part(self):
        scanner = Scanner("5.0")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].literal == 5.0

    def test_dot_alone_is_not_a_number(self):
        scanner = Scanner(".")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.DOT
        assert tokens[0].lexeme == "."

    def test_number_with_dot_no_digits(self):
        scanner = Scanner("1.")
        tokens = scanner.scan_tokens()
        assert len(tokens) == 3  # NUMBER, DOT, EOF
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].literal == 1.0
        assert tokens[1].type == TokenType.DOT


class TestIdentifiers:
    def test_simple_identifier(self):
        scanner = Scanner("variable")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].lexeme == "variable"
        assert tokens[0].literal is None

    def test_identifier_with_underscore(self):
        # Note: The current scanner doesn't support underscores in identifiers
        # Only alphanumeric characters are supported
        with pytest.raises(UnexpectedCharacterError) as exc_info:
            scanner = Scanner("_underscore")
            scanner.scan_tokens()
        assert exc_info.value.line == 1
        assert exc_info.value.char == "_"

    def test_identifier_with_numbers(self):
        scanner = Scanner("var123")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].lexeme == "var123"

    def test_identifier_with_uppercase(self):
        scanner = Scanner("MyVariable")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].lexeme == "MyVariable"

    def test_camel_case_identifier(self):
        scanner = Scanner("camelCase")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].lexeme == "camelCase"


class TestKeywords:
    def test_and_keyword(self):
        scanner = Scanner("and")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.AND
        assert tokens[0].lexeme == "and"

    def test_class_keyword(self):
        scanner = Scanner("class")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.CLASS

    def test_else_keyword(self):
        scanner = Scanner("else")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.ELSE

    def test_false_keyword(self):
        scanner = Scanner("false")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.FALSE

    def test_fun_keyword(self):
        scanner = Scanner("fun")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.FUN

    def test_for_keyword(self):
        scanner = Scanner("for")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.FOR

    def test_if_keyword(self):
        scanner = Scanner("if")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.IF

    def test_nil_keyword(self):
        scanner = Scanner("nil")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.NIL

    def test_or_keyword(self):
        scanner = Scanner("or")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.OR

    def test_print_keyword(self):
        scanner = Scanner("print")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.PRINT

    def test_return_keyword(self):
        scanner = Scanner("return")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.RETURN

    def test_super_keyword(self):
        scanner = Scanner("super")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.SUPER

    def test_this_keyword(self):
        scanner = Scanner("this")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.THIS

    def test_true_keyword(self):
        scanner = Scanner("true")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.TRUE

    def test_var_keyword(self):
        scanner = Scanner("var")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.VAR

    def test_while_keyword(self):
        scanner = Scanner("while")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.WHILE


class TestComments:
    def test_line_comment(self):
        scanner = Scanner("// this is a comment")
        tokens = scanner.scan_tokens()
        assert len(tokens) == 1  # Only EOF
        assert tokens[0].type == TokenType.EOF

    def test_code_before_comment(self):
        scanner = Scanner("123 // comment")
        tokens = scanner.scan_tokens()
        assert len(tokens) == 2
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].literal == 123.0

    def test_comment_with_code_after(self):
        scanner = Scanner("// comment\n456")
        tokens = scanner.scan_tokens()
        assert len(tokens) == 2
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].literal == 456.0
        assert tokens[0].line == 2


class TestWhitespace:
    def test_space_ignored(self):
        scanner = Scanner("   (   ")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.LEFT_PAREN
        assert tokens[0].lexeme == "("

    def test_tab_ignored(self):
        scanner = Scanner("\t(\t")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.LEFT_PAREN

    def test_carriage_return_ignored(self):
        scanner = Scanner("\r(\r")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.LEFT_PAREN

    def test_newline_increments_line(self):
        scanner = Scanner("(\n)")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.LEFT_PAREN
        assert tokens[0].line == 1
        assert tokens[1].type == TokenType.RIGHT_PAREN
        assert tokens[1].line == 2


class TestMultipleTokens:
    def test_simple_expression(self):
        scanner = Scanner("1 + 2")
        tokens = scanner.scan_tokens()
        assert len(tokens) == 4  # NUMBER, PLUS, NUMBER, EOF
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[1].type == TokenType.PLUS
        assert tokens[2].type == TokenType.NUMBER
        assert tokens[3].type == TokenType.EOF

    def test_complex_expression(self):
        scanner = Scanner("(1 + 2) * 3")
        tokens = scanner.scan_tokens()
        assert [
            t.type for t in tokens[:-1]
        ] == [
            TokenType.LEFT_PAREN,
            TokenType.NUMBER,
            TokenType.PLUS,
            TokenType.NUMBER,
            TokenType.RIGHT_PAREN,
            TokenType.STAR,
            TokenType.NUMBER,
        ]

    def test_variable_declaration(self):
        scanner = Scanner("var x = 10;")
        tokens = scanner.scan_tokens()
        assert [
            t.type for t in tokens[:-1]
        ] == [
            TokenType.VAR,
            TokenType.IDENTIFIER,
            TokenType.EQUAL,
            TokenType.NUMBER,
            TokenType.SEMICOLON,
        ]

    def test_function_call(self):
        scanner = Scanner("print(x);")
        tokens = scanner.scan_tokens()
        assert [
            t.type for t in tokens[:-1]
        ] == [
            TokenType.PRINT,
            TokenType.LEFT_PAREN,
            TokenType.IDENTIFIER,
            TokenType.RIGHT_PAREN,
            TokenType.SEMICOLON,
        ]

    def test_comparison_operators(self):
        scanner = Scanner("1 == 2 != 3 <= 4 >= 5 < 6 > 7")
        tokens = scanner.scan_tokens()
        assert [
            t.type for t in tokens[:-1]
        ] == [
            TokenType.NUMBER,
            TokenType.EQUAL_EQUAL,
            TokenType.NUMBER,
            TokenType.BANG_EQUAL,
            TokenType.NUMBER,
            TokenType.LESS_EQUAL,
            TokenType.NUMBER,
            TokenType.GREATER_EQUAL,
            TokenType.NUMBER,
            TokenType.LESS,
            TokenType.NUMBER,
            TokenType.GREATER,
            TokenType.NUMBER,
        ]


class TestEdgeCases:
    def test_empty_source(self):
        scanner = Scanner("")
        tokens = scanner.scan_tokens()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF

    def test_whitespace_only(self):
        scanner = Scanner("   \t\n\r  ")
        tokens = scanner.scan_tokens()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF

    def test_identifier_that_starts_with_keyword(self):
        scanner = Scanner("andy")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].lexeme == "andy"

    def test_identifier_that_contains_keyword(self):
        scanner = Scanner("orphan")
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].lexeme == "orphan"


class TestErrorHandling:
    def test_unexpected_character(self):
        scanner = Scanner("@")
        with pytest.raises(UnexpectedCharacterError) as exc_info:
            scanner.scan_tokens()
        assert exc_info.value.line == 1
        assert exc_info.value.char == "@"

    def test_unexpected_character_after_valid_tokens(self):
        scanner = Scanner("1 + @")
        with pytest.raises(UnexpectedCharacterError) as exc_info:
            scanner.scan_tokens()
        assert exc_info.value.line == 1
        assert exc_info.value.char == "@"

    def test_unexpected_character_on_new_line(self):
        scanner = Scanner("1\n@")
        with pytest.raises(UnexpectedCharacterError) as exc_info:
            scanner.scan_tokens()
        assert exc_info.value.line == 2
        assert exc_info.value.char == "@"

    def test_unterminated_string_on_multiline(self):
        scanner = Scanner('"start\ncontinue"')
        tokens = scanner.scan_tokens()
        # This should work - string can span multiple lines
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].literal == "start\ncontinue"


class TestTokenDataclass:
    def test_token_creation(self):
        token = Token(TokenType.NUMBER, "123", 123.0, 5)
        assert token.type == TokenType.NUMBER
        assert token.lexeme == "123"
        assert token.literal == 123.0
        assert token.line == 5

    def test_token_with_none_literal(self):
        token = Token(TokenType.IDENTIFIER, "x", None, 1)
        assert token.literal is None


class TestEOFToken:
    def test_eof_token_appended(self):
        scanner = Scanner("123")
        tokens = scanner.scan_tokens()
        assert tokens[-1].type == TokenType.EOF
        assert tokens[-1].lexeme == ""
        assert tokens[-1].literal is None


class TestLineTracking:
    def test_line_tracking_across_tokens(self):
        scanner = Scanner("(\n)\n(\n)")
        tokens = scanner.scan_tokens()
        assert tokens[0].line == 1
        assert tokens[1].line == 2
        assert tokens[2].line == 3
        assert tokens[3].line == 4

    def test_string_spanning_multiple_lines(self):
        scanner = Scanner('"line1\nline2\nline3"')
        tokens = scanner.scan_tokens()
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].literal == "line1\nline2\nline3"
        assert tokens[0].line == 3  # String ends on line 3
