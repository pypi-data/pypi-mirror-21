#include "lue/constant_size/time/omnipresent/domain.h"


namespace lue {
namespace constant_size {
namespace time {
namespace omnipresent {

Domain::Domain(
    hdf5::Identifier const& location)

    : constant_size::Domain(location),
      _space(id())

{
}


Domain::Domain(
    constant_size::Domain&& domain)

    : constant_size::Domain(std::forward<constant_size::Domain>(domain)),
      _space(id())

{
}


SpaceDomain const& Domain::space() const
{
    return _space;
}


SpaceDomain& Domain::space()
{
    return _space;
}


Domain create_domain(
    hdf5::Identifier const& location)
{
    auto domain = constant_size::create_domain(location);
    auto space = omnipresent::create_space_domain(domain);

    return Domain(std::move(domain));
}

}  // namespace omnipresent
}  // namespace time
}  // namespace constant_size
}  // namespace lue
