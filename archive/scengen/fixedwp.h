  }

    for ($i = 1; $i <= $NN ; $i++) {

	($x, $y) = where_node($i, $time);
	move_node($i, $x, $y);

#	printf("t %f n %d x %f y %f\n",$time, $i, $x, $y);

	if ($show_cobwebs) {
	    # draw a line between us and any earlier nodes we're in range of
	    $current_position[$i][0] = $x;
	    $current_position[$i][1] = $y;	    
	    for ($j = 1; $j < $i ; $j++) {
		if (dist($x,$y,
			 $current_position[$j][0],  
			 $current_position[$j][1]) <= $RANGE) {
		    $CANVAS->create('line',
				    scale_dist($x),scale_dist($y),
				    scale_dist($current_position[$j][0]),  
				    scale_dist($current_position[$j][1]),
				    -fill => $cobweb_color,
				    -width => 2,
				    -tag => 'cobweb',
				    );
		}
	    }
	} # end of if show cobwebs

    }

}

###########