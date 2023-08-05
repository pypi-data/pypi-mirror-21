#include "lue/constant_size/time/omnipresent/space_domain.h"
#include <pybind11/pybind11.h>


namespace py = pybind11;
using namespace pybind11::literals;


namespace lue {
namespace constant_size {
namespace time {
namespace omnipresent {

void init_space_domain_class(
    py::module& module)
{

    py::class_<SpaceDomain, constant_size::SpaceDomain>(
        module,
        "SpaceDomain",
        "SpaceDomain docstring...")

        ;

}

}  // namespace omnipresent
}  // namespace time
}  // namespace constant_size
}  // namespace lue
