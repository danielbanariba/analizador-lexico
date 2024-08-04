
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'CADENA COMA DEF DOS_PUNTOS ELSE FOR IDENTIFICADOR IF IN LLAVE_DER LLAVE_IZQ NUMERO OPERADOR_ARITMETICO OPERADOR_ASIGNACION OPERADOR_COMPARACION PARENTESIS_DER PARENTESIS_IZQ PRINT RETURN WHILEprograma : declaracionesdeclaraciones : declaracion\n                     | declaraciones declaraciondeclaracion : asignacion\n                   | if_stmt\n                   | while_stmt\n                   | for_stmt\n                   | funcion_def\n                   | expresion\n                   | print_stmt\n                   | return_stmtasignacion : IDENTIFICADOR OPERADOR_ASIGNACION expresionif_stmt : IF expresion DOS_PUNTOS bloque\n               | IF expresion DOS_PUNTOS bloque ELSE DOS_PUNTOS bloquewhile_stmt : WHILE expresion DOS_PUNTOS bloquefor_stmt : FOR IDENTIFICADOR IN expresion DOS_PUNTOS bloquefuncion_def : DEF IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER DOS_PUNTOS bloqueparametros : IDENTIFICADOR\n                  | parametros COMA IDENTIFICADOR\n                  | bloque : declaracion\n              | LLAVE_IZQ declaraciones LLAVE_DERexpresion : NUMERO\n                 | CADENA\n                 | IDENTIFICADOR\n                 | expresion OPERADOR_ARITMETICO expresion\n                 | expresion OPERADOR_COMPARACION expresion\n                 | PARENTESIS_IZQ expresion PARENTESIS_DERprint_stmt : PRINT PARENTESIS_IZQ expresion PARENTESIS_DERreturn_stmt : RETURN expresion'

