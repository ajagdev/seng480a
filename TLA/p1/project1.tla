------------------------------ MODULE project1 ------------------------------
EXTENDS Integers

(*
--fair algorithm tcs {
  variables EW = "green", NS = "red", timer = 5;
  
  { 
    while (TRUE) {
        
           if ( timer > 0) {
            timer := timer - 1;
            };
     
            if ( timer = 1) {
             
                if (EW = "red") {
                    NS := "yellow";
                } else {
                    EW := "yellow";
                };
           
            };
            
             if ( timer = 0) {
             
                if (EW = "red") {
                    EW := "green";
                    NS := "red";
                } else {
                    NS := "green";
                    EW := "red";
                };
           
                timer := 5;
            };
        
    };
  }
}
*)
\* BEGIN TRANSLATION
VARIABLES EW, NS, timer, pc

vars == << EW, NS, timer, pc >>

Init == (* Global variables *)
        /\ EW = "green"
        /\ NS = "red"
        /\ timer = 5
        /\ pc = "Lbl_1"

Lbl_1 == /\ pc = "Lbl_1"
         /\ IF timer > 0
               THEN /\ timer' = timer - 1
               ELSE /\ TRUE
                    /\ timer' = timer
         /\ IF timer' = 1
               THEN /\ IF EW = "red"
                          THEN /\ NS' = "yellow"
                               /\ EW' = EW
                          ELSE /\ EW' = "yellow"
                               /\ NS' = NS
               ELSE /\ TRUE
                    /\ UNCHANGED << EW, NS >>
         /\ IF timer' = 0
               THEN /\ IF EW' = "red"
                          THEN /\ pc' = "Lbl_2"
                          ELSE /\ pc' = "Lbl_3"
               ELSE /\ pc' = "Lbl_1"

Lbl_4 == /\ pc = "Lbl_4"
         /\ timer' = 5
         /\ pc' = "Lbl_1"
         /\ UNCHANGED << EW, NS >>

Lbl_2 == /\ pc = "Lbl_2"
         /\ EW' = "green"
         /\ NS' = "red"
         /\ pc' = "Lbl_4"
         /\ timer' = timer

Lbl_3 == /\ pc = "Lbl_3"
         /\ NS' = "green"
         /\ EW' = "red"
         /\ pc' = "Lbl_4"
         /\ timer' = timer

Next == Lbl_1 \/ Lbl_4 \/ Lbl_2 \/ Lbl_3

Spec == /\ Init /\ [][Next]_vars
        /\ WF_vars(Next)

\* END TRANSLATION
NoCollisions == /\ []((EW = "green" \/ EW = "yellow") => NS = "red")
                /\ []((NS = "green" \/ NS = "yellow") => EW = "red")

Cycle == /\ [][EW = "green" => EW' = "yellow"]_<<EW>>
         /\ [][EW = "yellow" => EW' = "red"]_<<EW>>
         /\ [][EW = "red" => EW' = "green"]_<<EW>>
         /\ [][NS = "green" => NS' = "yellow"]_<<NS>>
         /\ [][NS = "yellow" => NS' = "red"]_<<NS>>
         /\ [][NS = "red" => NS' = "green"]_<<NS>>
=============================================================================
\* Modification History
\* Last modified Mon Nov 21 13:14:59 PST 2016 by Daniel
\* Last modified Mon Nov 21 13:08:57 PST 2016 by abhi
\* Last modified Mon Nov 21 12:05:43 PST 2016 by Daniel
\* Last modified Tue Nov 01 15:47:27 PDT 2016 by abhi
\* Last modified Tue Nov 01 15:39:16 PDT 2016 by Daniel
\* Created Tue Nov 01 15:33:18 PDT 2016 by Daniel
