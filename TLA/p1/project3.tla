------------------------------ MODULE project3 ------------------------------
EXTENDS Integers

(*
--fair algorithm tcs {
  variables EW = "green", NS = "red", timer = -1,
  EW_ped = "red", NS_ped = "red", EW_ped_button = FALSE, NS_ped_button = TRUE,
  NS_sensor = FALSE, EW_sensor = FALSE;
  
  { 
loop: while (TRUE) {
        
       either   EW_ped_button := TRUE;
       or       NS_ped_button := TRUE;
       or       NS_sensor := TRUE;
       or       EW_sensor := TRUE;
       or {
                EW_ped_button := EW_ped_button;
                NS_ped_button := NS_ped_button;
                EW_sensor := EW_sensor;
                NS_sensor := NS_sensor;
           };
       
       if ( timer >= 0) {
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
                
ew_green:       EW_sensor := FALSE;
                EW := "green";
            } else {                
                EW := "red";
                
                if (NS_ped_button = TRUE) {
                     NS_ped_button := FALSE;
ped2:                NS_ped := "green";
                };
                
ns_green:   NS_sensor := FALSE;
            NS := "green";
            };
            
        };
        
sensor: if (timer = -1) {
            if ((EW = "green" /\ NS_sensor = TRUE) \/ (NS = "green" /\ EW_sensor = TRUE)
                     \/ NS_ped_button = TRUE \/ EW_ped_button = TRUE) {
timer_reset:    timer := 5;
            };
        };
        
    };
  }
}
*)
\* BEGIN TRANSLATION
VARIABLES EW, NS, timer, EW_ped, NS_ped, EW_ped_button, NS_ped_button, 
          NS_sensor, EW_sensor, pc

vars == << EW, NS, timer, EW_ped, NS_ped, EW_ped_button, NS_ped_button, 
           NS_sensor, EW_sensor, pc >>

Init == (* Global variables *)
        /\ EW = "green"
        /\ NS = "red"
        /\ timer = -1
        /\ EW_ped = "red"
        /\ NS_ped = "red"
        /\ EW_ped_button = FALSE
        /\ NS_ped_button = TRUE
        /\ NS_sensor = FALSE
        /\ EW_sensor = FALSE
        /\ pc = "loop"

loop == /\ pc = "loop"
        /\ \/ /\ EW_ped_button' = TRUE
              /\ UNCHANGED <<NS_ped_button, NS_sensor, EW_sensor>>
           \/ /\ NS_ped_button' = TRUE
              /\ UNCHANGED <<EW_ped_button, NS_sensor, EW_sensor>>
           \/ /\ NS_sensor' = TRUE
              /\ UNCHANGED <<EW_ped_button, NS_ped_button, EW_sensor>>
           \/ /\ EW_sensor' = TRUE
              /\ UNCHANGED <<EW_ped_button, NS_ped_button, NS_sensor>>
           \/ /\ EW_ped_button' = EW_ped_button
              /\ NS_ped_button' = NS_ped_button
              /\ EW_sensor' = EW_sensor
              /\ NS_sensor' = NS_sensor
        /\ IF timer >= 0
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
            ELSE /\ pc' = "sensor"
                 /\ UNCHANGED << EW, NS, EW_ped, NS_ped, EW_ped_button, 
                                 NS_ped_button >>
      /\ UNCHANGED << timer, NS_sensor, EW_sensor >>

ew_green == /\ pc = "ew_green"
            /\ EW_sensor' = FALSE
            /\ EW' = "green"
            /\ pc' = "sensor"
            /\ UNCHANGED << NS, timer, EW_ped, NS_ped, EW_ped_button, 
                            NS_ped_button, NS_sensor >>

ns_green == /\ pc = "ns_green"
            /\ NS_sensor' = FALSE
            /\ NS' = "green"
            /\ pc' = "sensor"
            /\ UNCHANGED << EW, timer, EW_ped, NS_ped, EW_ped_button, 
                            NS_ped_button, EW_sensor >>

ped1 == /\ pc = "ped1"
        /\ EW_ped' = "green"
        /\ pc' = "ew_green"
        /\ UNCHANGED << EW, NS, timer, NS_ped, EW_ped_button, NS_ped_button, 
                        NS_sensor, EW_sensor >>

ped2 == /\ pc = "ped2"
        /\ NS_ped' = "green"
        /\ pc' = "ns_green"
        /\ UNCHANGED << EW, NS, timer, EW_ped, EW_ped_button, NS_ped_button, 
                        NS_sensor, EW_sensor >>

sensor == /\ pc = "sensor"
          /\ IF timer = -1
                THEN /\ IF (EW = "green" /\ NS_sensor = TRUE) \/ (NS = "green" /\ EW_sensor = TRUE)
                                \/ NS_ped_button = TRUE \/ EW_ped_button = TRUE
                           THEN /\ pc' = "timer_reset"
                           ELSE /\ pc' = "loop"
                ELSE /\ pc' = "loop"
          /\ UNCHANGED << EW, NS, timer, EW_ped, NS_ped, EW_ped_button, 
                          NS_ped_button, NS_sensor, EW_sensor >>

timer_reset == /\ pc = "timer_reset"
               /\ timer' = 5
               /\ pc' = "loop"
               /\ UNCHANGED << EW, NS, EW_ped, NS_ped, EW_ped_button, 
                               NS_ped_button, NS_sensor, EW_sensor >>

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
              /\ UNCHANGED << EW, NS, timer, EW_ped_button, NS_ped_button, 
                              NS_sensor, EW_sensor >>

Next == loop \/ t0 \/ ew_green \/ ns_green \/ ped1 \/ ped2 \/ sensor
           \/ timer_reset \/ ped_yellow

Spec == /\ Init /\ [][Next]_vars
        /\ WF_vars(Next)

\* END TRANSLATION
Sensor == /\(NS_sensor = TRUE) ~> ( NS = "green" )
         /\(EW_sensor = TRUE) ~> ( EW = "green" )
         
p2 == INSTANCE project2 WITH EW <- EW, NS <- NS, NS_ped <- NS_ped, EW_ped <- EW_ped,
 EW_ped_button <- EW_ped_button, NS_ped_button <- NS_ped_button
=============================================================================
\* Modification History
\* Last modified Mon Nov 21 15:21:07 PST 2016 by Daniel
\* Last modified Mon Nov 21 13:08:57 PST 2016 by abhi
\* Last modified Mon Nov 21 12:05:43 PST 2016 by Daniel
\* Last modified Tue Nov 01 15:47:27 PDT 2016 by abhi
\* Last modified Tue Nov 01 15:39:16 PDT 2016 by Daniel
\* Created Tue Nov 01 15:33:18 PDT 2016 by Daniel
