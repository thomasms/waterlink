# waterlink

## Belgian water cost estimator for WaterLink

Most people don't realise how much water costs, and are unaware of the "comfort" threshold.
Once you go above this threshold water usage is charged double, yes double, the amount, so this simple computer tells you how much it will cost you.

It is important to realise (and this takes it into account):

- Water rates change per year
- The threshold depends on the number of people in the household
- The threshold depends on the number of households (if they share a water meter)

**we** or **WE** is the number of households to take into account. This is if you share a water meter, by default this is just 1.

**dom** or **DOM** is the number of people to take into account (across all households).

For example:

- if you live alone and do not share a water meter with another household: we=1, dom=1
- if you are a couple and do not share a water meter with another household: we=1, dom=2
- if you are a family of four and do not share a water meter with another household: we=1, dom=4
- if you are a family of four and share a water meter with another household with another couple: we=2, dom=6

It is important also to realise that they only count someone if they are registered in the household on the 1st January. If someone moves in on the 2nd January (officially) then they will not count until the next 1st January. Similarly if someone leaves on the 2nd January (officially) they will still be counted until 31st December. This is very important because this changes your comfort threshold - normally 30m3 per person.
