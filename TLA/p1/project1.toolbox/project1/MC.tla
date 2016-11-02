---- MODULE MC ----
EXTENDS project1, TLC

\* SPECIFICATION definition @modelBehaviorSpec:0
spec_14780432836964000 ==
Spec
----
\* INVARIANT definition @modelCorrectnessInvariants:0
inv_14780432837075000 ==
((EW = "green" \/ EW = "yellow")=>(NS = "red"))
/\
((NS = "green" \/ NS = "yellow")=>(EW = "red"))
----
=============================================================================
\* Modification History
\* Created Tue Nov 01 16:34:43 PDT 2016 by abhi
