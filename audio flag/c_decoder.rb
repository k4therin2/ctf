# This is only here because I don't want to spend one more second using C
puts "Input output from wav_decoder.c: "
flag = gets.chomp().split(" ")

# Don't even look at this
# Don't tell Andrew I ever wrote ruby like this
# Seriously I'm 4 glasses of wine in leave me alone

negative_duplicate = false



for x in flag
	if (negative_duplicate) 
	    negative_duplicate = !negative_duplicate
 	else 
	    if (x.to_i > 0) 
	    	print 1 
	    else 
	    	print 0
	    end
 	 	negative_duplicate = !negative_duplicate
 	end
end 
