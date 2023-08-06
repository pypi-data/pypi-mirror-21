Documentation: http://pybinding.site/

v0.9.1 | 2017-04-28

* Fixed an issue with multi-orbital models where onsite/hopping modifiers would return unexpected
  results if a new `energy` array was returned (rather than being modified in place).

* Fixed `Solver.calc_spatial_ldos` and `Solver.calc_probability` returning single-orbital results
  for multi-orbital models.

* Fixed slicing of `Structure` objects and made access to the `data` property of `SpatialMap` and
  `StructureMap` mutable again.



