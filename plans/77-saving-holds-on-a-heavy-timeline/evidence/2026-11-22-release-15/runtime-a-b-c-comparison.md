# Plan 77 Runtime A, B and C comparison

The three browser trials used current App `e3dbad64d402724ac5a35fb6447f18e432c64b78`, Agent `8807f820eb47d6018db723511e024a0a123fbe95`, the same stock compiled artifact inventory, and the 300-clip signed v30 fixture. Each Runtime variant was restored independently. A cold was profiled at 100 Hz. Other browser runs were unprofiled. The post-cold C opening used a new browser profile and matched C cold's Runtime process identity by PID and birth receipt. The archive records the match as a boolean.

| Runtime | CPU before navigation, seconds from process birth | Cold writable, wall seconds | Cold Runtime CPU, seconds | Cold limit-50 history intervals, seconds | Same-process writable, wall seconds | Same-process Runtime CPU, seconds | Same-process history intervals, seconds |
| --- | ---: | ---: | ---: | --- | ---: | ---: | --- |
| A landed release literal `3c28211f` | 291.80 | 306.552 | 295.62 | 60.452 stopped, 60.112 stopped, 57.304 200 | 13.744 | 6.17 | 7.040 200 |
| B disposable release plus nine commits `c3f811cb` | 306.85 | 176.179 | 166.78 | 60.478 stopped, 47.176 200 | unobserved | unobserved | unobserved |
| C Round 5 `d7be2f04` | 299.62 | 165.019 | 155.57 | 60.294 stopped, 8.454 200 | 170.095 | 160.10 | 60.441 stopped, 40.685 200 |

The before-navigation CPU bucket includes live Runtime startup and preparation. It excludes offline restore and installer processes. Successful browser runs verified one active original v30 head, 300 clips, 10 occurrences, and zero timeline commit POSTs. A separate unprofiled stock A run stopped without writable at 480 seconds. B was a disposable unpushed single cold trial. There was one A trial, one B trial, and one C cold plus one C same-process opening. No trial measured a gesture.

The historical full Round 5 tuple reached writable in 22.994 seconds and used 19.89 Runtime CPU seconds during opening. Its earlier Runtime CPU and process cache state were unobserved. File timestamps place navigation about 19 minutes after install started, 17 minutes 28 seconds after restore started, and 12 minutes 14 seconds after adoption started.

These observations do not isolate individual B commits or resolve differences between current and Round 5 consumers. Variant setup took about 17 minutes per arm. The next experiment in the source page is a current warm collision and legal timing, with the one-shot gesture guard intact and no inexpensive bisect available.
