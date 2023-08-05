from sqlwhat.Test import TestFail, Test
from sqlwhat.State import State

from functools import partial, wraps
import copy

def requires_ast(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        state = kwargs.get('state', args[0] if len(args) else None)
        AntlrException = state.ast_dispatcher.ast.AntlrException

        state_ast = [state.student_ast, state.solution_ast]
        parse_fail = any(isinstance(ast, AntlrException) for ast in state_ast)

        if parse_fail: return state              # skip test
        else: return f(*args, **kwargs)          # proceed with test

    return wrapper

@requires_ast
def check_node(state, name, index=0, missing_msg="Your submission is incorrect. Try again!", priority=None):
    """Select a node from abstract syntax tree (AST), using its name and index position.
    
    Args:
        state: State instance describing student and solution code. Can be omitted if used with Ex().
        name : the name of the abstract syntax tree node to find.
        index: the position of that node (see below for details).
        missing_msg: feedback message if node is not in student AST.
        priority: the priority level of the node being searched for. This determines whether to
                  descend into other AST nodes during the search. Higher priority nodes descend
                  into lower priority. Currently, the only important part of priority is that 
                  setting a very high priority (e.g. 99) will search every node.
                

    :Example:
        If both the student and solution code are.. ::

            SELECT a FROM b; SELECT x FROM y;

        then we can focus on the first select with::
        
            # approach 1: with manually created State instance
            state = State(*args, **kwargs)
            new_state = check_node(state, 'SelectStmt', 0)
            
            # approach 2:  with Ex and chaining
            new_state = Ex().check_node('SelectStmt', 0)

    """
    df = partial(state.ast_dispatcher, 'node', name, slice(None), priority=priority)

    stu_stmt_list = df(state.student_ast)
    try: stu_stmt = stu_stmt_list[index]
    except IndexError: 
        _msg = missing_msg.format(name)
        state.reporter.do_test(Test(_msg))

    sol_stmt_list = df(state.solution_ast) 
    try: sol_stmt = sol_stmt_list[index]
    except IndexError: raise IndexError("Can't get %s statement at index %s"%(name, index))

    return state.to_child(student_ast = stu_stmt, solution_ast = sol_stmt)

@requires_ast
def check_field(state, name, index=None, missing_msg="Your submission is incorrect. Try again!"):
    """Select an attribute from an abstract syntax tree (AST) node, using the attribute name.
    
    Args:
        state: State instance describing student and solution code. Can be omitted if used with Ex().
        name: the name of the attribute to select from current AST node.
        index: entry to get from field. If too few entires, will fail with missing_msg.
        missing_msg: feedback message if attribute is not in student AST.

    :Example:
        If both the student and solution code are.. ::
            
            SELECT a FROM b; SELECT x FROM y;

        then we can get the from_clause using ::

            # approach 1: with manually created State instance -----
            state = State(*args, **kwargs)
            select = check_node(state, 'SelectStmt', 0)
            clause = check_field(select, 'from_clause')

            # approach 2: with Ex and chaining ---------------------
            select = Ex().check_node('SelectStmt', 0)     # get first select statement
            clause =  select.check_field('from_clause')    # get from_clause (a list)
            clause2 = select.check_field('from_clause', 0) # get first entry in from_clause
    """
    try: 
        stu_attr = getattr(state.student_ast, name)
        if index is not None: stu_attr = stu_attr[index]
    except: 
        _msg = missing_msg.format(name)
        state.reporter.do_test(Test(_msg))

    try: 
        sol_attr = getattr(state.solution_ast, name)
        if index is not None: sol_attr = sol_attr[index]
    except IndexError: 
        raise IndexError("Can't get %s attribute"%name)

    # fail if attribute exists, but is none only for student
    if stu_attr is None and sol_attr is not None:
        _msg = missing_msg.format(name)
        state.reporter.do_test(Test(_msg))

    return state.to_child(student_ast = stu_attr, solution_ast = sol_attr)

import re

def test_student_typed(state, text, msg="Submission does not contain the code `{}`.", fixed=False):
    """Test whether the student code contains text.

    Args:
        state: State instance describing student and solution code. Can be omitted if used with Ex().
        text : text that student code must contain.
        msg  : feedback message if text is not in student code.
        fixed: whether to match text exactly, rather than using regular expressions.

    Note:
        Functions like ``check_node`` focus on certain parts of code.
        Using these functions followed by ``test_student_typed`` will only look
        in the code being focused on.

    :Example:
        If the student code is.. ::

            SELECT a FROM b WHERE id < 100

        Then the first test below would (unfortunately) pass, but the second would fail..::

            # contained in student code
            Ex().test_student_typed(text="id < 10")

            # the $ means that you are matching the end of a line
            Ex().test_student_typed(text="id < 10$")

        By setting ``fixed = True``, you can search for fixed strings::

            # without fixed = True, '*' matches any character
            Ex().test_student_typed(text="SELECT * FROM b")               # passes
            Ex().test_student_typed(text="SELECT \\\\* FROM b")             # fails
            Ex().test_student_typed(text="SELECT * FROM b", fixed=True)   # fails

        You can check only the code corresponding to the WHERE clause, using ::

            where = Ex().check_node('SelectStmt', 0).check_field('where_clause')
            where.test_student_typed(text = "id < 10)


    """
    stu_text = state.student_ast._get_text(state.student_code)

    _msg = msg.format(text)
    if fixed and not text in stu_text:            # simple text matching
        state.reporter.do_test(Test(msg))
    elif not re.match(text, stu_text):            # regex
        state.reporter.do_test(Test(msg))

    return state


@requires_ast
def has_equal_ast(state, msg="Your submission is incorrect. Try again!", sql=None, start="sql_script"):
    """Test whether the student and solution code have identical AST representations
    
    """
    ast = state.ast_dispatcher.ast
    sol_ast = state.solution_ast if sql is None else ast.parse(sql, start)
    if repr(state.student_ast) != repr(sol_ast):
        state.reporter.do_test(Test(msg))

    return state


def test_mc(state, correct, msgs):
    """
    Note uses 1-based indexing in order to work with Datacamp's campus app.
    """

    ctxt = {}
    exec(state.student_code, globals(), ctxt)
    sel_indx = ctxt['selected_option']
    if sel_indx != correct:
        state.reporter.do_test(Test(msgs[sel_indx-1]))
    else:
        state.reporter.feedback.success_msg = msgs[correct-1]

    return state

def success_msg(state, msg):
    """
    Changes the success message to display if submission passes.
    """
    state.reporter.success_msg = msg

    return state

def verify_ast_parses(state):
    if state.student_ast is None or state.solution_ast is None:
        state.reporter.do_test(Test("AST did not parse"))
