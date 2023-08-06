
evoalgos has been tested with Python 2.7 and 3.4. The recommended version is
Python 3.x, because compatibility is reached by avoiding usage of xrange. So,
the code has a higher memory consumption under Python 2.

Everything in this package is pure Python. For a description of the contents
see DESCRIPTION.rst.


Changes
=======

0.7
---
* Added FixedSizeSetIndividual to evoalgos.individual. It can be used to evolve
  sets of fixed size and bitstrings with a fixed number of ones.
* evoalgos.reproduction.ESReproduction got a new argument
  "redetermine_first_parent".
* Added a function connected_components to
  evoalgos.niching.NearestBetterClustering.
* Added forgotten documentation for RankSumSorting.

0.6
---
* Gave distance function argument a default for NearestBetterSorting and
  NearestBetterSelection.
* Changed the provided distance for NearestBetterSorting and
  NearestBetterSelection from squared Euclidean distance to Euclidean distance.
* Added a module evoalgos.niching with the two basin identification methods
  TopographicalSelection and NearestBetterClustering.
* Moved the inner class NearestBetterSorting.DistMatrixFunction to its own
  module. New place: evoalgos.distance.DistMatrixFunction.

0.5
---
* Simplified the code in the sorting module.
* Added sorting component RankSumSorting for many-objective optimization.
* Added a multiobjective mode of operation to NearestBetterSorting and
  NearestBetterSelection.

0.4
---
* LexicographicSorting can now also sort when objective values are just scalars.
* Implemented NearestBetterSorting and NearestBetterSelection.
* identify_groups() and identify_best_group() of CrowdingDistanceSorting and
  HyperVolumeContributionSorting now also consider the respective secondary
  criteria (before: only dominance relation).
* Added documentation about parallelization.

0.3
---
* Added BinaryIndividual for optimization in binary search spaces.
* Added convenience classes CommaEA and PlusEA, which are special cases of
  EvolutionaryAlgorithm. By default, they are intended for single-objective
  optimization.

0.2
---
* Implemented the NSGA2b (NSGA2 with extensions).
* Fixed bug when individuals with identical objective values should be sorted
  by HyperVolumeContributionSorting (led to "unorderable types" exception
  under Python 3).
* Changed default setting for parameter "prefer_boundary_points" of SMSEMOA
  to True.

0.1
---
* Initial version containing the SMS-EMOA.
