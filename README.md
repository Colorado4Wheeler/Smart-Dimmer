![](https://raw.githubusercontent.com/Colorado4Wheeler/WikiDocs/master/Smart-Dimmer/Logo-lg.png)

## Smart Dimmer

This plugin for the [Indigo Domotics](http://www.indigodomo.com/) home automation platform that allows you to use a single action to brighten and then dim a device.  This is very handy for control pages where you want a single icon to control your dimmable light rather than have a host of icons to turn on/off/dim up/dim down.

### Summary

I had a need to use a single button to dim AND brighten a device on my control pages. It is easy enough to say the button action would, say, "brighten by 25%" but once it hit 100% then I had to hit a different button to turn it off and if I wanted to go from 75% to 50% I had to turn off the device and then tap the button 2 times to get to 50%.

This has two modes, default and "round robin". In default mode each execution of the action brightens the selected device up to 100% and then each execution will then dim it down to 0%. Basically you bounce between the ON state and OFF state through steps of brightness.

In Round Robin mode you can choose to just always brighten, in which case you brighten to 100% and the next execution will turn off the device and the next will brighten again.
