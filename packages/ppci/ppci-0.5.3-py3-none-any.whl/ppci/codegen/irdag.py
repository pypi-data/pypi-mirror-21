""" IR to DAG

The process of instruction selection is preceeded by the creation of
a selection DAG (directed acyclic graph). The dagger take ir-code as
input and produces such a dag for instruction selection.

A DAG represents the logic (computation) of a single basic block.

To do selection with tree matching, the DAG is then splitted into a
series of tree patterns. This is often referred to as a forest of trees.

.. autoclass:: ppci.codegen.irdag.SelectionGraphBuilder
    :members: build

.. autoclass:: ppci.codegen.irdag.DagSplitter
    :members: split_into_trees

"""

import logging
from .. import ir
from ..arch.generic_instructions import Label
from ..binutils.debuginfo import FpOffsetAddress
from ..utils.tree import Tree
from .selectiongraph import SGNode, SGValue, SelectionGraph


def prepare_function_info(arch, function_info, ir_function):
    """ Fill function info with labels for all basic blocks """
    # First define labels and phis:

    function_info.epilog_label = Label(
        make_label_name(ir_function) + '_epilog')

    for ir_block in ir_function:
        # Put label into map:
        function_info.label_map[ir_block] = Label(make_label_name(ir_block))

        # Create virtual registers for phi-nodes:
        for phi in ir_block.phis:
            vreg = function_info.frame.new_reg(
                arch.get_reg_class(ty=phi.ty), twain=phi.name)
            function_info.phi_map[phi] = vreg

    function_info.arg_vregs = []
    for arg in ir_function.arguments:
        # New vreg:
        vreg = function_info.frame.new_reg(
            arch.value_classes[arg.ty], twain=arg.name)
        function_info.arg_vregs.append(vreg)

    if isinstance(ir_function, ir.Function):
        function_info.rv_vreg = function_info.frame.new_reg(
            arch.get_reg_class(ty=ir_function.return_ty), twain='retval')

    function_info.arg_types = [a.ty for a in ir_function.arguments]


class FunctionInfo:
    """ Keeps track of global function data when generating code for part
    of a functions. """
    def __init__(self, frame):
        self.frame = frame
        self.value_map = {}  # mapping from ir-value to dag node
        self.label_map = {}
        self.epilog_label = None
        self.phi_map = {}  # mapping from phi node to vreg
        self.block_trees = {}  # Mapping from block to tree serie for block
        self.block_tails = {}


def depth_first_order(function):
    """ Return blocks in depth first search order """
    blocks = [function.entry]
    L = [function.entry]
    while L:
        b = L.pop(0)
        for b2 in b.successors:
            if b2 not in blocks:
                blocks.append(b2)
                L.append(b2)
    return blocks


class Operation:
    """ A single operation with a type """
    def __init__(self, op, ty):
        self.op = op
        self.ty = ty
        # assert ty, str(op)+str(ty)
        if op == 'MOV' and ty is None:
            raise AssertionError('MOV must not have type none')

    def __str__(self):
        if self.ty is None or self.op in ['LABEL', 'CALL']:
            return self.op.upper()
        else:
            return '{}{}'.format(self.op, str(self.ty)).upper()


def make_map(cls):
    """
        Add an attribute to the class that is a map of ir types to handler
        functions. For example if a function is called do_phi it will be
        registered into f_map under key ir.Phi.
    """
    f_map = getattr(cls, 'f_map')
    for name, func in list(cls.__dict__.items()):
        if name.startswith('do_'):
            tp_name = ''.join(x.capitalize() for x in name[2:].split('_'))
            ir_class = getattr(ir, tp_name)
            f_map[ir_class] = func
    return cls


