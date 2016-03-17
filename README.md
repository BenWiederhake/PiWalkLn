# PiWalkLn

Random walk meets digits of pi, meets neat visualization

## What is this?

Take the digits of pi, use them as walking instructions, turn by a
fixed angle after each digit. As one can [consider pi to behave
normal](https://en.wikipedia.org/wiki/Pi#Properties), the walk will
stay reasonably close to the starting point.

![](/samples/pi_a1.04720_n0003000.png)
(3k digits with angle 60°)

Don't get me wrong, pi *does* wander off considerably, but in relation
to how far away it *could* go, it's not much.

## Why the fisheye?

Like I said, pi is an untamed beast that likes to wander both the
unexplored paths of the canvas and the well-known neighborhood of it's
own tail. Here's how it would look like without the transformation:

![](/samples/bad_4_128_64.png)
(10k digits with [the noisiest angle](https://www.wolframalpha.com/input/?i=180%C2%B0%2F%28golden+ratio%29), but without fisheye projection)

As you can see, the image is large, it's too far zoomed out, and part
of the trail is missing (it should go to blue as in `(0, 0, 255)`).

Thus the idea of using transformed coordinates: the further away from
the center, the more crunched/compressed the image is. This allows a
very large region to be covered, while still showing the "pattern" at a
comfortable size.

![](/samples/pi_a1.94161_n0010000.png)
(10k digits with [the noisiest angle](https://www.wolframalpha.com/input/?i=180%C2%B0%2F%28golden+ratio%29), but *with* fisheye projection)

## Seriously, how does the fisheye thing work?

I don't know why you're interested, but it's a very simple idea:
- If the distance (to the starting point `(0, 0)`, which will be at the
  center of the image) is less-or-equal 1, then keep it.
- If the distance is bigger, use `1 + ln d` instead.

Here's what a [Hilbert Walk](https://en.wikipedia.org/wiki/Hilbert_curve) (which is great to visualize how a square gets distorted) looks like using this projection:
![](/Hilbert_walk.png)


### What?

Thanks for asking.

This composite function has the wonderful property of being
[continuously differentiable][C1],
which means that the transition between "keep it" and "use `1 + ln d`"
is smooth.

Also, it means that the covered walk-space grows exponentially with
image size, which means that we can always keep the walk "in sight".
Don't let pi escape!

[C1]: https://en.wikipedia.org/wiki/Differentiable_function#Differentiability_classes

### What's with the weird grey lines that don't form a box?

These *do* form a box, but they're distorted by the fisheye projection.
- dark grey: rectangle from `(-2,-1)` to `(2,1)`
- medium grey: rectangle from `(-20,-10)` to `(20,10)`
- light grey: rectangle from `(-200,-100)` to `(200,100)`

![](/samples/pi_a3.12414_n0001000.png)
(1k digits with angle 179°)

## So what does it look like?

Thanks for asking! I want to show you even more images:

![](/samples/pi_a1.57080_n0010000.png)
(10k digits with angle 90°)

![](/samples/pi_a0.31416_n0000030.png)
(30 digits with angle 18°)

For more samples, look at the `samples` folder. Or, hey, why don't you
clone it and experiment yourself? Feel free to share awesome images by
making a PR :D
