Date: 2026-11-11
Kind: fix
Source: Owner request while handing off Plan 48
Resolved by: —

The plan skill had a rubric for when a review is load-bearing but nothing equivalent for test runs; the rules were spread across the run contract and the manage skill's baseline step. The run contract now has one table of the four moments a test run bears load (before the first task, after each task, before others build on a shared part, before review), what to run at each, what to skip, and a cost exception for inventories that run in seconds. The plan skill links to it.
