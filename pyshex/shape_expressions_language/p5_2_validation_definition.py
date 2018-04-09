""" Implementation of `5.2 Validation Definition <http://shex.io/shex-semantics/#validation>`_ """
from typing import Tuple, List

from ShExJSG.ShExJ import BNODE
from pyjsg.jsglib.jsg import isinstance_

from pyshex.parse_tree.parse_node import ParseNode
from pyshex.shape_expressions_language.p5_3_shape_expressions import satisfies
from pyshex.shape_expressions_language.p5_context import Context
from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import Node
from pyshex.shapemap_structure_and_language.p3_shapemap_structure import FixedShapeMap, START, nodeSelector


def isValid(cntxt: Context, m: FixedShapeMap) -> Tuple[bool, List[str]]:
    """`5.2 Validation Definition <http://shex.io/shex-semantics/#validation>`_

    The expression isValid(G, m) indicates that for every nodeSelector/shapeLabel pair (n, s) in m, s has a
        corresponding shape expression se and satisfies(n, se, G, m). satisfies is defined below for each form
        of shape expression

    :param cntxt: evaluation context - includes graph and schema
    :param m: list of NodeShape pairs to test
    :return: Success/failure indicator and, if fail, a list of failure reasons
    """
    parse_nodes = []
    for nodeshapepair in m:
        n = nodeshapepair.nodeSelector
        if not isinstance_(n, Node):
            return False, [f"{n}: Tripple patterns are not implemented"]
        elif isinstance_(nodeshapepair.shapeLabel, BNODE):
            return False, [f"{nodeshapepair.shapeLabel}: BNode shape references are not implemented"]
        else:
            s = cntxt.shapeExprFor(START if nodeshapepair.shapeLabel is None or nodeshapepair.shapeLabel is START
                                   else nodeshapepair.shapeLabel)
            cntxt.current_node = ParseNode(satisfies, s, n)
            if not s:
                if nodeshapepair.shapeLabel is START or nodeshapepair.shapeLabel is None:
                    cntxt.current_node.fail_reason = "START node is not specified or is invalid"
                else:
                    cntxt.current_node.fail_reason = f"Shape: {nodeshapepair.shapeLabel} not found in Schema"
                return False, cntxt.process_reasons()
            parse_nodes.append(cntxt.current_node)
            if not satisfies(cntxt, n, s):
                cntxt.current_node.result = False
                return False, cntxt.process_reasons()
            else:
                cntxt.current_node.result = True
    return True, []
