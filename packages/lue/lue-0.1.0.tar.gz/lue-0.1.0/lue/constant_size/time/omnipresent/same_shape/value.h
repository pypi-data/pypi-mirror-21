#pragma once
// #include "../value.h"
#include "lue/array.h"
#include "lue/hdf5/group.h"
// #include "lue/chunks.h"
// #include <memory>


namespace lue {
namespace constant_size {
namespace time {
namespace omnipresent {
namespace same_shape {

/*!
    The property value is represented by a dataset where the first
    dimension represents the items and the subsequent dimensions represent
    the value per item.

    @sa create_value
*/
class Value:
    // public omnipresent::Value,
    public Array
{

public:

                   Value               (hdf5::Identifier const& location,
                                        std::string const& name,
                                        hdf5::Datatype const& memory_datatype);

                   // Value               (hdf5::Identifier const& location,
                   //                      std::string const& name,
                   //                      hid_t const type_id);

                   // Value               (hdf5::Identifier&& location,
                   //                      hid_t const type_id);

                   Value               (hdf5::Dataset&& dataset,
                                        hdf5::Datatype const& memory_datatype);

                   Value               (Value const& other)=delete;

                   Value               (Value&& other)=default;

                   ~Value              ()=default;

    Value&         operator=           (Value const& other)=delete;

    Value&         operator=           (Value&& other)=default;

    void           reserve             (hsize_t const nr_items);

private:

};


Value              create_value        (hdf5::Group const& group,
                                        std::string const& name,
                                        hdf5::Datatype const& file_datatype,
                                        hdf5::Datatype const& memory_datatype);

Value              create_value        (hdf5::Group const& group,
                                        std::string const& name,
                                        hdf5::Datatype const& file_datatype,
                                        hdf5::Datatype const& memory_datatype,
                                        hdf5::Shape const& value_shape,
                                        hdf5::Shape const& value_chunk);

}  // namespace same_shape
}  // namespace omnipresent
}  // namespace time
}  // namespace constant_size
}  // namespace lue
