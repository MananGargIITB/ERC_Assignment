# ERC_Assignment

I used python in VSCode to do this task.
I used the numpy fft function to find the frequency spectrum. The frequency spectrum has even spread of all frequencies (noise) and spikes at certain specific frequencies (Meaningful signal). Looking at the frequency spectrum, I took an eyeball value of 10000 Hz as the carrier frequency, since it was roughly the middle value of the meaningful signals.
I demodulated the signal and filter the audio using butter bandpass in the range 800 to 1800 Hz with order 5 filter.
I have also plotted the various relevant signals.
