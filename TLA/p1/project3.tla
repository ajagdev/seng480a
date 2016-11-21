------------------------------ MODULE project3 ------------------------------
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
            
ped_yellow: if (EW_ped = "green") {
                EW_ped := "yellow";
            };
            
            if (NS_ped = "green") {
                NS_ped := "yellow";
            };
        };
        
t0:      if ( timer = 0) {
         
            EW_ped := "red";
            NS_ped := "red";
         
            if (EW = "red") {
                NS := "red";
                
                if (EW_ped_button = TRUE) {
                    EW_ped_button := FALSE;
ped1:               EW_ped := "green";
                };
                
ew_green:       EW := "green";
            } else {                
                EW := "red";
                
                if (NS_ped_button = TRUE) {
                     NS_ped_button := FALSE;
ped2:                NS_ped := "green";
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
              THEN /\ pc' = "ped_yellow"
              ELSE /\ pc' = "t0"
        /\ UNCHANGED << EW_ped, NS_ped >>

t0 == /\ pc = "t0"
      /\ IF timer = 0
            THEN /\ EW_ped' = "red"
                 /\ NS_ped' = "red"
                 /\ IF EW = "red"
                       THEN /\ NS' = "red"
                            /\ IF EW_ped_button = TRUE
                                  THEN /\ EW_ped_button' = FALSE
                                       /\ pc' = "ped1"
                                  ELSE /\ pc' = "ew_green"
                                       /\ UNCHANGED EW_ped_button
                            /\ UNCHANGED << EW, NS_ped_button >>
                       ELSE /\ EW' = "red"
                            /\ IF NS_ped_button = TRUE
                                  THEN /\ NS_ped_button' = FALSE
                                       /\ pc' = "ped2"
                                  ELSE /\ pc' = "ns_green"
                                       /\ UNCHANGED NS_ped_button
                            /\ UNCHANGED << NS, EW_ped_button >>
            ELSE /\ pc' = "loop"
                 /\ UNCHANGED << EW, NS, EW_ped, NS_ped, EW_ped_button, 
                                 NS_ped_button >>
      /\ timer' = timer

timer_reset == /\ pc = "timer_reset"
               /\ timer' = 5
               /\ pc' = "loop"
               /\ UNCHANGED << EW, NS, EW_ped, NS_ped, EW_ped_button, 
                               NS_ped_button >>

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
        /\ pc' = "ew_green"
        /\ UNCHANGED << EW, NS, timer, NS_ped, EW_ped_button, NS_ped_button >>

ped2 == /\ pc = "ped2"
        /\ NS_ped' = "green"
        /\ pc' = "ns_green"
        /\ UNCHANGED << EW, NS, timer, EW_ped, EW_ped_button, NS_ped_button >>

ped_yellow == /\ pc = "ped_yellow"
              /\ IF EW_ped = "green"
                    THEN /\ EW_ped' = "yellow"
                    ELSE /\ TRUE
                         /\ UNCHANGED EW_ped
              /\ IF NS_ped = "green"
                    THEN /\ NS_ped' = "yellow"
                    ELSE /\ TRUE
                         /\ UNCHANGED NS_ped
              /\ pc' = "t0"
              /\ UNCHANGED << EW, NS, timer, EW_ped_button, NS_ped_button >>

Next == loop \/ t0 \/ timer_reset \/ ew_green \/ ns_green \/ ped1 \/ ped2
           \/ ped_yellow

Spec == /\ Init /\ [][Next]_vars
        /\ WF_vars(Next)

\* END TRANSLATION
Press == /\(NS_ped_button = TRUE) ~> (NS_ped_button = FALSE /\ NS_ped = "green")
         /\(EW_ped_button = TRUE) ~> (EW_ped_button = FALSE /\ EW_ped = "green")
         
LongerYellow == /\ [][(NS_ped = "green" /\ NS_ped = "yellow") => (NS = "green")]_<<NS_ped, NS>>
                /\ [][(EW_ped = "green" /\ EW_ped = "yellow") => (EW = "green")]_<<EW_ped, EW>>

NoPedCollisions == /\ []((EW = "green" \/ EW = "yellow") => (NS_ped = "red"))
                   /\ []((NS = "green" \/ NS = "yellow") => (EW_ped = "red"))

PedCycle == /\ [][EW_ped = "green" => EW_ped' = "yellow"]_<<EW_ped>>
            /\ [][EW_ped = "yellow" => EW_ped' = "red"]_<<EW_ped>>
            /\ [][EW_ped = "red" => EW_ped' = "green"]_<<EW_ped>>
            /\ [][NS_ped = "green" => NS_ped' = "yellow"]_<<NS_ped>>
            /\ [][NS_ped = "yellow" => NS_ped' = "red"]_<<NS_ped>>
            /\ [][NS_ped = "red" => NS_ped' = "green"]_<<NS_ped>>
            
PedOnRed == /\([][(EW_ped = "red" /\ EW_ped' = "green") => (EW = "red" /\ NS = "red")]_<<EW_ped, EW, NS>>)
            /\([][(NS_ped = "red" /\ NS_ped' = "green") => (EW = "red" /\ NS = "red")]_<<NS_ped, EW, NS>>)

         
p2 == INSTANCE project2 WITH EW <- EW, NS <- NS, NS_ped <- NS_ped, EW_ped <- EW_ped,
 EW_ped_button <- EW_ped_button, NS_ped_button <- NS_ped_button
=============================================================================
\* Modification History
\* Last modified Mon Nov 21 15:04:41 PST 2016 by abhi
\* Last modified Mon Nov 21 14:54:14 PST 2016 by Daniel
\* Last modified Mon Nov 21 13:08:57 PST 2016 by abhi
\* Last modified Mon Nov 21 12:05:43 PST 2016 by Daniel
\* Last modified Tue Nov 01 15:47:27 PDT 2016 by abhi
\* Last modified Tue Nov 01 15:39:16 PDT 2016 by Daniel
\* Created Tue Nov 01 15:33:18 PDT 2016 by Daniel
