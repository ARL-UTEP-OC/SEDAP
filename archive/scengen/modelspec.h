#flow 4
0.0 LISTEN TCP 5040
0.0 LISTEN UDP 5041
0.0 LISTEN UDP 5042

5.0 ON 10 TCP SRC 10.0.0.4/5030 DST 10.0.0.3/5030 PERIODIC [50.0 1280]
5.0 ON 11 UDP SRC 10.0.0.4/5051 DST 10.0.0.5/5051 PERIODIC [50.0 1280]
5.0 ON 12 UDP SRC 10.0.0.4/5062 DST 10.0.0.6/5062 PERIODIC [50.0 1280]


                                                                                                                                                                                     