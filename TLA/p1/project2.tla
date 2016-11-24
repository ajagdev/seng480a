------------------------------ MODULE project2 ------------------------------
EXTENDS Integers

(*
--fair algorithm tcs {
  variables EW = "green", NS = "red", timer = 5,
  EW_ped = "red", NS_ped = "red", EW_ped_button = FALSE, NS_ped_button = FALSE;
  process (triggers = 0)
  {
triggers: either   EW_ped_button := TRUE;
       or       NS_ped_button := TRUE;
    }
  
  
  fair process (lights = 1)
  { 
loop: while (TRUE) {       
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

ProcSet == {0} \cup {1}

Init == (* Global variables *)
        /\ EW = "green"
        /\ NS = "red"
        /\ timer = 5
        /\ EW_ped = "red"
        /\ NS_ped = "red"
        /\ EW_ped_button = FALSE
        /\ NS_ped_button = FALSE
        /\ pc = [self \in ProcSet |-> CASE self = 0 -> "button"
                                        [] self = 1 -> "loop"]

button == /\ pc[0] = "button"
          /\ \/ /\ EW_ped_button' = TRUE
                /\ UNCHANGED NS_ped_button
             \/ /\ NS_ped_button' = TRUE
                /\ UNCHANGED EW_ped_button
          /\ pc' = [pc EXCEPT ![0] = "Done"]
          /\ UNCHANGED << EW, NS, timer, EW_ped, NS_ped >>

buttons == button

loop == /\ pc[1] = "loop"
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
              THEN /\ pc' = [pc EXCEPT ![1] = "ped_yellow"]
              ELSE /\ pc' = [pc EXCEPT ![1] = "t0"]
        /\ UNCHANGED << EW_ped, NS_ped, EW_ped_button, NS_ped_button >>

t0 == /\ pc[1] = "t0"
      /\ IF timer = 0
            THEN /\ EW_ped' = "red"
                 /\ NS_ped' = "red"
                 /\ IF EW = "red"
                       THEN /\ NS' = "red"
                            /\ IF EW_ped_button = TRUE
                                  THEN /\ EW_ped_button' = FALSE
                                       /\ pc' = [pc EXCEPT ![1] = "ped1"]
                                  ELSE /\ pc' = [pc EXCEPT ![1] = "ew_green"]
                                       /\ UNCHANGED EW_ped_button
                            /\ UNCHANGED << EW, NS_ped_button >>
                       ELSE /\ EW' = "red"
                            /\ IF NS_ped_button = TRUE
                                  THEN /\ NS_ped_button' = FALSE
                                       /\ pc' = [pc EXCEPT ![1] = "ped2"]
                                  ELSE /\ pc' = [pc EXCEPT ![1] = "ns_green"]
                                       /\ UNCHANGED NS_ped_button
                            /\ UNCHANGED << NS, EW_ped_button >>
            ELSE /\ pc' = [pc EXCEPT ![1] = "loop"]
                 /\ UNCHANGED << EW, NS, EW_ped, NS_ped, EW_ped_button, 
                                 NS_ped_button >>
      /\ timer' = timer

timer_reset == /\ pc[1] = "timer_reset"
               /\ timer' = 5
               /\ pc' = [pc EXCEPT ![1] = "loop"]
               /\ UNCHANGED << EW, NS, EW_ped, NS_ped, EW_ped_button, 
                               NS_ped_button >>

ew_green == /\ pc[1] = "ew_green"
            /\ EW' = "green"
            /\ pc' = [pc EXCEPT ![1] = "timer_reset"]
            /\ UNCHANGED << NS, timer, EW_ped, NS_ped, EW_ped_button, 
                            NS_ped_button >>

ns_green == /\ pc[1] = "ns_green"
            /\ NS' = "green"
            /\ pc' = [pc EXCEPT ![1] = "timer_reset"]
            /\ UNCHANGED << EW, timer, EW_ped, NS_ped, EW_ped_button, 
                            NS_ped_button >>

ped1 == /\ pc[1] = "ped1"
        /\ EW_ped' = "green"
        /\ pc' = [pc EXCEPT ![1] = "ew_green"]
        /\ UNCHANGED << EW, NS, timer, NS_ped, EW_ped_button, NS_ped_button >>

ped2 == /\ pc[1] = "ped2"
        /\ NS_ped' = "green"
        /\ pc' = [pc EXCEPT ![1] = "ns_green"]
        /\ UNCHANGED << EW, NS, timer, EW_ped, EW_ped_button, NS_ped_button >>

ped_yellow == /\ pc[1] = "ped_yellow"
              /\ IF EW_ped = "green"
                    THEN /\ EW_ped' = "yellow"
                    ELSE /\ TRUE
                         /\ UNCHANGED EW_ped
              /\ IF NS_ped = "green"
                    THEN /\ NS_ped' = "yellow"
                    ELSE /\ TRUE
                         /\ UNCHANGED NS_ped
              /\ pc' = [pc EXCEPT ![1] = "t0"]
              /\ UNCHANGED << EW, NS, timer, EW_ped_button, NS_ped_button >>

lights == loop \/ t0 \/ timer_reset \/ ew_green \/ ns_green \/ ped1 \/ ped2
             \/ ped_yellow

Next == buttons \/ lights

Spec == /\ Init /\ [][Next]_vars
        /\ WF_vars(Next)
        /\ WF_vars(lights)

\* END TRANSLATION
Press == /\(NS_ped_button = TRUE) ~> (NS_ped_button = FALSE /\ NS_ped = "green")
         /\(EW_ped_button = TRUE) ~> (EW_ped_button = FALSE /\ EW_ped = "green")
         
LongerYellow == /\ [][(NS_ped = "green" /\ NS_ped' = "yellow") => (NS = "green")]_<<NS_ped, NS>>
                /\ [][(EW_ped = "green" /\ EW_ped' = "yellow") => (EW = "green")]_<<EW_ped, EW>>

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

Properties == Press /\ LongerYellow /\ NoPedCollisions /\ PedCycle /\ PedOnRed
         
p1 == INSTANCE project1 WITH EW <- EW, NS <- NS
=============================================================================
\* Modification History
\* Last modified Thu Nov 24 11:58:47 PST 2016 by Daniel
\* Last modified Mon Nov 21 13:08:57 PST 2016 by abhi
\* Last modified Mon Nov 21 12:05:43 PST 2016 by Daniel
\* Last modified Tue Nov 01 15:47:27 PDT 2016 by abhi
\* Last modified Tue Nov 01 15:39:16 PDT 2016 by Daniel
\* Created Tue Nov 01 15:33:18 PDT 2016 by Daniel
