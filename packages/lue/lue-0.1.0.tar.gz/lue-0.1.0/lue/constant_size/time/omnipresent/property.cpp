#include "lue/constant_size/time/omnipresent/property.h"


namespace lue {
namespace constant_size {
namespace time {
namespace omnipresent {

// Property::Property(
//     constant_size::Property&& property)
// 
//     : constant_size::Property(std::forward<constant_size::Property>(property))
// 
// {
// }


Property::Property(
    hdf5::Identifier const& id)

    : constant_size::Property(id)

{
}


Property::Property(
    lue::Property const& property)

    : constant_size::Property(property)

{
}


Property create_property(
    PropertySet& property_set,
    std::string const& name,
    Property::Configuration const& configuration)
{
    auto& properties = property_set.properties();
    auto& property = properties.add(name, std::move(
        constant_size::create_property(properties, name, configuration)));

    return Property(property.id());
}

}  // namespace omnipresent
}  // namespace time
}  // namespace constant_size
}  // namespace lue
