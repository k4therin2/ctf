require 'wavefile'
include WaveFile

#Ask CTF Overlords for flag value
puts "Enter flag: "
flag = gets.chomp()

#Unpack ASCII to 8-digit binary
#EG character "C" >> 01100011
flag_binary_string = flag.unpack("B*")[0]

#Gonna put each single bit from ASCII char byte into array
#EG "abc" will produce flag_samples = "011000010110001001100011"
flag_samples = []


# split by each character so we can actually turn this into an array
# flag_binary_string ="011000010110001001100011"
# will produce flag_samples =[0,1,1,0,0,0,0,1,0,1,1,0,0,0,1,0,0,1,1,0,0,0,1,1]
flag_binary_string.split("").each do |c|
	# Let's pick something we can hear- instead of 1's and 0's, 
	# values will be 0.5 and -0.5. Don't ask why. Trust the science*.
	value = ((c.to_i)) - 0.5
	flag_samples << value
	# Since this is a waveform, add negative value right after so 
	# we can hear it! Even though we didn't encode this value!
	flag_samples << -1*value
end

puts flag_binary_string

# specify a duration to repeat each binary value
# so the .wav is long enough for us to hear....
duration = 100

buffer = Buffer.new(flag_samples, Format.new(:mono, :float, 44100))
Writer.new("flag.wav", Format.new(:mono, :pcm_16, 44100)) do |writer|
  # write to file value 
  # again and again and again 
  # the number of times we specified in duration variable
  duration.times { output = writer.write(buffer) }
 end

# * or read about it: http://wavefilegem.com/getting_started.html