@make_map
class SelectionGraphBuilder:
    """ Create a selectiongraph from a function for instruction selection """
    logger = logging.getLogger('selection-graph-builder')
    f_map = {}

    def __init__(self, arch, debug_db):
        self.arch = arch
        self.debug_db = debug_db
        self.size_map = {8: ir.i8, 16: ir.i16, 32: ir.i32, 64: ir.i64}
        self.ptr_ty = self.size_map[arch.byte_sizes['ptr'] * 8]

    def build(self, ir_function: ir.SubRoutine, function_info):
        """ Create a selection graph for the given function.

        Selection graph is divided into groups for each basic block.
        """
        self.sgraph = SelectionGraph()
        self.function_info = function_info

        # TODO: fix this total mess with vreg, block and chains:
        self.current_block = None

        # Create maps for global variables:
        for variable in ir_function.module.variables:
            val = self.new_node('LABEL', ir.ptr)
            val.value = make_label_name(variable)
            self.add_map(variable, val.new_output(variable.name))

        # Create start node:
        self.current_token = self.new_node('ENTRY', None).new_output(
            'token', kind=SGValue.CONTROL)

        # Create temporary registers for aruments:
        for arg, vreg in zip(ir_function.arguments, function_info.arg_vregs):
            param_node = self.new_node('REG', arg.ty, value=vreg)
            output = param_node.new_output(arg.name)
            output.vreg = vreg

            # When refering the paramater, use the copied value:
            self.add_map(arg, output)

            self.chain(param_node)

        # Generate nodes for all blocks:
        for ir_block in depth_first_order(ir_function):
            self.block_to_sgraph(ir_block, function_info)

        self.sgraph.check()
        return self.sgraph

    def block_to_sgraph(self, ir_block: ir.Block, function_info):
        """ Create dag (directed acyclic graph) from a basic block.

        The resulting dag can be used for instruction selection.
        """
        assert isinstance(ir_block, ir.Block)

        self.current_block = ir_block

        # Create start node:
        entry_node = self.new_node('ENTRY', None)
        entry_node.value = ir_block
        self.current_token = entry_node.new_output(
            'token', kind=SGValue.CONTROL)

        # Generate series of trees:
        for instruction in ir_block:
            # In case of last statement, first perform phi-lifting:
            if instruction.is_terminator:
                self.copy_phis_of_successors(ir_block)

            # Dispatch the handler depending on type:
            self.f_map[type(instruction)](self, instruction)

        # Save tail node of this block:
        function_info.block_tails[ir_block] = self.current_token.node

        # Create end node:
        sgnode = self.new_node('EXIT', None)
        sgnode.add_input(self.current_token)

    def do_jump(self, node):
        sgnode = self.new_node('JMP', None)
        sgnode.value = self.function_info.label_map[node.target]
        self.debug_db.map(node, sgnode)
        self.chain(sgnode)

    def chain(self, sgnode):
        if self.current_token is not None:
            sgnode.add_input(self.current_token)
        self.current_token = sgnode.new_output('ctrl', kind=SGValue.CONTROL)

    def new_node(self, name, ty, *args, value=None):
        """ Create a new selection graph node, and add it to the graph """
        assert isinstance(name, str)
        assert isinstance(ty, ir.Typ) or ty is None
        # assert isinstance(name, Operation)
        if ty is ir.ptr:
            ty = self.ptr_ty
        sgnode = SGNode(Operation(name, ty))
        sgnode.add_inputs(*args)
        sgnode.value = value
        sgnode.group = self.current_block
        self.sgraph.add_node(sgnode)
        return sgnode

    def new_vreg(self, ty):
        """ Generate a new temporary fitting for the given type """
        return self.function_info.frame.new_reg(self.arch.value_classes[ty])

    def add_map(self, node, sgvalue):
        assert isinstance(node, ir.Value)
        assert isinstance(sgvalue, SGValue)
        self.function_info.value_map[node] = sgvalue

    def get_value(self, node):
        return self.function_info.value_map[node]

    def do_return(self, node):
        """ Move result into result register and jump to epilog """
        res = self.get_value(node.result)
        vreg = self.function_info.rv_vreg
        mov_node = self.new_node('MOV', node.result.ty, res, value=vreg)
        self.chain(mov_node)

        # Jump to epilog:
        sgnode = self.new_node('JMP', None)
        sgnode.value = self.function_info.epilog_label
        self.chain(sgnode)

    def do_c_jump(self, node):
        """ Process conditional jump into dag """
        lhs = self.get_value(node.a)
        rhs = self.get_value(node.b)
        cond = node.cond
        sgnode = self.new_node('CJMP', None, lhs, rhs)
        sgnode.value = cond, self.function_info.label_map[node.lab_yes],\
            self.function_info.label_map[node.lab_no]
        self.chain(sgnode)
        self.debug_db.map(node, sgnode)

    def do_exit(self, node):
        # Jump to epilog:
        sgnode = self.new_node('JMP', None)
        sgnode.value = self.function_info.epilog_label
        self.chain(sgnode)

    def do_alloc(self, node):
        """ Process the alloc instruction """
        # TODO: check alignment?
        # fp = self.new_node("REG", ir.ptr, value=self.arch.fp)
        # fp_output = fp.new_output('fp')
        # fp_output.wants_vreg = False
        # offset = self.new_node("CONST", ir.ptr)
        offset = self.function_info.frame.alloc(node.amount)
        # offset_output = offset.new_output('offset')
        # offset_output.wants_vreg = False
        sgnode = self.new_node('FPREL', ir.ptr, value=offset)

        output = sgnode.new_output('alloc')
        output.wants_vreg = False
        self.add_map(node, output)
        if self.debug_db.contains(node):
            dbg_var = self.debug_db.get(node)
            dbg_var.address = FpOffsetAddress(offset)
        # self.debug_db.map(node, sgnode)

    def get_address(self, ir_address):
        """ Determine address for load or store. """
        if isinstance(ir_address, ir.Variable):
            # A global variable may be contained in another module
            # That is why it is created here, and not in the prepare step
            sgnode = self.new_node('LABEL', ir.ptr)
            sgnode.value = make_label_name(ir_address)
            address = sgnode.new_output('address')
        else:
            address = self.get_value(ir_address)
        return address

    def do_load(self, node):
        """ Create dag node for load operation """
        address = self.get_address(node.address)
        sgnode = self.new_node('LDR', node.ty, address)
        # Make sure a data dependence is added to this node
        self.debug_db.map(node, sgnode)
        self.chain(sgnode)
        self.add_map(node, sgnode.new_output(node.name))

    def do_store(self, node):
        """ Create a DAG node for the store operation """
        address = self.get_address(node.address)
        value = self.get_value(node.value)
        sgnode = self.new_node('STR', node.value.ty, address, value)
        self.chain(sgnode)
        self.debug_db.map(node, sgnode)

    def do_const(self, node):
        """ Process constant instruction """
        if isinstance(node.value, (int, float)):
            value = node.value
        else:  # pragma: no cover
            raise NotImplementedError(str(type(node.value)))
        sgnode = self.new_node('CONST', node.ty)
        self.debug_db.map(node, sgnode)
        sgnode.value = value
        output = sgnode.new_output(node.name)
        output.wants_vreg = False
        self.add_map(node, output)

    def do_literal_data(self, node):
        """ Literal data is stored after a label """
        label = self.function_info.frame.add_constant(node.data)
        sgnode = self.new_node('LABEL', ir.ptr, value=label)
        self.add_map(node, sgnode.new_output(node.name))

    def do_binop(self, node):
        """ Visit a binary operator and create a DAG node """
        names = {'+': 'ADD', '-': 'SUB', '|': 'OR', '<<': 'SHL',
                 '*': 'MUL', '&': 'AND', '>>': 'SHR', '/': 'DIV',
                 '%': 'REM', '^': 'XOR'}
        op = names[node.operation]
        a = self.get_value(node.a)
        b = self.get_value(node.b)
        sgnode = self.new_node(op, node.ty, a, b)
        self.debug_db.map(node, sgnode)
        self.add_map(node, sgnode.new_output(node.name))

    def do_cast(self, node):
        """ Create a cast of type """
        from_ty = node.src.ty
        if from_ty is ir.ptr:
            from_ty = self.ptr_ty
        op = '{}TO'.format(str(from_ty).upper())
        a = self.get_value(node.src)
        sgnode = self.new_node(op, node.ty, a)
        self.add_map(node, sgnode.new_output(node.name))

    def prep_call_arguments(self, node):
        """ Prepare call arguments into new temporaries """
        # This is the moment to move all parameters to new temp registers.
        args = []
        inputs = []
        for argument in node.arguments:
            arg_val = self.get_value(argument)
            loc = self.new_vreg(argument.ty)
            args.append(loc)
            arg_sgnode = self.new_node('MOV', argument.ty, arg_val, value=loc)
            self.chain(arg_sgnode)
            # inputs.append(arg_sgnode.new_output('x'))

        arg_types = [argument.ty for argument in node.arguments]
        return args, inputs, arg_types

    def do_procedure_call(self, node):
        """ Transform a procedure call """
        args, inputs, arg_types = self.prep_call_arguments(node)

        # Perform the actual call:
        sgnode = self.new_node('CALL', None)
        sgnode.value = (node.function_name, arg_types, args)
        self.debug_db.map(node, sgnode)
        for i in inputs:
            sgnode.add_input(i)
        self.chain(sgnode)

    def do_function_call(self, node):
        """ Transform a function call """
        args, inputs, arg_types = self.prep_call_arguments(node)

        # New register for copy of result:
        ret_val = self.function_info.frame.new_reg(
            self.arch.value_classes[node.ty], '{}_result'.format(node.name))

        # Perform the actual call:
        sgnode = self.new_node('CALL', node.ty)
        sgnode.value = (node.function_name, arg_types, node.ty, args, ret_val)
        self.debug_db.map(node, sgnode)
        for i in inputs:
            sgnode.add_input(i)
        self.chain(sgnode)

        # When using the call as an expression, use the return value vreg:
        sgnode = self.new_node('REG', node.ty, value=ret_val)
        output = sgnode.new_output('res')
        output.vreg = ret_val
        self.add_map(node, output)

    def do_phi(self, node):
        """ Refer to the correct copy of the phi node """
        vreg = self.function_info.phi_map[node]
        sgnode = self.new_node('REG', node.ty, value=vreg)
        output = sgnode.new_output(node.name)
        output.vreg = vreg
        self.add_map(node, output)
        self.debug_db.map(node, vreg)

    def copy_phis_of_successors(self, ir_block):
        """ When a terminator instruction is encountered, handle the copy
        of phi values into the expected virtual register """
        # Copy values to phi nodes in other blocks:
        # step 1: create a new temporary that contains the value of the phi
        # node. Do this because the calculation of the value can involve the
        # phi vreg itself.
        val_map = {}
        for succ_block in ir_block.successors:
            for phi in succ_block.phis:
                from_val = phi.get_value(ir_block)
                val = self.get_value(from_val)
                vreg1 = self.new_vreg(phi.ty)
                sgnode = self.new_node('MOV', phi.ty, val, value=vreg1)
                self.chain(sgnode)
                val_map[from_val] = vreg1

        # Step 2: copy the temporary value to the phi register:
        for succ_block in ir_block.successors:
            for phi in succ_block.phis:
                vreg = self.function_info.phi_map[phi]
                from_val = phi.get_value(ir_block)
                vreg1 = val_map[from_val]

                # Create reg node:
                sgnode1 = self.new_node('REG', phi.ty, value=vreg1)
                val = sgnode1.new_output(vreg1.name)

                # Create move node:
                sgnode = self.new_node('MOV', phi.ty, val, value=vreg)
                self.chain(sgnode)