_lr_action_items = {'IDENTIFICADOR':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22,23,24,25,27,32,33,34,35,36,37,38,39,40,41,43,44,45,46,50,52,53,55,56,57,58,59,61,62,],[12,12,-2,-4,-5,-6,-7,-8,-9,-10,-11,-25,27,27,29,30,27,-23,-24,27,-3,27,27,27,-25,27,-30,-26,-27,-12,12,12,27,48,-28,-13,-21,12,-15,-29,12,12,60,12,-22,-16,12,-14,-17,]),'IF':([0,2,3,4,5,6,7,8,9,10,11,12,18,19,22,27,33,34,35,36,37,38,41,43,44,45,46,50,52,53,56,57,58,59,61,62,],[13,13,-2,-4,-5,-6,-7,-8,-9,-10,-11,-25,-23,-24,-3,-25,-30,-26,-27,-12,13,13,-28,-13,-21,13,-15,-29,13,13,13,-22,-16,13,-14,-17,]),'WHILE':([0,2,3,4,5,6,7,8,9,10,11,12,18,19,22,27,33,34,35,36,37,38,41,43,44,45,46,50,52,53,56,57,58,59,61,62,],[14,14,-2,-4,-5,-6,-7,-8,-9,-10,-11,-25,-23,-24,-3,-25,-30,-26,-27,-12,14,14,-28,-13,-21,14,-15,-29,14,14,14,-22,-16,14,-14,-17,]),'FOR':([0,2,3,4,5,6,7,8,9,10,11,12,18,19,22,27,33,34,35,36,37,38,41,43,44,45,46,50,52,53,56,57,58,59,61,62,],[15,15,-2,-4,-5,-6,-7,-8,-9,-10,-11,-25,-23,-24,-3,-25,-30,-26,-27,-12,15,15,-28,-13,-21,15,-15,-29,15,15,15,-22,-16,15,-14,-17,]),'DEF':([0,2,3,4,5,6,7,8,9,10,11,12,18,19,22,27,33,34,35,36,37,38,41,43,44,45,46,50,52,53,56,57,58,59,61,62,],[16,16,-2,-4,-5,-6,-7,-8,-9,-10,-11,-25,-23,-24,-3,-25,-30,-26,-27,-12,16,16,-28,-13,-21,16,-15,-29,16,16,16,-22,-16,16,-14,-17,]),'NUMERO':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,17,18,19,21,22,23,24,25,27,32,33,34,35,36,37,38,39,41,43,44,45,46,50,52,53,56,57,58,59,61,62,],[18,18,-2,-4,-5,-6,-7,-8,-9,-10,-11,-25,18,18,18,-23,-24,18,-3,18,18,18,-25,18,-30,-26,-27,-12,18,18,18,-28,-13,-21,18,-15,-29,18,18,18,-22,-16,18,-14,-17,]),'CADENA':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,17,18,19,21,22,23,24,25,27,32,33,34,35,36,37,38,39,41,43,44,45,46,50,52,53,56,57,58,59,61,62,],[19,19,-2,-4,-5,-6,-7,-8,-9,-10,-11,-25,19,19,19,-23,-24,19,-3,19,19,19,-25,19,-30,-26,-27,-12,19,19,19,-28,-13,-21,19,-15,-29,19,19,19,-22,-16,19,-14,-17,]),'PARENTESIS_IZQ':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,17,18,19,20,21,22,23,24,25,27,30,32,33,34,35,36,37,38,39,41,43,44,45,46,50,52,53,56,57,58,59,61,62,],[17,17,-2,-4,-5,-6,-7,-8,-9,-10,-11,-25,17,17,17,-23,-24,32,17,-3,17,17,17,-25,40,17,-30,-26,-27,-12,17,17,17,-28,-13,-21,17,-15,-29,17,17,17,-22,-16,17,-14,-17,]),'PRINT':([0,2,3,4,5,6,7,8,9,10,11,12,18,19,22,27,33,34,35,36,37,38,41,43,44,45,46,50,52,53,56,57,58,59,61,62,],[20,20,-2,-4,-5,-6,-7,-8,-9,-10,-11,-25,-23,-24,-3,-25,-30,-26,-27,-12,20,20,-28,-13,-21,20,-15,-29,20,20,20,-22,-16,20,-14,-17,]),'RETURN':([0,2,3,4,5,6,7,8,9,10,11,12,18,19,22,27,33,34,35,36,37,38,41,43,44,45,46,50,52,53,56,57,58,59,61,62,],[21,21,-2,-4,-5,-6,-7,-8,-9,-10,-11,-25,-23,-24,-3,-25,-30,-26,-27,-12,21,21,-28,-13,-21,21,-15,-29,21,21,21,-22,-16,21,-14,-17,]),'$end':([1,2,3,4,5,6,7,8,9,10,11,12,18,19,22,27,33,34,35,36,41,43,44,46,50,57,58,61,62,],[0,-1,-2,-4,-5,-6,-7,-8,-9,-10,-11,-25,-23,-24,-3,-25,-30,-26,-27,-12,-28,-13,-21,-15,-29,-22,-16,-14,-17,]),'LLAVE_DER':([3,4,5,6,7,8,9,10,11,12,18,19,22,27,33,34,35,36,41,43,44,46,50,52,57,58,61,62,],[-2,-4,-5,-6,-7,-8,-9,-10,-11,-25,-23,-24,-3,-25,-30,-26,-27,-12,-28,-13,-21,-15,-29,57,-22,-16,-14,-17,]),'ELSE':([4,5,6,7,8,9,10,11,12,18,19,27,33,34,35,36,41,43,44,46,50,57,58,61,62,],[-4,-5,-6,-7,-8,-9,-10,-11,-25,-23,-24,-25,-30,-26,-27,-12,-28,51,-21,-15,-29,-22,-16,-14,-17,]),'OPERADOR_ARITMETICO':([9,12,18,19,26,27,28,31,33,34,35,36,41,42,47,],[23,-25,-23,-24,23,-25,23,23,23,23,23,23,-28,23,23,]),'OPERADOR_COMPARACION':([9,12,18,19,26,27,28,31,33,34,35,36,41,42,47,],[24,-25,-23,-24,24,-25,24,24,24,24,24,24,-28,24,24,]),'OPERADOR_ASIGNACION':([12,],[25,]),'DOS_PUNTOS':([18,19,26,27,28,34,35,41,47,51,54,],[-23,-24,37,-25,38,-26,-27,-28,53,56,59,]),'PARENTESIS_DER':([18,19,27,31,34,35,40,41,42,48,49,60,],[-23,-24,-25,41,-26,-27,-20,-28,50,-18,54,-19,]),'IN':([29,],[39,]),'LLAVE_IZQ':([37,38,53,56,59,],[45,45,45,45,45,]),'COMA':([40,48,49,60,],[-20,-18,55,-19,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'programa':([0,],[1,]),'declaraciones':([0,45,],[2,52,]),'declaracion':([0,2,37,38,45,52,53,56,59,],[3,22,44,44,3,22,44,44,44,]),'asignacion':([0,2,37,38,45,52,53,56,59,],[4,4,4,4,4,4,4,4,4,]),'if_stmt':([0,2,37,38,45,52,53,56,59,],[5,5,5,5,5,5,5,5,5,]),'while_stmt':([0,2,37,38,45,52,53,56,59,],[6,6,6,6,6,6,6,6,6,]),'for_stmt':([0,2,37,38,45,52,53,56,59,],[7,7,7,7,7,7,7,7,7,]),'funcion_def':([0,2,37,38,45,52,53,56,59,],[8,8,8,8,8,8,8,8,8,]),'expresion':([0,2,13,14,17,21,23,24,25,32,37,38,39,45,52,53,56,59,],[9,9,26,28,31,33,34,35,36,42,9,9,47,9,9,9,9,9,]),'print_stmt':([0,2,37,38,45,52,53,56,59,],[10,10,10,10,10,10,10,10,10,]),'return_stmt':([0,2,37,38,45,52,53,56,59,],[11,11,11,11,11,11,11,11,11,]),'bloque':([37,38,53,56,59,],[43,46,58,61,62,]),'parametros':([40,],[49,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programa","S'",1,None,None,None),
  ('programa -> declaraciones','programa',1,'p_programa','ejemplo2.py',82),
  ('declaraciones -> declaracion','declaraciones',1,'p_declaraciones','ejemplo2.py',86),
  ('declaraciones -> declaraciones declaracion','declaraciones',2,'p_declaraciones','ejemplo2.py',87),
  ('declaracion -> asignacion','declaracion',1,'p_declaracion','ejemplo2.py',94),
  ('declaracion -> if_stmt','declaracion',1,'p_declaracion','ejemplo2.py',95),
  ('declaracion -> while_stmt','declaracion',1,'p_declaracion','ejemplo2.py',96),
  ('declaracion -> for_stmt','declaracion',1,'p_declaracion','ejemplo2.py',97),
  ('declaracion -> funcion_def','declaracion',1,'p_declaracion','ejemplo2.py',98),
  ('declaracion -> expresion','declaracion',1,'p_declaracion','ejemplo2.py',99),
  ('declaracion -> print_stmt','declaracion',1,'p_declaracion','ejemplo2.py',100),
  ('declaracion -> return_stmt','declaracion',1,'p_declaracion','ejemplo2.py',101),
  ('asignacion -> IDENTIFICADOR OPERADOR_ASIGNACION expresion','asignacion',3,'p_asignacion','ejemplo2.py',105),
  ('if_stmt -> IF expresion DOS_PUNTOS bloque','if_stmt',4,'p_if_stmt','ejemplo2.py',109),
  ('if_stmt -> IF expresion DOS_PUNTOS bloque ELSE DOS_PUNTOS bloque','if_stmt',7,'p_if_stmt','ejemplo2.py',110),
  ('while_stmt -> WHILE expresion DOS_PUNTOS bloque','while_stmt',4,'p_while_stmt','ejemplo2.py',117),
  ('for_stmt -> FOR IDENTIFICADOR IN expresion DOS_PUNTOS bloque','for_stmt',6,'p_for_stmt','ejemplo2.py',121),
  ('funcion_def -> DEF IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER DOS_PUNTOS bloque','funcion_def',7,'p_funcion_def','ejemplo2.py',125),
  ('parametros -> IDENTIFICADOR','parametros',1,'p_parametros','ejemplo2.py',129),
  ('parametros -> parametros COMA IDENTIFICADOR','parametros',3,'p_parametros','ejemplo2.py',130),
  ('parametros -> <empty>','parametros',0,'p_parametros','ejemplo2.py',131),
  ('bloque -> declaracion','bloque',1,'p_bloque','ejemplo2.py',140),
  ('bloque -> LLAVE_IZQ declaraciones LLAVE_DER','bloque',3,'p_bloque','ejemplo2.py',141),
  ('expresion -> NUMERO','expresion',1,'p_expresion','ejemplo2.py',148),
  ('expresion -> CADENA','expresion',1,'p_expresion','ejemplo2.py',149),
  ('expresion -> IDENTIFICADOR','expresion',1,'p_expresion','ejemplo2.py',150),
  ('expresion -> expresion OPERADOR_ARITMETICO expresion','expresion',3,'p_expresion','ejemplo2.py',151),
  ('expresion -> expresion OPERADOR_COMPARACION expresion','expresion',3,'p_expresion','ejemplo2.py',152),
  ('expresion -> PARENTESIS_IZQ expresion PARENTESIS_DER','expresion',3,'p_expresion','ejemplo2.py',153),
  ('print_stmt -> PRINT PARENTESIS_IZQ expresion PARENTESIS_DER','print_stmt',4,'p_print_stmt','ejemplo2.py',163),
  ('return_stmt -> RETURN expresion','return_stmt',2,'p_return_stmt','ejemplo2.py',167),
]