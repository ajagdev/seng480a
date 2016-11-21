------------------------------ MODULE project2 ------------------------------
EXTENDS Integers

(*
--fair algorithm tcs {
  variables EW = "green", NS = "red", timer = 5,
  EW_ped = "red", NS_ped = "red", EW_ped_button = FALSE, NS_ped_button = TRUE;
  
  { 
loop: while (TRUE) {
        
       either   EW_ped_button := TRUE;
       or       NS_ped_button := TRUE;
       or {
                EW_ped_button := EW_ped_button;
                NS_ped_button := NS_ped_button;
           };
       
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
        
        if (timer = 2) {
            
            if (EW_ped = "green") {
                EW_ped := "yellow";
            };
            
            if (NS_ped = "green") {
                NS_ped := "yellow";
            };
        };
        
         if ( timer = 0) {
         
t0:         EW_ped := "red";
            NS_ped := "red";
         
            if (EW = "red") {
                NS := "red";
                
                if (EW_ped_button = TRUE) {
ped1:               EW_ped := "green";
                    EW_ped_button := FALSE;
                };
                
ew_green:       EW := "green";
            } else {                
                EW := "red";
                
                if (NS_ped_button = TRUE) {
ped2:                NS_ped := "green";
                     NS_ped_button := FALSE;
                };
                
ns_green:       NS := "green";
            };
       
timer_reset: timer := 5;
        };
        
    };
  }
}
*)
\* BEGIN TRANSLATION
VARIABLES EW, NS, timer, EW_ped, NS_ped, EW_ped_button, NS_ped_button, pc

vars == << EW, NS, timer, EW_ped, NS_ped, EW_ped_button, NS_ped_button, pc >>

Init == (* Global variables *)
        /\ EW = "green"
        /\ NS = "red"
        /\ timer = 5
        /\ EW_ped = "red"
        /\ NS_ped = "red"
        /\ EW_ped_button = FALSE
        /\ NS_ped_button = TRUE
        /\ pc = "loop"

loop == /\ pc = "loop"
        /\ \/ /\ EW_ped_button' = TRUE
              /\ UNCHANGED NS_ped_button
           \/ /\ NS_ped_button' = TRUE
              /\ UNCHANGED EW_ped_button
           \/ /\ EW_ped_button' = EW_ped_button
              /\ NS_ped_button' = NS_ped_button
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
        /\ IF timer' = 2
              THEN /\ IF EW_ped = "green"
                         THEN /\ EW_ped' = "yellow"
                         ELSE /\ TRUE
                              /\ UNCHANGED EW_ped
                   /\ IF NS_ped = "green"
                         THEN /\ NS_ped' = "yellow"
                         ELSE /\ TRUE
                              /\ UNCHANGED NS_ped
              ELSE /\ TRUE
                   /\ UNCHANGED << EW_ped, NS_ped >>
        /\ IF timer' = 0
              THEN /\ pc' = "t0"
              ELSE /\ pc' = "loop"

t0 == /\ pc = "t0"
      /\ EW_ped' = "red"
      /\ NS_ped' = "red"
      /\ IF EW = "red"
            THEN /\ NS' = "red"
                 /\ IF EW_ped_button = TRUE
                       THEN /\ pc' = "ped1"
                       ELSE /\ pc' = "ew_green"
                 /\ EW' = EW
            ELSE /\ EW' = "red"
                 /\ IF NS_ped_button = TRUE
                       THEN /\ pc' = "ped2"
                       ELSE /\ pc' = "ns_green"
                 /\ NS' = NS
      /\ UNCHANGED << timer, EW_ped_button, NS_ped_button >>

ew_green == /\ pc = "ew_green"
            /\ EW' = "green"
            /\ pc' = "timer_reset"
            /\ UNCHANGED << NS, timer, EW_ped, NS_ped, EW_ped_button, 
                            NS_ped_button >>

ns_green == /\ pc = "ns_green"
            /\ NS' = "green"
            /\ pc' = "timer_reset"
            /\ UNCHANGED << EW, timer, EW_ped, NS_ped, EW_ped_button, 
                            NS_ped_button >>

ped1 == /\ pc = "ped1"
        /\ EW_ped' = "green"
        /\ EW_ped_button' = FALSE
        /\ pc' = "ew_green"
        /\ UNCHANGED << EW, NS, timer, NS_ped, NS_ped_button >>

ped2 == /\ pc = "ped2"
        /\ NS_ped' = "green"
        /\ NS_ped_button' = FALSE
        /\ pc' = "ns_green"
        /\ UNCHANGED << EW, NS, timer, EW_ped, EW_ped_button >>

timer_reset == /\ pc = "timer_reset"
               /\ timer' = 5
               /\ pc' = "loop"
               /\ UNCHANGED << EW, NS, EW_ped, NS_ped, EW_ped_button, 
                               NS_ped_button >>

Next == loop \/ t0 \/ ew_green \/ ns_green \/ ped1 \/ ped2 \/ timer_reset

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
         
p1 == INSTANCE project1 WITH EW <- EW, NS <- NS
=============================================================================
\* Modification History
\* Last modified Mon Nov 21 13:51:48 PST 2016 by Daniel
\* Last modified Mon Nov 21 13:08:57 PST 2016 by abhi
\* Last modified Mon Nov 21 12:05:43 PST 2016 by Daniel
\* Last modified Tue Nov 01 15:47:27 PDT 2016 by abhi
\* Last modified Tue Nov 01 15:39:16 PDT 2016 by Daniel
\* Created Tue Nov 01 15:33:18 PDT 2016 by Daniel