def make_label_name(dut):
    """ Returns the assembly code label name for the given ir-object """
    if isinstance(dut, ir.Block):
        return make_label_name(dut.function) + '_block_' + dut.name
    elif isinstance(dut, (ir.SubRoutine, ir.Variable)):
        return make_label_name(dut.module) + '_' + dut.name
    elif isinstance(dut, ir.Module):
        return dut.name
    else:  # pragma: no cover
        raise NotImplementedError(str(dut) + str(type(dut)))


def topological_sort_modified(nodes, start):
    """ Modified topological sort, start at the end and work back """
    unmarked = set(nodes)
    marked = set()
    temp_marked = set()
    L = []

    def visit(n):
        if n not in nodes:
            return
        assert n not in temp_marked, 'DAG has cycles'
        if n in unmarked:
            temp_marked.add(n)

            # 1 satisfy control dependencies:
            for inp in n.control_inputs:
                visit(inp.node)

            # 2 memory dependencies:
            for inp in n.memory_inputs:
                visit(inp.node)

            # 3 data dependencies:
            for inp in n.data_inputs:
                visit(inp.node)
            temp_marked.remove(n)
            marked.add(n)
            unmarked.remove(n)
            L.append(n)

    # Start to visit with pre-knowledge of the last node!
    visit(start)
    while unmarked:
        node = next(iter(unmarked))
        visit(node)

    # Hack: move tail again to tail:
    if L:
        if L[-1] is not start:
            L.remove(start)
            L.append(start)
    return L


