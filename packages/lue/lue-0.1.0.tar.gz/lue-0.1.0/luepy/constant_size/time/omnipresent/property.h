#pragma once
#include "lue/constant_size/time/omnipresent/property.h"
#include <pybind11/pybind11.h>


namespace lue {
namespace constant_size {
namespace time {
namespace omnipresent {

pybind11::object   cast_to_specialized_property(
                                        Property const& property);

}  // namespace omnipresent
}  // namespace time
}  // namespace constant_size
}  // namespace lue
