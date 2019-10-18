% Financial Portfolio

% Funcs

function int: dot_prod(array[bInd] of 0..1: v1, 
                       array[bInd] of 0..1: v2) = 
  sum(i in bInd) (bool2int(v1[i] == 1 /\ v2[i] == 1));
  
function var int: dot_prod(array[bInd] of var 0..1: v1, 
                                array[bInd] of var 0..1: v2) = 
  sum(i in bInd) (bool2int(v1[i] == 1 /\ v2[i] == 1));

% Params

int: targetLambda;

int: v;
int: b;
int: r;

set of int: vInd = 1..v;
set of int: bInd = 1..b;

% Vars

array[vInd, bInd] of var 0..1: M;

% Objective

constraint max(r1 in vInd, r2 in r1+1..v) (dot_prod(M[r1, ..], M[r2, ..])) <= targetLambda;
solve satisfy;

% Constraints

constraint forall(i in vInd) (sum(M[i, ..]) = r);

% Output

output [
  "v = ", show(v), "\n",
  "b = ", show(b), "\n",
  "r = ", show(r), "\n",
  "Lambda = ", show(max(r1 in vInd, r2 in r1+1..v) 
                       (dot_prod(M[r1, ..], M[r2, ..]))), "\n",
  "M = \n", show2d(M), "\n",
];