class DagSplitter:
    """ Class that splits a DAG into a series of trees. This series is sorted
        such that data dependencies are met. The trees can henceforth be
        used to match trees.
    """
    logger = logging.getLogger('dag-splitter')

    def __init__(self, arch, debug_db):
        self.arch = arch
        self.debug_db = debug_db

    def split_into_trees(self, sgraph, ir_function, function_info):
        """ Split a forest of trees into a sorted series of trees for each
            block.
        """
        self.assign_vregs(sgraph, function_info)
        for ir_block in ir_function:
            nodes = sgraph.get_group(ir_block)
            # Get rid of ENTRY and EXIT:
            nodes = set(
                filter(
                    lambda x: x.name.op not in ['ENTRY', 'EXIT'], nodes))

            tail_node = function_info.block_tails[ir_block]
            trees = self.make_trees(nodes, tail_node)
            function_info.block_trees[ir_block] = trees

    def assign_vregs(self, sgraph, function_info):
        """ Give vreg values to values that cross block boundaries """
        frame = function_info.frame
        for node in sgraph:
            if node.group:
                self.check_vreg(node, frame)

    def check_vreg(self, node, frame):
        """ Determine whether node outputs need a virtual register """
        assert node.group is not None

        for data_output in node.data_outputs:
            if (len(data_output.users) > 1) or node.volatile or \
                    any(u.group is not node.group
                        for u in data_output.users):
                if data_output.wants_vreg and not data_output.vreg:
                    cls = self.get_reg_class(data_output)
                    vreg = frame.new_reg(cls, data_output.name)
                    data_output.vreg = vreg

    def make_trees(self, nodes, tail_node):
        """ Create a tree from a list of sorted nodes. """
        sorted_nodes = topological_sort_modified(nodes, tail_node)
        trees = []
        node_map = {}

        def mk_tr(inp):
            if inp.vreg:
                # If the input value has a vreg, use it
                child_tree = Tree(
                    self.make_op('REG', inp.ty), value=inp.vreg)
            elif inp.node in node_map:
                child_tree = node_map[inp.node]
            elif inp.node.name.op == 'LABEL':
                child_tree = Tree(str(inp.node.name), value=inp.node.value)
            else:  # inp.node.name.startswith('CONST'):
                # If the node is a constant, use that
                assert not inp.wants_vreg
                children = [mk_tr(i) for i in inp.node.inputs]
                child_tree = Tree(
                    str(inp.node.name), *children, value=inp.node.value)
            return child_tree

        for node in sorted_nodes:
            assert len(node.data_outputs) <= 1

            # Determine data dependencies:
            children = []
            for inp in node.data_inputs:
                child_tree = mk_tr(inp)
                children.append(child_tree)

            # Create a tree node:
            tree = Tree(str(node.name), *children, value=node.value)
            self.debug_db.map(node, tree)

            # Handle outputs:
            if len(node.data_outputs) == 0:
                # If the tree was volatile, it must be emitted
                if node.volatile:
                    trees.append(tree)
            else:
                # If the output has a vreg, put the value in:
                data_output = node.data_outputs[0]
                if data_output.vreg:
                    vreg = data_output.vreg
                    typ = data_output.ty
                    if typ is None:
                        print(node)
                    tree = Tree(self.make_op('MOV', typ), tree, value=vreg)
                    trees.append(tree)
                    tree = Tree(self.make_op('REG', typ), value=vreg)
                elif node.volatile:
                    trees.append(tree)

            # Store for later:
            node_map[node] = tree
        return trees

    def make_op(self, op, typ):
        """ Construct a string opcode from an operation and a type """
        assert isinstance(typ, ir.Typ), str(typ)
        return '{}{}'.format(op, typ).upper()

    def get_reg_class(self, data_flow):
        """ Determine the register class suited for this data flow line """
        op = data_flow.node.name
        assert isinstance(op.ty, ir.Typ)
        return self.arch.get_reg_class(ty=op.ty)
